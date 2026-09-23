print('hoi')

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math as m


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

    for node in range(2, k+2):
        G.add_edge(1, node)


    for new_node in range(k+2, N+1):

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

    # controleren op een self loop
    for node in G.nodes():

        if G.has_edge(node, node):

            print(f"Self-loop gevonden bij node {node}")


    return G






def visualize_network(G):
    '''
    Visualiseert een Barabási-Albert-netwerk met een kleuren indicator en de size die is aangepast.

    Parameters: 
        G = Barabási-Albert-netwerk gemaakt met def create_network.

    Return: 
        Een plot van de Barabási-Albert-netwerk

    Matthijs
    '''
    N = len(G.nodes())
    sizes  = []
    colors = []
    nodes = []


    for node in G.nodes():
        sizes.append(10*m.exp(-N/1000)*G.degree(node))
        colors.append(G.degree(node))
        nodes.append(node)
    
    plt.figure(figsize=(18, 14))
    pos = nx.spring_layout(G)
    nodes_plot = nx.draw_networkx_nodes(G,pos,node_size=sizes,node_color=colors,cmap="seismic")
    nx.draw_networkx_edges(G,pos, width = 0.3)
    plt.colorbar(nodes_plot)
    
    return plt.show()



G = create_network(5, 400, 4)
visualize_network(G)