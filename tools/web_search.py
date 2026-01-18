import os
import requests
import json
from logger import log

def web_search(query: str) -> str:
    """
    Performs a Google Search via Serper.dev.
    Returns a formatted string of snippets that the agent can read.
    """
    # 1. Configuration
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "ERROR: SERPER_API_KEY environment variable not set."

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": 5})
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    log("WEB SEARCH", f"Searching for: '{query}'", True)

    try:
        # 2. Make the API Call
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        search_results = response.json()

        # 3. Parse and Format the results
        # We focus on 'organic' results which contain the snippets
        organic_results = search_results.get("organic", [])
        
        if not organic_results:
            return f"No search results found for: '{query}'"

        formatted_output = ["### SEARCH RESULTS ###"]
        
        for i, result in enumerate(organic_results, 1):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No snippet available.")
            link = result.get("link", "No link available.")
            
            # This structured format helps the LLM recognize facts immediately
            formatted_output.append(f"{i}. {title}")
            formatted_output.append(f"   Snippet: {snippet}")
            formatted_output.append(f"   Source: {link}\n")

        log('WEB SEARCH', formatted_output, True)
        return "\n".join(formatted_output)

    except requests.exceptions.RequestException as e:
        return f"TOOL ERROR: The search API failed with the following error: {str(e)}"
