import json
import mwclient
import concurrent.futures
import threading
from collections import defaultdict, deque
from typing import List, Dict, Set

def fetch_article_links(article_queue: deque, 
                        site: mwclient.Site, 
                        visited_articles: Set[str], 
                        links_lock: threading.Lock, 
                        article_links: Dict[str, List[str]], 
                        max_depth: int, 
                        visited_lock: threading.Lock) -> None:
    """
    Worker function to fetch links of articles from Wikipedia.
    
    Args:
    - article_queue: A queue containing articles to be processed.
    - site: mwclient site object for Wikipedia.
    - visited_articles: A set to keep track of processed articles.
    - links_lock: A lock to ensure thread-safe updates to article_links.
    - article_links: Dictionary storing links for each article.
    - max_depth: Maximum depth for recursive link fetching.
    - visited_lock: A lock to ensure thread-safe updates to visited_articles.
    """
    
    while article_queue:
        try:
            article_title, current_depth = article_queue.popleft()
        except IndexError:  # Handles case when deque is empty
            break
        
        # Check if article already visited or max depth reached
        with visited_lock:
            if current_depth > max_depth or article_title in visited_articles:
                continue
            visited_articles.add(article_title)
        
        # Fetch links from the current article
        page = site.pages[article_title]
        if page.namespace == 0:  # Ensure it's an actual article
            linked_articles = [link.name for link in page.links()]

            # Update the global links dictionary
            with links_lock:
                article_links[article_title].extend(linked_articles)

            # Add linked articles to the queue for further processing
            for linked_article in linked_articles:
                article_queue.append((linked_article, current_depth + 1))

def multithreaded_link_collection(site: mwclient.Site, 
                               seed_articles: List[str], 
                               depth: int = 2) -> Dict[str, List[str]]:
    """
    Collect links from Wikipedia articles using a multithreaded approach.
    
    Args:
    - site: mwclient site object for Wikipedia.
    - seed_articles: Initial articles to start the link collection.
    - depth: Maximum depth for link fetching.

    Returns:
    - Dictionary with articles as keys and their linked articles as values.
    """
    
    article_links = defaultdict(list)
    article_queue = deque((article, 1) for article in seed_articles)
    visited_articles = set()
    links_lock = threading.Lock()
    visited_lock = threading.Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start worker threads
        futures = [executor.submit(fetch_article_links, article_queue, site, visited_articles, links_lock, article_links, depth, visited_lock) for _ in range(10)]
        concurrent.futures.wait(futures)
    
    return article_links

def saved_links(seed_articles: List[str], output_file: str = 'wikipedia_links.json') -> None:
    """Fetch and save Wikipedia article links."""
    site = mwclient.Site('en.wikipedia.org')
    links = multithreaded_link_collection(site, seed_articles)

    # Save links to a JSON file
    with open(output_file, 'w') as f:
        json.dump(links, f)

    print(f"Collected data for {len(links)} articles.")


def main() -> None:
    """Main function to fetch and save Wikipedia article links."""
    
    # Connect to Wikipedia
    site = mwclient.Site('en.wikipedia.org')
    
    # Define seed articles
    seed_articles = ['Mathematics',
                     'Computer_science' 
                    ] # user input of desired list of starting seed articles

    
    # Fetch links using a multithreaded approach
    saved_links(seed_articles)

if __name__ == "__main__":
    main()