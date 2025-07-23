from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()
import os

mcp = FastMCP("search")

@mcp.tool()
def search_tool(query: str) -> dict:
   tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
   results =  tool.invoke(query)
   return results

if __name__ == "__main__":
    mcp.run(transport="stdio")