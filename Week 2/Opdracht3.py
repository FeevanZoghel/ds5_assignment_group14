import networkx as nx
import matplotlib.pyplot as plt
import random
import math as m


def calculate_probabilities(G: nx.Graph) -> list:
    """
    Bereken de selectiekans van iedere node op basis van zijn degree.

    Een node met meer verbindingen krijgt een grotere kans om geselecteerd
    te worden. De kansen staan in dezelfde volgorde als ``G.nodes()``.

    Args:
        G: De graaf waarvoor de selectiekansen worden berekend.

    Returns:
        Een lijst met kansen, waarvan de som 1 is.

    Author:
        Matthijs
    """

    total_degree = sum(G.degree(node) for node in G.nodes())

    return [
        G.degree(node) / total_degree
        for node in G.nodes()
    ]


def create_network(k : int, N: int, M: int) -> nx.Graph:
    """
    Maak een ongerichte Barabási-Albert-graaf zonder graph generator.

    Args:
        k: Het aantal nodes dat in de start-star met node 1 wordt verbonden.
        N: Het totale aantal nodes in de uiteindelijke graaf.
        M: Het aantal bestaande nodes waaraan iedere nieuwe node wordt
            verbonden.

    Returns:
        De gegenereerde ongerichte graaf.

    Author:
        Matthijs
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

    # Controleer of er geen self-loop is ontstaan.
    for node in G.nodes():
        if G.has_edge(node, node):
            print(f"Self-loop gevonden bij node {node}")

    return G


def visualize_network(G: nx.Graph) -> None:
    """
    Visualiseer de graaf met grootte en kleur gebaseerd op de degree.

    Args:
        G: Een graaf die door ``create_network`` is gemaakt.

    Returns:
        None. De visualisatie wordt in een matplotlib-venster getoond.

    Author:
        Matthijs
    """
    N = len(G.nodes())
    sizes  = []
    colors = []

    for node in G.nodes():
        sizes.append(10*m.exp(-N/1000)*G.degree(node))
        colors.append(G.degree(node))

    plt.figure(figsize=(18, 14))
    pos = nx.spring_layout(G)
    nodes_plot = nx.draw_networkx_nodes(G,pos,node_size=sizes,node_color=colors,cmap="seismic")
    nx.draw_networkx_edges(G,pos, width = 0.3)
    plt.colorbar(nodes_plot)
    
    plt.show()

G = create_network(5, 400, 4)
visualize_network(G)