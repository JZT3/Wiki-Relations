

def collect_links(site, article_title, visited_articles, links, depth=2):
    """
    Recursively collect links from a given Wikipedia article up to a specified depth.
    """
    if depth == 0 or article_title in visited_articles:
        return

    visited_articles.add(article_title)
    page = site.pages[article_title]

    # Only consider pages in the main namespace (i.e., actual articles)
    if page.namespace == 0:
        linked_articles = [link.name for link in page.links()]
        links[article_title] = linked_articles

        # Recursively fetch links from linked articles
        for linked_article in linked_articles:
            collect_links(site, linked_article, visited_articles, links, depth-1)


def main():
    # Connect to Wikipedia
    site = mwclient.Site('en.wikipedia.org')

    # List of initial "seed" articles for math and computer science
    seed_articles = ['Mathematics', 'Computer_Science']

    # Set to store visited articles to avoid loops
    visited_articles = set()

    # Dictionary to store links between articles
    links = {}

    # Start data collection from seed articles
    for seed in seed_articles:
        collect_links(site, seed, visited_articles, links)

    # Save links to a JSON file
    with open('wikipedia_links.json', 'w') as f:
        json.dump(links, f)

    print(f"Collected data for {len(visited_articles)} articles.")

if __name__ == "__main__":
    main()
