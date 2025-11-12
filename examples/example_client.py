# examples/example_client.py
from fastmcp.client.transports import StdioTransport
from fastmcp import Client
import asyncio

transport = StdioTransport(
    command="python",
    args=["mhlabs-mcp-tools"],
)
client = Client(transport)

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        # tools = await client.list_tools()
        # resources = await client.list_resources()
        # prompts = await client.list_prompts()
        
        # Execute operations
        result = await client.call_tool("textprep.remove_email", {"input_text": "Contact me at test@mail.com"})
        print(result)

asyncio.run(main())

