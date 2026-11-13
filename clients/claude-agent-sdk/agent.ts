import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Summarize my unread AY Inbox replies from today.",
  options: {
    mcpServers: {
      ayinbox: {
        type: "http",
        url: "https://api.ayinbox.com/v1/mcp",
        headers: { Authorization: `Bearer ${process.env.AYINBOX_API_KEY}` },
      },
    },
    allowedTools: ["mcp__ayinbox__*"],
  },
})) {
  if (message.type === "result" && message.subtype === "success") console.log(message.result);
}
