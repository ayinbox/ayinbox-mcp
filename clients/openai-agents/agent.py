import asyncio
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp


async def main() -> None:
    async with MCPServerStreamableHttp(
        name="ayinbox",
        params={
            "url": "https://api.ayinbox.com/v1/mcp?toolsets=inbox",
            "headers": {"Authorization": f"Bearer {os.environ['AYINBOX_API_KEY']}"},
        },
    ) as ayinbox:
        agent = Agent(name="Inbox assistant", mcp_servers=[ayinbox])
        result = await Runner.run(agent, "Summarize my unread replies from today.")
        print(result.final_output)


asyncio.run(main())
