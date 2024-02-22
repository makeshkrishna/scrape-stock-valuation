import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of Wikipedia URLs to scrape
wiki_urls = [
    'https://en.wikipedia.org/wiki/Python_(programming_language)',
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://en.wikipedia.org/wiki/Machine_learning',
    # Add more Wikipedia URLs as needed
]

# List of proxy servers (replace with your own list)
proxy_list = [
'188.166.17.18:8881',
'98.162.25.7:31653',
]

def make_request_with_proxy(url, proxy):
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url} with proxy {proxy}: {e}")
        return None
    

def scrape_title(url, proxy):
    html_content = make_request_with_proxy(url, proxy)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'N/A'
        print(f"Title from {url}: {title}")
        return title
    else:
        return None

def main():
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Using ThreadPoolExecutor for concurrent execution of tasks
        futures = [executor.submit(scrape_title, url, proxy) for url in wiki_urls for proxy in proxy_list]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    print("\nAll Titles:")
    for title in results:
        print(title)

if __name__ == "__main__":
    main()
