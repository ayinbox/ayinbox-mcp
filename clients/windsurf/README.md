# Windsurf

Merge `mcp_config.json` into `~/.codeium/windsurf/mcp_config.json` and refresh the MCP servers in Cascade. Cascade signs in with OAuth for a streamable HTTP server that asks for it. For an API key use `mcp_config.api-key.json`: Windsurf replaces `${env:AYINBOX_API_KEY}` in `headers` with the environment variable. Source: https://docs.devin.ai/windsurf/plugins/cascade/mcp
