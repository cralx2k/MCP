from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Math & Text Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers together and returns the sum."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    return a - b


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverses the order of characters in text."""
    return text[::-1]


if __name__ == "__main__":
    mcp.run()
