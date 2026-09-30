"""
Episode 25 - app number two: our AI agent, using the tools through MCP instead of importing them.
It asks the server which tools exist, and turns them into tool descriptions for the model.
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from llm import MODEL, get_client

client = get_client()
SERVER = StdioServerParameters(command="python", args=["server.py"])
SYSTEM = """You help a logged-in customer of Northwind Home.
For questions about their orders, call get_orders (it needs no arguments). For the shop's rules, call search_handbook.
Answer briefly, only from tool results, in euros."""


async def main(task):
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            specs = [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.inputSchema}} for t in tools]
            messages = [{"role": "system", "content": SYSTEM},
                        {"role": "user", "content": task}]
            print(f"TASK: {task}")
            for step in range(1, 7):
                msg = client.chat.completions.create(model=MODEL, messages=messages, tools=specs, temperature=0).choices[0].message
                if not msg.tool_calls:
                    print(f"step {step}: FINAL ANSWER: {msg.content}")
                    return
                messages.append(msg)
                for i, call in enumerate(msg.tool_calls):
                    args = json.loads(call.function.arguments or "{}")
                    if i > 0:                                                    # one tool per step (episode 24)
                        text = "not run: call one tool at a time, and use its result first"
                    else:
                        result = await session.call_tool(call.function.name, args)   # the SERVER runs it
                        text = result.content[0].text if result.content else ""
                    print(f"step {step}: [mcp] {call.function.name}({args}) -> {text[:80]}")
                    messages.append({"role": "tool", "tool_call_id": call.id, "content": text})


asyncio.run(main("What did I order on 5 September, and how much was the shipping?"))
