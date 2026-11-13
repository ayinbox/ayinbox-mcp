# Codex CLI

OAuth: `codex mcp add ayinbox --url https://api.ayinbox.com/v1/mcp`, then `codex mcp login ayinbox` to sign in in the browser. `config.toml` here is the same entry written by hand into `~/.codex/config.toml`. With an API key, use `config.api-key.toml` instead, or `codex mcp add ayinbox --url https://api.ayinbox.com/v1/mcp --bearer-token-env-var AYINBOX_API_KEY`; Codex reads the key from `AYINBOX_API_KEY` when it connects and never stores it in the file. Source: https://developers.openai.com/codex/mcp
