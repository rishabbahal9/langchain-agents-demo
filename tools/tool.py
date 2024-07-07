from langchain_community.tools.tavily_search import TavilySearchResults


def crawls_google(text: str):
    """Searches for recipes based on ingredients."""
    search = TavilySearchResults()
    res = search.run(f"{text}")
    return res[0]
