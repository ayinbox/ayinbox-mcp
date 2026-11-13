# Claude Code

OAuth, from a shell:

```bash
claude mcp add --transport http --scope user ayinbox https://api.ayinbox.com/v1/mcp
claude mcp login ayinbox
```

Or run `/mcp` inside Claude Code and choose the server to sign in. With an API key, add `--header "Authorization: Bearer $AYINBOX_API_KEY"` to the first command instead of logging in, or put `.mcp.json` from this folder at the root of a project: Claude Code expands `${AYINBOX_API_KEY}` in `url` and `headers` when it loads the file, and leaves an unset variable as literal text with a warning. `claude mcp list` shows whether it connected. This repository is also a Claude Code plugin (`/plugin marketplace add ayinbox/ayinbox-mcp`, then `/plugin install ayinbox@ayinbox`), which connects with OAuth and adds the agent skill. Source: https://code.claude.com/docs/en/mcp
