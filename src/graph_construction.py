import json
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

cleaned_links_path = './cleaned_wiki_links.json'
with open(cleaned_links_path, 'r') as f:
    data = json.load(f)

G = nx.DiGraph()

for article, links in data.items():
    G.add_node(article)
    for link in links:
        G.add_edge(article, link)

centrality = nx.degree_centrality(G)
communities_generator = community.girvan_newman(G)

shortest_path = nx.shortest_path(G, source="Source_Article", target="Target_Article")



plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

# Save as GraphML format
nx.write_graphml(G, "wiki_graph.graphml")
