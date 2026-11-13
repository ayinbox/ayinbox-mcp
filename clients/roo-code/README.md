# Roo Code

Merge `mcp.json` into `.roo/mcp.json` (one project, **Edit Project MCP**) or the global `mcp_settings.json` (**Edit Global MCP**), and replace `aybox_...` with your key. `"type": "streamable-http"` is required. Roo Code documents headers for authentication and does not document MCP OAuth, so this folder has the API-key form only; its `${env:...}` syntax is documented for `args`, not for headers, so paste the key itself. Source: https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo
