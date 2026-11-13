# Crush

Crush reads its configuration from a shell file named `crushrc` (`./.crushrc`, `./crushrc` or `~/.config/crush/crushrc`). Append the line from `crushrc` to sign in with OAuth, or the command from `crushrc.api-key` to send an API key from `AYINBOX_API_KEY`; Crush drops a header whose value comes out empty. The older `crush.json` format still works but is deprecated, so this folder uses `crushrc`. Source: https://github.com/charmbracelet/crush
