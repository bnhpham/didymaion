from tavily import TavilyClient
from dotenv import load_dotenv
import os


# Load environment variables from a .env file
load_dotenv()

# Entry point to interacting with the Tavily API
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# Return top 5 most relevant web search results for the user's query
def search_web(query: str) -> dict:
    response = client.search(query=query, max_results=5)

    formatted = []
    sources = []

    for result in response["results"]:
        formatted.append(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Content: {result['content']}" # short content snippet
            )
        sources.append(result["url"])

    return {
        "text": "\n\n".join(formatted),
        "sources": sources,
        }