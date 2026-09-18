import networkx as nx
import matplotlib.pyplot as plt
import random


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


def create_network(n: int, m: int) -> nx.Graph:
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

    G.add_edges_from([
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5)
    ])

    for new_node in range(6, n + 1):

        nodes = list(G.nodes())

        probabilities = calculate_probabilities(G)

        chosen_nodes = []

        while len(chosen_nodes) < m:

            chosen_node = random.choices(nodes,weights=probabilities,k=1)[0]

            if chosen_node not in chosen_nodes:
                chosen_nodes.append(chosen_node)

        G.add_node(new_node)

        for chosen_node in chosen_nodes:
            G.add_edge(new_node, chosen_node)

    return G

G = create_network(20, 2)

nx.draw(G, with_labels=True)
plt.show()