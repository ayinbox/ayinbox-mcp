# Security

Report a vulnerability in AY Inbox, its MCP server or anything in this repository by email to [team@ayinbox.com](mailto:team@ayinbox.com). Do not open a public issue for it.

Include what you found, how to reproduce it and what it lets someone do. We will reply to confirm we received it.

If you think an API key has leaked (for example, committed with one of the config files here), revoke it in the dashboard under **Settings > API keys** and create a new one. The files in `clients/` never need a real key committed: they read it from `AYINBOX_API_KEY` or ask for it, except where a client cannot do either, and those READMEs say so.
