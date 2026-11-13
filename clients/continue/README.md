# Continue

Copy `ayinbox.yaml` to `.continue/mcpServers/ayinbox.yaml` in your workspace, or move its `mcpServers` entry into your `config.yaml`. `apiKey` is sent as `Authorization: Bearer`, and `${{ secrets.AYINBOX_API_KEY }}` reads the secret named `AYINBOX_API_KEY` from Continue's local secrets (for example a `.env` file in `~/.continue`). Continue does not document MCP OAuth, so this folder has the API-key form only. Sources: https://docs.continue.dev/customize/deep-dives/mcp and https://docs.continue.dev/reference
