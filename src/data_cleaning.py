import json
from typing import Dict, List


def remove_duplicate_links(data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Removes duplicate links from the articles' links.
    """
    return {article: list(set(links)) for article, links in data.items()}


def filter_stub_articles(data: Dict[str, List[str]], threshold: int = 3) -> Dict[str, List[str]]:
    """
    Filters out articles that have links below a certain threshold.
    """
    return {article: links for article, links in data.items() if len(links) > threshold}


def remove_orphaned_articles(data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Removes articles that are not referenced by any other article.
    """
    linked_from = set(link for links in data.values() for link in links)
    return {article: links for article, links in data.items() if article in linked_from}


def remove_self_referential_links(data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Removes links from an article that point to itself.
    """
    return {article: [link for link in links if link != article] for article, links in data.items()}


def filter_redundant_articles(data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Filters out articles with "(disambiguation)" in their title.
    """
    return {article: links for article, links in data.items() if "(disambiguation)" not in article}


def clean_data(input_file_path: str, output_file_path: str) -> None:
    """
    Loads the data, cleans it, and then saves the cleaned data to a new file.
    """
    with open(input_file_path, 'r') as f:
        data = json.load(f)

    data = remove_duplicate_links(data)
    data = filter_stub_articles(data)
    data = remove_orphaned_articles(data)
    data = remove_self_referential_links(data)
    data = filter_redundant_articles(data)

    with open(output_file_path, 'w') as f:
        json.dump(data, f)




def main() -> None:
    raw_data_file = 'Z:\Graph_Theory_Project\Wiki-Relations\wikipedia_links.json'
    cleaned_data_file_path = 'Z:\Graph_Theory_Project\Wiki-Relations\cleaned_wiki_links.json'
    
    clean_data(raw_data_file, cleaned_data_file_path)




if __name__ == "__main__":
    main()
