# Zed

Open your settings with **zed: open settings file** and merge the `context_servers` entry from `settings.json`, or use **Settings > AI > MCP Servers > Add Server > Add Remote Server**. With no `Authorization` header, Zed prompts you to sign in with the standard MCP OAuth flow. For an API key use `settings.api-key.json` and replace `aybox_...` with your key: Zed documents no environment variable expansion in headers, so the key sits in your settings file in plain text. Source: https://zed.dev/docs/ai/mcp
