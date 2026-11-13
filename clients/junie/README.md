# JetBrains Junie

Copy `mcp.json` to `~/.junie/mcp/mcp.json` (every project) or `.junie/mcp/mcp.json` (one project); in the IDE plugin, **Tools > Junie > MCP Settings > Add** opens the same file. The server then shows **Authorization required**: open its menu, choose **Authorize** and sign in in the browser. For an API key use `mcp.api-key.json` and replace `aybox_...` with your key, since Junie documents no environment variable expansion. Sources: https://junie.jetbrains.com/docs/junie-cli-mcp-configuration.html and https://junie.jetbrains.com/docs/junie-plugin-mcp-settings.html
