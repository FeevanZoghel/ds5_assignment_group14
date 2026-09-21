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
        k: Het aantal verbindingen voor de 1e node.
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

nx.draw(G, with_labels=True)
plt.show()