"""
Episode 25 - app number one: a plain Python client. Start the server, list its tools, call one.
"""
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python", args=["server.py"])


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"tool: {tool.name:<16} {tool.description}")
            result = await session.call_tool("order_details", {"order_id": "A-1003"})
            print("\norder_details('A-1003') ->", result.content[0].text)


asyncio.run(main())
