# OpenCode

Merge `opencode.json` into `opencode.json` in your project or into your global OpenCode config, then run `opencode mcp auth ayinbox` (or `/mcps` in the TUI) to sign in. For an API key use `opencode.api-key.json`: OpenCode replaces `{env:AYINBOX_API_KEY}` with the environment variable (`$AYINBOX_API_KEY` is not expanded), and `"oauth": false` skips the sign-in. Source: https://opencode.ai/docs/mcp-servers/
