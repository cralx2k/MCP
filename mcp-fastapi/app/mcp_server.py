import httpx
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

BASE_URL = "http://localhost:8000"

server = Server("fastapi-mcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_items",
            description="List all items",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_item",
            description="Get a single item by ID",
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "integer"}},
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="create_item",
            description="Create a new item",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["name", "description"],
            },
        ),
        types.Tool(
            name="clone_item",
            description="Clone an existing item by ID",
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "integer"}},
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="delete_item",
            description="Delete an existing item by ID",
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "integer"}},
                "required": ["item_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    async with httpx.AsyncClient() as client:
        if name == "list_items":
            r = await client.get(f"{BASE_URL}/items")
        elif name == "get_item":
            r = await client.get(f"{BASE_URL}/items/{arguments['item_id']}")
        elif name == "create_item":
            r = await client.post(f"{BASE_URL}/items", json=arguments)
        elif name == "clone_item":
            r = await client.post(f"{BASE_URL}/items/{arguments['item_id']}/clone")
        elif name == "delete_item":
            r = await client.delete(f"{BASE_URL}/items/{arguments['item_id']}")
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    return [types.TextContent(type="text", text=r.text)]


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
