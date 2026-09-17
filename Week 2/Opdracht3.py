print('hoi')

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_edges_from([
    (1, 2),
    (1, 4),
    (2, 3),
    (3, 5)
])

nx.draw(G, with_labels=True)
plt.show()
