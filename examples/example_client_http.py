import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def main():
    async with client:
        tools = await client.list_tools()
        # tools -> list[mcp.types.Tool]
        # print(tools)
        for tool in tools:
            print(f"Tool: {tool.name}")
            # print(f"Description: {tool.description}")
            # if tool.inputSchema:
            #     print(f"Parameters: {tool.inputSchema}")
            # # Access tags and other metadata
            # if hasattr(tool, 'meta') and tool.meta:
            #     fastmcp_meta = tool.meta.get('_fastmcp', {})
            #     print(f"Tags: {fastmcp_meta.get('tags', [])}")
        
        result = await client.call_tool("textprep.expand_contraction", {"input_text": "The must've SSN is 859-98-0987. The employee's phone number is 555-555-5555."})
        print("Result:", result)

asyncio.run(main())