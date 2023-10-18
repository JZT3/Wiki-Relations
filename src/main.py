import json
import mwclient
import concurrent.futures
from collections import defaultdict, deque

def worker(d, site, visited_articles, links_lock, links, depth, visited_lock):
    while d:
        article_title, current_depth = d.popleft()
        
        with visited_lock:
            if current_depth > depth or article_title in visited_articles:
                continue
            visited_articles.add(article_title)
        
        page = site.pages[article_title]

        if page.namespace == 0:
            linked_articles = [link.name for link in page.links()]

            with links_lock:
                links[article_title].extend(linked_articles)

            for linked_article in linked_articles:
                d.append((linked_article, current_depth + 1))

def collect_links_multithreaded(site, seed_articles, depth=2):
    links = defaultdict(list)
    d = deque((article, 1) for article in seed_articles)
    visited_articles = set()
    links_lock = concurrent.futures.Lock()
    visited_lock = concurrent.futures.Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, d, site, visited_articles, links_lock, links, depth, visited_lock) for _ in range(10)]
        concurrent.futures.wait(futures)
    
    return links

def main():
    site = mwclient.Site('en.wikipedia.org')
    seed_articles = ['Mathematics', 'Computer_Science']
    links = collect_links_multithreaded(site, seed_articles)

    with open('wikipedia_links.json', 'w') as f:
        json.dump(links, f)

    print(f"Collected data for {len(links)} articles.")

if __name__ == "__main__":
    main()
