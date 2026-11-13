# Publishing to the official MCP Registry

`server.json` publishes as `com.ayinbox/ayinbox`. A `com.ayinbox/*` name needs proof that the publisher controls `ayinbox.com`, by HTTP (a file on the site) or DNS (a TXT record). This repository has no package, only a remote, so there is no package ownership check.

These steps follow the registry's own docs as of `mcp-publisher` 1.8.9 and schema `2025-12-11`: [authentication](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx), [remote servers](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/remote-servers.mdx), [quickstart](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx).

## 1. Install mcp-publisher

```bash
brew install mcp-publisher
```

or the release binary:

```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/
```

Check the file before publishing (it validates against the live registry and changes nothing):

```bash
mcp-publisher validate server.json
```

## 2. Make a signing key

Ed25519 needs OpenSSL 3. macOS's system `openssl` is LibreSSL and fails with `Algorithm Ed25519 not found`; use `brew install openssl@3` and call `/opt/homebrew/opt/openssl@3/bin/openssl` (Intel: `/usr/local/opt/openssl@3/bin/openssl`) in place of `openssl` below.

```bash
openssl genpkey -algorithm Ed25519 -out key.pem
PUBLIC_KEY="$(openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64)"
```

`key.pem` is the private key. Keep it out of this repository (`.gitignore` already lists it) and out of chat and logs. Store it in a password manager or a CI secret.

## 3a. Prove the domain over HTTP (preferred)

Write the proof record:

```bash
echo "v=MCPv1; k=ed25519; p=${PUBLIC_KEY}" > mcp-registry-auth
```

Serve that file at exactly:

```
https://ayinbox.com/.well-known/mcp-registry-auth
```

What the registry requires of that URL:

| Property | Requirement |
|---|---|
| Request it sends | `GET https://ayinbox.com/.well-known/mcp-registry-auth` with `Accept: text/plain` and `User-Agent: mcp-registry/1.0`, from Google Cloud addresses |
| Status | `200 OK`. Redirects are not followed, so a `301` or `302` fails |
| Body | the proof record, one record per line, `v=MCPv1; k=ed25519; p=<base64 public key>`, at most 4096 bytes in all. Surrounding whitespace is ignored. An HTML page with a `200` fails |
| Reachability | every public address of `ayinbox.com` must answer, IPv6 included; no WAF, bot or geo rule may challenge the request |
| Timeout | 15 seconds overall, at most one retry |

`ayinbox.com` already serves `/.well-known/security.txt` as `text/plain` with `200` to that user agent, so putting the file next to it on the site works the same way. Check what the registry will see:

```bash
curl -sS -o - -w '\n%{http_code}\n' -H 'Accept: text/plain' -A 'mcp-registry/1.0' \
  https://ayinbox.com/.well-known/mcp-registry-auth
```

Then log in:

```bash
MCP_PRIVATE_KEY="$(openssl pkey -in key.pem -noout -text | sed -n '/priv:/,/pub:/p' | sed '1d;$d' | tr -d ' :\n')" \
  mcp-publisher login http --domain ayinbox.com
```

The command prints an `Expected proof record:` line; it must match the file's contents. A `token exchange failed with status 401` means the registry could not fetch the file or the key does not match.

## 3b. Or prove the domain over DNS

Add a TXT record on the apex `ayinbox.com` (not on `_mcp-auth.ayinbox.com` or any other selector) with the value:

```
v=MCPv1; k=ed25519; p=<PUBLIC_KEY>
```

Print it with:

```bash
echo "ayinbox.com. IN TXT \"v=MCPv1; k=ed25519; p=${PUBLIC_KEY}\""
```

Wait for it to show in `dig TXT ayinbox.com +short`, then:

```bash
MCP_PRIVATE_KEY="$(openssl pkey -in key.pem -noout -text | sed -n '/priv:/,/pub:/p' | sed '1d;$d' | tr -d ' :\n')" \
  mcp-publisher login dns --domain ayinbox.com
```

Leave the other TXT records on the apex (SPF, verifications) as they are.

## 4. Publish

From the repository root:

```bash
mcp-publisher publish
```

Check it:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=com.ayinbox/ayinbox"
```

## Later releases

Each publish needs a new `version` in `server.json` (the registry refuses a version it already has, and a published version cannot be edited). Bump it, add a `CHANGELOG.md` entry, run `mcp-publisher validate server.json`, log in again (registry tokens last minutes) and `mcp-publisher publish`.

To rotate the key, add the new record as a second line of the file (or a second TXT record), log in with the new key, then remove the old record. An old record left in place keeps the old key valid.
