import json
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

def load_data(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logging.error(f"Failed to load data from {file_path}. Error: {e}")
        raise

def create_graph(data: dict) -> nx.DiGraph:
    G = nx.DiGraph()
    for article, links in data.items():
        add_node(G, article)
        for link in links:
            add_edge(G, article, link)
    return G

def add_node(G: nx.DiGraph, node: str) -> None:
    G.add_node(node)

def add_edge(G: nx.DiGraph, source: str, target: str) -> None:
    G.add_edge(source, target)

def calculate_centrality(G: nx.DiGraph) -> dict:
    try:
        centrality = nx.degree_centrality(G)
        return centrality
    except Exception as e:
        logging.error(f"Failed to calculate centrality. Error: {e}")
        raise

def find_shortest_path(G: nx.DiGraph, source: str, target: str) -> list:
    try:
        shortest_path = nx.shortest_path(G, source=source, target=target)
        return shortest_path
    except nx.NetworkXNoPath:
        logging.error(f"No path found between {source} and {target}.")
        return []
    except Exception as e:
        logging.error(f"Failed to find shortest path. Error: {e}")
        raise

def visualize_graph(G: nx.DiGraph) -> None:
    try:
        plt.figure(figsize=(12, 12))
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()
    except Exception as e:
        logging.error(f"Failed to visualize graph. Error: {e}")

def save_graph(G: nx.DiGraph, file_path: str) -> None:
    try:
        nx.write_graphml(G, file_path)
        logging.info(f"Graph saved to {file_path}.")
    except Exception as e:
        logging.error(f"Failed to save graph. Error: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    cleaned_links_path = '.\cleaned_wiki_links.json'
    source_article = "Source_Article"
    target_article = "Target_Article"

    data = load_data(cleaned_links_path)
    graph = create_graph(data)
    centrality = calculate_centrality(graph)
    shortest_path = find_shortest_path(graph, source_article, target_article)
    
    if shortest_path:
        logging.info(f"Shortest path from {source_article} to {target_article}: {' -> '.join(shortest_path)}")
    
    visualize_graph(graph)
    save_graph(graph, "wiki_graph.graphml")
