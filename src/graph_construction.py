import json
import networkx as nx
import matplotlib.pyplot as plt
import logging
import os

# Creating a logging object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DockerBuildFailedException(Exception):
    pass

def load_data(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logger.error(f"Data file '{file_path}' not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from '{file_path}'.")
        raise

def create_graph(data: dict) -> nx.DiGraph:
    G = nx.DiGraph()
    for article, links in data.items():
        G.add_node(article)
        for link in links:
            G.add_edge(article, link)
    return G

def calculate_centrality(G: nx.DiGraph) -> dict:
    try:
        centrality = nx.degree_centrality(G)
        return centrality
    except (nx.NetworkXError, nx.NetworkXPointlessConcept) as e:
        logger.error(f"Failed to calculate centrality: {e}")
        raise

def find_shortest_path(G: nx.DiGraph, source: str, target: str) -> list:
    if source not in G or target not in G:
        logger.error(f"Either '{source}' or '{target}' not present in the graph.")
        return []

    try:
        return nx.shortest_path(G, source=source, target=target)
    except nx.NetworkXNoPath:
        logger.warning(f"No path found between {source} and {target}.")
        return []
    except nx.NodeNotFound:
        logger.error(f"One of the nodes '{source}' or '{target}' not found in the graph.")
        return []

def visualize_graph(G: nx.DiGraph) -> None:
    try:
        plt.figure(figsize=(12, 12))
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()
    except ValueError as e:
        logger.warning(f"Error while visualizing the graph: {e}")

def save_graph(G: nx.DiGraph, file_path: str) -> None:
    try:
        nx.write_graphml(G, file_path)
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Failed to save graph to '{file_path}': {e}")
        raise

def visualize_and_save_graph(G: nx.DiGraph, layout: str, file_path: str) -> None:
    plt.figure(figsize=(12, 12))
    
    if layout == "spring":
        pos = nx.spring_layout(G)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "shell":
        # Example shells. Adjust as needed.
        shells = [list(G.nodes())[x:x+50] for x in range(0, len(G.nodes()), 50)]
        pos = nx.shell_layout(G, shells)
    else:
        logger.warning(f"Unknown layout '{layout}'. Defaulting to spring layout.")
        pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.savefig(file_path, format="PDF")
    plt.close()

if __name__ == "__main__":
    print("working...")
    cleaned_links_path = '/GraphTheoryProject/Wiki-Relations/cleaned_wiki_links.json'
    data = load_data(cleaned_links_path)
    graph = create_graph(data)
    centrality = calculate_centrality(graph)
    source_article = "Graph theory"
    target_article = "Entropy (information theory)"
    shortest_path = find_shortest_path(graph, source_article, target_article)
    visualize_graph(graph)
    save_graph(graph, "wiki_graph.graphml")

    cwd = os.getcwd()

    # Visualize and save using different layouts
    layouts = ["spring", "circular", "kamada_kawai", "shell"]
    for layout in layouts:
        file_path = os.path.join(cwd, f"wiki_graph_{layout}.pdf")
        visualize_and_save_graph(graph, layout, file_path)