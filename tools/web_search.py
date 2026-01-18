import urllib.parse
from urllib.error import URLError
from urllib.request import Request, urlopen
import trafilatura

MAX_RETRIES = 5 
REQUEST_HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive'
}

def is_valid_url(url):
    """Checks if the string has a valid protocol/scheme."""
    parsed = urllib.parse.urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def web_search(query_or_url):
    target_url = query_or_url
    
    # 1. If it's not a URL, format it as a Google Search
    if not is_valid_url(query_or_url):
        print(f"Input is not a URL. Searching Google for: {query_or_url}")
        encoded_query = urllib.parse.quote_plus(query_or_url)
        target_url = f"https://www.google.com/search?q={encoded_query}"

    # 2. Attempt to fetch
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(target_url, headers=REQUEST_HDRS)
            with urlopen(req, timeout=10) as response:
                return trafilatura.extract(response.read())
        except (ConnectionResetError, URLError, Exception) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                # 3. Final Fallback: If URL fetch failed, try searching it on Google anyway
                if target_url == query_or_url:
                    print("URL fetch failed. Retrying as Google Search...")
                    return web_search(f"https://www.google.com/search?q={urllib.parse.quote_plus(query_or_url)}")
                
    raise Exception(f"Could not process request for: {query_or_url}")
