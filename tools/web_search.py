import os
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from core.config import settings

# Inject the Tavily API key from the central config into the environment
# as LangChain's Tavily tool reads directly from os.environ
if settings.tavily_api_key:
    os.environ["TAVILY_API_KEY"] = settings.tavily_api_key

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the internet.")

@tool("web_search", args_schema=WebSearchInput)
def web_search(query: str) -> str:
    """Useful for answering questions about current events, recent news, or fetching live information from the web.
    If the agent's internal memory does not have the answer, always use this tool to search the internet.
    """
    if not settings.tavily_api_key:
        return "Error: TAVILY_API_KEY is not configured in the .env file. Web search is unavailable."
    
    try:
        # Initialize the LangChain Tavily wrapper (fetching top 3 results)
        tavily_tool = TavilySearchResults(max_results=3)
        results = tavily_tool.invoke({"query": query})
        return str(results)
    except Exception as e:
        return f"Web search failed: {str(e)}"
