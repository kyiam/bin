#example

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

dist = [[0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]]

exlst = np.array([0, 1, 0, 0, 0, 1, 1, 0, 0])
exlst = exlst.reshape(3,3)
#print(exlst)

G = nx.DiGraph()

for i in range(len(exlst)):
    tmp = np.where(exlst[i]==1)[0][0]
    G.add_edge(i, tmp)
    G.edges[i, tmp]['weight'] = dist[i][tmp]

edge_labels = {}
for a,b in G.edges:
    edge_labels[a, b] = dist[a][b]
print(edge_labels)

pos = nx.spring_layout(G, 0.5, weight='weight')
nx.draw_networkx(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
