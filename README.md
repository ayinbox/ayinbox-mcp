# AY Inbox MCP server

AY Inbox is a hosted cold email platform: it sends cold email at a paced daily volume, brings every reply into one inbox (Unibox), drafts answers from a campaign brain, and can offer a meeting time from Cal.com or Calendly. Its MCP server lets an AI agent build contact lists, draft campaigns and their brains, read replies and draft answers, and track deals, with the same credential as the REST API.

- **Server URL:** `https://api.ayinbox.com/v1/mcp` (streamable HTTP; one JSON-RPC message per POST, no session, no event stream)
- **Protocol versions:** `2025-11-25`, `2025-06-18`, `2025-03-26`
- **Sign in with OAuth 2.1:** add the URL with no key. The client finds the sign-in on its own (a `401` challenge, protected-resource metadata, dynamic client registration, PKCE), you sign in at app.ayinbox.com and approve the scopes. No key to copy.
- **Or use an API key:** create one in the dashboard under **Settings > API keys** (it starts with `aybox_` and is shown once) and send `Authorization: Bearer aybox_...`. The examples here read it from `AYINBOX_API_KEY`.
- **Official MCP Registry name:** `com.ayinbox/ayinbox`
- **Access:** Access to the hosted service is invite only for now: ask at [team@ayinbox.com](mailto:team@ayinbox.com).
- **Agent guide:** [ayinbox.com/skill.md](https://ayinbox.com/skill.md)

AY Inbox is a hosted service. This repository holds the registry manifest, connect steps and ready-to-copy client configs for its MCP server. The service itself is not open source.

## Connect

Every client below has a folder in [`clients/`](clients/) with the config file and a short README. Where a client can read an environment variable in its config, the API-key form uses `AYINBOX_API_KEY`. Where it cannot, the file has `aybox_...` to replace with your key, and the key then sits in that file in plain text: keep it out of version control.

### Claude (web and desktop)

**Customize > Connectors > Add > Add custom connector**, name it AY Inbox, paste `https://api.ayinbox.com/v1/mcp`, choose **Continue**, keep the detected options, choose **Add**, then **Connect** and sign in. On Team and Enterprise plans an owner adds it under **Organization settings > Connectors > Add > Custom > Web** and members connect it from **Customize > Connectors**.

Custom connectors use OAuth. For an API key in Claude Desktop, bridge it with [`mcp-remote`](https://github.com/punkpeye/mcp-remote) (third party, needs Node.js) in `claude_desktop_config.json`: [`clients/claude-desktop/`](clients/claude-desktop/).

```json
{
  "mcpServers": {
    "ayinbox": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.ayinbox.com/v1/mcp", "--header", "Authorization:${AYINBOX_AUTH}"],
      "env": { "AYINBOX_AUTH": "Bearer aybox_..." }
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http --scope user ayinbox https://api.ayinbox.com/v1/mcp
claude mcp login ayinbox
```

API key:

```bash
claude mcp add --transport http --scope user ayinbox https://api.ayinbox.com/v1/mcp \
  --header "Authorization: Bearer $AYINBOX_API_KEY"
```

Or install this repository as a plugin, which connects with OAuth and adds the agent skill:

```
/plugin marketplace add ayinbox/ayinbox-mcp
/plugin install ayinbox@ayinbox
```

A project `.mcp.json` with `${AYINBOX_API_KEY}` is in [`clients/claude-code/`](clients/claude-code/).

### ChatGPT

Where your plan offers developer mode: [chatgpt.com/plugins](https://chatgpt.com/plugins) > **+** > **Add custom MCP server**, paste `https://api.ayinbox.com/v1/mcp`, choose **OAuth**, then **Create as a plugin** and sign in. ChatGPT documents no header or API-key option for custom servers.

### Codex CLI

```bash
codex mcp add ayinbox --url https://api.ayinbox.com/v1/mcp
codex mcp login ayinbox
```

API key (Codex reads the variable when it connects):

```bash
codex mcp add ayinbox --url https://api.ayinbox.com/v1/mcp --bearer-token-env-var AYINBOX_API_KEY
```

```toml
# ~/.codex/config.toml
[mcp_servers.ayinbox]
url = "https://api.ayinbox.com/v1/mcp"
bearer_token_env_var = "AYINBOX_API_KEY"
```

### Cursor

`~/.cursor/mcp.json` or `.cursor/mcp.json`. With only the URL, Cursor signs in with OAuth:

```json
{
  "mcpServers": {
    "ayinbox": { "url": "https://api.ayinbox.com/v1/mcp" }
  }
}
```

API key:

```json
{
  "mcpServers": {
    "ayinbox": {
      "url": "https://api.ayinbox.com/v1/mcp",
      "headers": { "Authorization": "Bearer ${env:AYINBOX_API_KEY}" }
    }
  }
}
```

### VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json`, or **MCP: Open User Configuration**. VS Code registers itself and opens the browser to sign in:

```json
{
  "servers": {
    "ayinbox": { "type": "http", "url": "https://api.ayinbox.com/v1/mcp" }
  }
}
```

API key (VS Code asks for it once and stores it as a secret):

```json
{
  "inputs": [
    { "type": "promptString", "id": "ayinbox-api-key", "description": "AY Inbox API key", "password": true }
  ],
  "servers": {
    "ayinbox": {
      "type": "http",
      "url": "https://api.ayinbox.com/v1/mcp",
      "headers": { "Authorization": "Bearer ${input:ayinbox-api-key}" }
    }
  }
}
```

### GitHub Copilot CLI

Add the server to `~/.copilot/mcp-config.json` (see [`clients/copilot-cli/`](clients/copilot-cli/)), then run `/mcp auth ayinbox` in `copilot` to sign in. API key:

```bash
copilot mcp add --transport http --header "Authorization: Bearer $AYINBOX_API_KEY" ayinbox https://api.ayinbox.com/v1/mcp
```

### Gemini CLI

```bash
gemini mcp add --transport http --scope user ayinbox https://api.ayinbox.com/v1/mcp
```

Sign in with `/mcp auth ayinbox`. API key (your shell expands the variable when you run it):

```bash
gemini mcp add --transport http --scope user --header "Authorization: Bearer $AYINBOX_API_KEY" ayinbox https://api.ayinbox.com/v1/mcp
```

Or install this repository as an extension, which connects with OAuth and loads the agent skill: `gemini extensions install https://github.com/ayinbox/ayinbox-mcp`.

### Windsurf

`~/.codeium/windsurf/mcp_config.json`. Without headers, Cascade signs in with OAuth:

```json
{
  "mcpServers": {
    "ayinbox": {
      "serverUrl": "https://api.ayinbox.com/v1/mcp",
      "headers": { "Authorization": "Bearer ${env:AYINBOX_API_KEY}" }
    }
  }
}
```

### Zed

`settings.json`, or **Settings > AI > MCP Servers > Add Server > Add Remote Server**. With no header, Zed runs the MCP OAuth sign-in:

```json
{
  "context_servers": {
    "ayinbox": { "url": "https://api.ayinbox.com/v1/mcp" }
  }
}
```

API key: add `"headers": { "Authorization": "Bearer aybox_..." }` with your key pasted in. Zed documents no variable expansion in headers.

### JetBrains Junie

`~/.junie/mcp/mcp.json` (or **Tools > Junie > MCP Settings > Add**) with `{"mcpServers": {"ayinbox": {"url": "https://api.ayinbox.com/v1/mcp"}}}`, then open the server's menu, choose **Authorize** and sign in. API key: add `"headers": { "Authorization": "Bearer aybox_..." }` with your key pasted in. See [`clients/junie/`](clients/junie/).

### Cline

OAuth: **MCP Servers > Remote Servers**, name `ayinbox`, URL `https://api.ayinbox.com/v1/mcp`, transport **Streamable HTTP**, **Add Server**, then sign in. API key:

```bash
cline mcp add ayinbox https://api.ayinbox.com/v1/mcp --transport http --header "Authorization: Bearer $AYINBOX_API_KEY" --yes
```

### Roo Code

API key only (Roo Code does not document MCP OAuth), in `.roo/mcp.json` or the global `mcp_settings.json`:

```json
{
  "mcpServers": {
    "ayinbox": {
      "type": "streamable-http",
      "url": "https://api.ayinbox.com/v1/mcp",
      "headers": { "Authorization": "Bearer aybox_..." }
    }
  }
}
```

### Kilo Code

`~/.config/kilo/kilo.jsonc` or `kilo.jsonc` in a project. Kilo starts the OAuth flow when it connects:

```json
{
  "mcp": {
    "ayinbox": { "type": "remote", "url": "https://api.ayinbox.com/v1/mcp", "enabled": true }
  }
}
```

API key: add `"headers": { "Authorization": "Bearer {env:AYINBOX_API_KEY}" }` and `"oauth": false`.

### Continue

API key only (Continue does not document MCP OAuth). `.continue/mcpServers/ayinbox.yaml`:

```yaml
name: AY Inbox
version: 1.0.0
schema: v1
mcpServers:
  - name: AY Inbox
    type: streamable-http
    url: https://api.ayinbox.com/v1/mcp
    apiKey: ${{ secrets.AYINBOX_API_KEY }}
```

### Goose

`~/.config/goose/config.yaml`, or `goose configure` > **Add Extension > Remote Extension (Streamable HTTP)**. With no headers Goose runs the OAuth sign-in itself:

```yaml
extensions:
  ayinbox:
    type: streamable_http
    name: ayinbox
    enabled: true
    uri: https://api.ayinbox.com/v1/mcp
    timeout: 300
```

API key: add the header and list the variable in `env_keys`, which Goose requires before it substitutes it:

```yaml
    headers:
      Authorization: "Bearer ${AYINBOX_API_KEY}"
    env_keys:
      - AYINBOX_API_KEY
```

### OpenCode

`opencode.json`, then `opencode mcp auth ayinbox`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ayinbox": { "type": "remote", "url": "https://api.ayinbox.com/v1/mcp", "enabled": true }
  }
}
```

API key: add `"oauth": false` and `"headers": { "Authorization": "Bearer {env:AYINBOX_API_KEY}" }`.

### Crush

In `crushrc` (`./.crushrc`, `./crushrc` or `~/.config/crush/crushrc`):

```bash
# OAuth
mcp add ayinbox --type http --url "https://api.ayinbox.com/v1/mcp" --oauth true

# or an API key
mcp add ayinbox --type http --url "https://api.ayinbox.com/v1/mcp" \
  --header Authorization "Bearer $AYINBOX_API_KEY"
```

### Amp

```bash
amp mcp add ayinbox https://api.ayinbox.com/v1/mcp
```

Amp opens the browser to sign in. API key, in `~/.config/amp/settings.json`:

```json
{
  "amp.mcpServers": {
    "ayinbox": {
      "url": "https://api.ayinbox.com/v1/mcp",
      "headers": { "Authorization": "Bearer ${AYINBOX_API_KEY}" }
    }
  }
}
```

### Hermes Agent

`~/.hermes/config.yaml`, then `hermes mcp login ayinbox`:

```yaml
mcp_servers:
  ayinbox:
    url: https://api.ayinbox.com/v1/mcp
    auth: oauth
```

API key: replace `auth: oauth` with a `headers:` map holding `Authorization: "Bearer aybox_..."` and your key pasted in. See [`clients/hermes/`](clients/hermes/).

### OpenAI Agents SDK and Responses API

```python
import os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="ayinbox",
    params={
        "url": "https://api.ayinbox.com/v1/mcp?toolsets=inbox",
        "headers": {"Authorization": f"Bearer {os.environ['AYINBOX_API_KEY']}"},
    },
) as ayinbox:
    agent = Agent(name="Inbox assistant", mcp_servers=[ayinbox])
    result = await Runner.run(agent, "Summarize my unread replies from today.")
```

For the Responses API, the remote MCP tool entry is in [`clients/openai-agents/responses-mcp-tool.json`](clients/openai-agents/responses-mcp-tool.json).

### Claude Agent SDK

```ts
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Summarize my unread AY Inbox replies from today.",
  options: {
    mcpServers: {
      ayinbox: {
        type: "http",
        url: "https://api.ayinbox.com/v1/mcp",
        headers: { Authorization: `Bearer ${process.env.AYINBOX_API_KEY}` },
      },
    },
    allowedTools: ["mcp__ayinbox__*"],
  },
})) {
  if (message.type === "result" && message.subtype === "success") console.log(message.result);
}
```

The SDK runs no interactive sign-in, so use an API key. Python is in [`clients/claude-agent-sdk/agent.py`](clients/claude-agent-sdk/agent.py).

### Any other client

Point a client that supports remote MCP over streamable HTTP at `https://api.ayinbox.com/v1/mcp`. If it supports MCP OAuth, it signs in on its own; otherwise send `Authorization: Bearer <key>`. A plain request works too:

```bash
curl -s https://api.ayinbox.com/v1/mcp \
  -H "Authorization: Bearer $AYINBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**Check it worked:** ask your agent to call `get_workspace_limits`. It is a free read that shows the plan's limits next to what the workspace uses.

## Tools

The server lists only the tools your credential may call. With every scope, that is 174 tools in twelve toolsets. Add `?toolsets=` to the URL to narrow the list for a small model, for example `https://api.ayinbox.com/v1/mcp?toolsets=inbox,campaigns` (some OAuth clients tie the token to the exact URL and then get the whole list).

| Toolset | What it covers | Tools |
|---|---|---|
| `inbox` | Read and sort replies, draft answers, offer meeting times | `list_threads`, `get_thread`, `draft_reply`, `generate_reply_draft`, `get_inbox_overview`, `get_unread_count`, `list_agent_drafts`, `discard_agent_draft`, `mark_thread_seen`, `set_thread_labels`, `move_thread_folder`, `snooze_thread`, `unsnooze_thread`, `list_scheduled_sends`, `cancel_scheduled_send`, `get_booking_settings`, `update_booking_settings`, `enable_booking_auto`, `get_booking_summary`, `list_booking_types`, `create_booking_type`, `update_booking_type`, `delete_booking_type`, `list_booking_event_types`, `get_availability`, `list_meeting_offers`, `get_meeting_offer`, `offer_meeting_times`, `stop_meeting_offer`, `resume_meeting_offer`, `reject_meeting_pick` |
| `campaigns` | Campaigns, their steps, campaign brains and auto-reply | `list_campaigns`, `get_campaign`, `get_campaign_stats`, `list_campaign_leads`, `create_campaign_draft`, `update_campaign`, `delete_campaign`, `set_campaign_status`, `set_lead_hold`, `list_campaign_senders`, `set_campaign_senders`, `verify_campaign_tracking_domain`, `get_campaign_logs`, `list_campaign_steps`, `add_campaign_step`, `update_campaign_step`, `delete_campaign_step`, `list_brains`, `get_brain`, `preview_brain`, `get_brain_material`, `get_brain_internal`, `list_brain_pages`, `get_brain_page`, `write_brain_page`, `create_brain`, `update_brain`, `delete_brain`, `add_brain_material`, `update_brain_material`, `remove_brain_material`, `refresh_brain_material`, `set_campaign_brain`, `set_default_brain`, `get_auto_reply_settings`, `enable_auto_reply`, `pause_auto_reply`, `get_campaign_auto_reply`, `update_campaign_auto_reply`, `enable_campaign_auto_reply`, `list_auto_reply_runs`, `get_auto_reply_run`, `cancel_auto_reply_run` |
| `contacts` | Contacts, segments (saved audiences) and the do-not-contact list | `search_contacts`, `get_contact`, `add_contact`, `update_contact_fields`, `delete_contact`, `add_tag`, `remove_tag`, `bulk_edit_contacts`, `get_contact_timeline`, `get_contact_sent_emails`, `list_segments`, `get_segment`, `list_segment_fields`, `preview_segment`, `create_segment`, `update_segment`, `delete_segment`, `set_segment_members`, `list_campaign_segments`, `set_campaign_segments`, `add_segment_to_campaign`, `list_suppressions`, `add_suppressions` |
| `crm` | Pipelines, deals, tasks and notes | `list_pipelines`, `create_pipeline`, `update_pipeline`, `delete_pipeline`, `create_pipeline_stage`, `update_pipeline_stage`, `delete_pipeline_stage`, `list_deals`, `get_deal`, `list_deals_by_contact`, `create_deal`, `update_deal`, `move_deal_stage`, `delete_deal`, `list_tasks`, `list_task_types`, `create_task`, `update_task`, `complete_task`, `delete_task`, `list_contact_notes`, `add_contact_note`, `update_contact_note`, `delete_contact_note` |
| `forms` | Hosted forms and their submissions | `list_forms`, `get_form`, `create_form`, `update_form`, `delete_form`, `list_form_submissions`, `get_form_stats`, `get_campaign_forms`, `mint_form_link` |
| `analytics` | Sending results, mailbox health, the Advisor, placement tests | `get_dashboard_analytics`, `list_mailboxes`, `list_recommendations`, `get_advisor_summary`, `list_placement_tests`, `get_placement_test`, `list_placement_batches`, `get_placement_batch` |
| `mailboxes` | Settings of connected sender mailboxes | `get_mailbox`, `update_mailbox`, `set_mailbox_warmup`, `set_mailbox_send_hold`, `set_mailbox_tracking_domain`, `get_warmup_ban_status`, `submit_warmup_appeal`, `disconnect_mailbox` |
| `workspace` | Plan, limits, AI credits, labels | `get_workspace_limits`, `get_org_settings`, `get_subscription`, `get_subscription_limits`, `get_credit_balance`, `get_credit_usage`, `list_credit_transactions`, `list_labels` |
| `developer` | API keys and webhooks | `list_api_keys`, `create_api_key`, `update_api_key`, `revoke_api_key`, `list_webhooks`, `list_webhook_deliveries`, `delete_webhook`, `verify_webhook` |
| `automation` | Automations | `list_automations`, `get_automation`, `create_automation_draft`, `update_automation`, `set_automation_enabled`, `delete_automation` |
| `leads` | Paid lead finding within a budget, address checks | `find_leads`, `get_lead_job`, `list_lead_jobs`, `verify_email` |
| `research` | Web search and the workspace's playbooks | `search_web`, `load_skill` |

Every tool carries a `title` and the standard annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), so a client can ask before a tool that changes or deletes something. Every write tool takes an optional `idempotency_key`: pass one, and a retry with the same key and arguments returns the first result instead of running twice. The full table with each tool's scope is on the [MCP server docs page](https://docs.ayinbox.com/api/mcp/).

## Scopes

Each tool checks its own scope, and the member behind the credential also needs the matching role permission, so an MCP client never does more than its person could.

- **Read and draft.** For a model that reads mail written by people outside the workspace, create a key from the **Agent: read and draft** preset: every read scope plus `AI_DRAFT`. It reads the inbox, campaigns and contacts and has the AI write reply drafts (charged to AI credits), and holds no scope that writes or sends. Add `WRITE_CONTACTS` and `WRITE_CAMPAIGNS` for an agent that builds lists and campaigns.
- **Starting a campaign** with `set_campaign_status` takes `START_CAMPAIGNS` or `SEND_CAMPAIGNS`. A client connected with OAuth holds `START_CAMPAIGNS` only when its person ticked **Start and resume campaigns** on the consent screen. No key preset includes `START_CAMPAIGNS`; add it on purpose.
- **What a person must grant.** A client connected with OAuth is never granted `SEND_CAMPAIGNS`, API-key management or `WRITE_WORKSPACE`. So through the tools it never turns on auto-reply, automatic booking or an automation, never turns off first-email review, and never links an audience to (or widens a segment feeding) a campaign that is sending. Those need a person, or a key a workspace owner gave `SEND_CAMPAIGNS` on purpose.
- **Spending.** `find_leads` (needs `INTEGRATIONS` and `BULK_CONTACTS` and a `max_cost_usd` budget) and `generate_reply_draft` spend credits. Approve those scopes only for a client you trust to spend them.

The full scope list is on the [permissions page](https://docs.ayinbox.com/api/permissions/).

## What it will not do

- **No tool sends an individual email.** Replying, composing, booking a meeting and placement tests are not exposed over MCP, whatever the scope. Reply drafts wait for a person.
- **No tool lifts a person's stop.** Removing a suppression (which could undo an unsubscribe or a complaint), creating or changing a webhook and rotating its secret stay in the dashboard.
- **No tool writes what the AI reads as instructions.** The workspace's product description, ideal customer notes, voice and playbooks are not editable through tools.
- **No tool approves a first email, records consent, connects a mailbox, or changes the team, workspace settings or billing.**
- **Results are data.** Every tool result is fenced between `<<<UNTRUSTED_CONTENT>>>` markers, because anyone who can email the workspace or fill in a form writes text the model reads. The one exception is `load_skill`, which returns the workspace's own playbook.

## Troubleshooting

| You see | Meaning | Do |
|---|---|---|
| HTTP `401` with `WWW-Authenticate: Bearer resource_metadata="https://api.ayinbox.com/.well-known/oauth-protected-resource", scope="..."` | No credential, an unknown or revoked key, or an expired or revoked OAuth token. This is the challenge an OAuth client follows to sign in | Let the client sign in (for example `/mcp` in Claude Code), or check the key |
| A client that worked stops with `401` | OAuth access tokens last one hour and refresh themselves with a rotating refresh token; a revoked app or a failed refresh ends that | Sign in again from the client. Disconnected apps are under connected apps in the dashboard |
| HTTP `405` with `Allow: POST` on `GET`, `HEAD` or `DELETE` | The server keeps no session and opens no event stream | Send every message as a POST. A client that insists on an SSE stream cannot connect |
| HTTP `400` with JSON-RPC `-32600` | `MCP-Protocol-Version` names a version the server does not implement | Start again with `initialize` |
| `isError` text naming a scope | The credential lacks that scope; nothing ran | For OAuth, reconnect and grant it at consent where a client may hold it; for a key, the workspace owner widens it |
| `-32000` mailbox limit | The key is limited to some mailboxes and tools act across the workspace | Use a key without mailbox limits |
| `-32601` | No such tool on this surface | Use a name from `tools/list` |

Quote the `request_id` from an error body when you report a problem to [team@ayinbox.com](mailto:team@ayinbox.com).

## Docs

- [MCP server](https://docs.ayinbox.com/api/mcp/): every tool and its scope, toolsets, retries, errors
- [Agent quickstart](https://docs.ayinbox.com/api/agent-quickstart/)
- [For agents](https://docs.ayinbox.com/api/for-agents/)
- [OAuth 2.1](https://docs.ayinbox.com/api/oauth/)
- [Authentication](https://docs.ayinbox.com/api/authentication/)
- [Permissions](https://docs.ayinbox.com/api/permissions/)
- [Agent tools over REST](https://docs.ayinbox.com/api/agent-tools/)
- [OpenAI-compatible agents](https://docs.ayinbox.com/api/openai-agents/)
- [Agent guide (skill.md)](https://ayinbox.com/skill.md)

## What's in this repository

| Path | What it is |
|---|---|
| `server.json` | The server's entry in the [official MCP Registry](https://registry.modelcontextprotocol.io) |
| `clients/` | One folder per client with a ready-to-copy config and a README |
| `mcp.json` | A generic `mcpServers` entry for clients that take that shape |
| `.claude-plugin/`, `.mcp.json` | Claude Code plugin and marketplace manifests, and the plugin's MCP connection (OAuth) |
| `gemini-extension.json` | Gemini CLI extension manifest |
| `skills/ayinbox/SKILL.md` | The agent skill the plugin and the extension load |
| `PUBLISH.md` | How `server.json` is published to the registry |

## License

The files in this repository are MIT licensed. Access to the AY Inbox service is separate: ask at [team@ayinbox.com](mailto:team@ayinbox.com).
