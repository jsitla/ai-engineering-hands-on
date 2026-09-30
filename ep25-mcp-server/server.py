"""
Episode 25 - our shop tools as an MCP server.
Any app that speaks MCP (the Model Context Protocol) can now use them.
Apps start it themselves; you don't run it by hand.
"""
from mcp.server.fastmcp import FastMCP

import shop_tools

mcp = FastMCP("northwind-home")


@mcp.tool()
def get_orders() -> dict:
    """All orders of the current customer, with date, items, total and shipping in euros."""
    return shop_tools.ORDERS


@mcp.tool()
def order_details(order_id: str) -> dict:
    """Details of ONE order, by its order number (like A-1003): date, items, total and shipping in euros."""
    return shop_tools.get_order(order_id)


@mcp.tool()
def search_handbook(question: str) -> str:
    """The most relevant paragraph of the Northwind Home customer handbook."""
    return shop_tools.search_handbook(question)


if __name__ == "__main__":
    mcp.run()  # talks over standard input/output
