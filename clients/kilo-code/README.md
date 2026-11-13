# Kilo Code

Merge `kilo.json` into `~/.config/kilo/kilo.jsonc` (global) or `kilo.jsonc` / `.kilo/kilo.jsonc` in a project. Kilo Code starts the OAuth flow when it connects; click the notification to sign in. For an API key use `kilo.api-key.json`: Kilo replaces `{env:AYINBOX_API_KEY}` (no `$`) with the environment variable, and `"oauth": false` stops it from starting a sign-in. Source: https://kilo.ai/docs/features/mcp/using-mcp-in-kilo-code
