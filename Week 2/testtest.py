print('hoi')

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


def calculate_probabilities(G: nx.Graph) -> list:
    """
    Berekent de kans dat elke node wordt geselecteerd
    op basis van de degree van die node.

    Fee
    """
    
    total_degree = 0

    for node in G.nodes():
        total_degree += G.degree(node)

    probabilities = []

    for node in G.nodes():
        probability = G.degree(node) / total_degree
        probabilities.append(probability)

    return probabilities


def create_network(k : int, N: int, M: int) -> nx.Graph:
    """
    Maakt een Barabási-Albert-netwerk.


    Parameters:
        n: Het totale aantal nodes.
        m: Het aantal verbindingen voor elke nieuwe node.

    Return:
    Het gegenereerde netwerk.

    Fee
    """
    G = nx.Graph()

    for node in range(2, k+1):
        G.add_edge(1, node)


    for new_node in range(k+1, N+1):

        nodes = list(G.nodes())

        probabilities = calculate_probabilities(G)

        chosen_nodes = []

        while len(chosen_nodes) < M:

            chosen_node = random.choices(nodes,weights=probabilities,k=1)[0]

            if chosen_node not in chosen_nodes:
                chosen_nodes.append(chosen_node)

        G.add_node(new_node)

        for chosen_node in chosen_nodes:
            G.add_edge(new_node, chosen_node)

    return G

G = create_network(5, 20, 2)


import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

pagerank = nx.pagerank(G)

sorted_pagerank = sorted(
    pagerank.items(),
    key=lambda x: x[1],
    reverse=True
)

hoogste = sorted_pagerank[0][1]

x = [0]
y = [0]
values = [hoogste]

for node, value in sorted_pagerank[1:]:

    verhouding = value / hoogste
    r = 1 - verhouding

    x.append(np.random.uniform(-r, r))
    y.append(np.random.uniform(-r, r))
    values.append(value)

sizes = [value * 10000 for value in values]

# Strepen tussen alle websites
for i in range(len(x)):
    for j in range(i + 1, len(x)):
        plt.plot(
            [x[i], x[j]],
            [y[i], y[j]],
            alpha=0.05,
            linewidth=0.5
        )

# Websites
plt.scatter(
    x,
    y,
    s=sizes,
    c=values,
    cmap='Blues'
)

plt.colorbar(label='PageRank')
plt.axis('equal')
plt.axis('off')
plt.show()