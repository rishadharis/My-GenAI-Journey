from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir.parent / '.env'

load_dotenv(dotenv_path)

tavily_api_key = os.getenv("TAVILY_API_KEY")
# print(tavily_api_key)

def get_url_profile_tavily(name: str):
    """Searches for LinkedIn Profile Page."""
    search = TavilySearchResults(tavily_api_key=tavily_api_key)
    res = search.run(f"{name}")

    return res
