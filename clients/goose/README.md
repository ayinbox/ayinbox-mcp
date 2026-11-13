# Goose

Merge the `ayinbox` entry from `config.yaml` into the `extensions:` block of `~/.config/goose/config.yaml`, or run `goose configure` and choose **Add Extension > Remote Extension (Streamable HTTP)**. With no headers, Goose runs the OAuth sign-in itself when AY Inbox asks for it. For an API key use `config.api-key.yaml`: Goose substitutes `${AYINBOX_API_KEY}` in a header only when the variable is listed in `env_keys` of the same entry, and then takes it from your environment or Goose's secret store. Source: https://goose-docs.ai/docs/getting-started/using-extensions
