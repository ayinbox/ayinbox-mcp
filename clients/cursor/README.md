# Cursor

Copy `mcp.json` to `~/.cursor/mcp.json` (every project) or `.cursor/mcp.json` (one project), or merge its `ayinbox` entry into the file you have. With only the URL, Cursor signs in with OAuth the first time it connects. For an API key use `mcp.api-key.json`: Cursor replaces `${env:AYINBOX_API_KEY}` with the environment variable when it loads the file. Source: https://cursor.com/docs/context/mcp
