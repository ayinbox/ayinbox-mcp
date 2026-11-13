import asyncio
import os

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query


async def main() -> None:
    options = ClaudeAgentOptions(
        mcp_servers={
            "ayinbox": {
                "type": "http",
                "url": "https://api.ayinbox.com/v1/mcp",
                "headers": {"Authorization": f"Bearer {os.environ['AYINBOX_API_KEY']}"},
            }
        },
        allowed_tools=["mcp__ayinbox__*"],
    )
    async for message in query(prompt="Summarize my unread AY Inbox replies from today.", options=options):
        if isinstance(message, ResultMessage):
            print(message.result)


asyncio.run(main())
