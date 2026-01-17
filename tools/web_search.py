from urllib.error import URLError
from urllib.request import Request, urlopen

MAX_RETRIES = 20
REQUEST_HDRS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}


def fetch_content(url):
    for _ in range(MAX_RETRIES):
        try:
            c = urlopen(Request(url, headers=REQUEST_HDRS))
            return c.read()
        except (ConnectionResetError, URLError):
            continue
    raise Exception(f"Could not open {url}")

