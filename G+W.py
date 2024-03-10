adj_matrix = [
    [0, 1, 0, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0]
]

edges = []

# Iterate through the adjacency matrix and add edges to the list
for i in range(len(adj_matrix)):
    for j in range(i + 1, len(adj_matrix[i])):
        if adj_matrix[i][j] == 1:
            edges.append((i, j))  

print(edges)
#print(len(edges))

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import sqrtm
loop = 1
correct = 0
reference_value = np.array([-1. + 0.j, -1. + 0.j,  1. + 0.j,  1. + 0.j,  1. + 0.j, -1. + 0.j,  1. + 0.j, -1. + 0.j])
reference_value2 = np.array([ 1. + 0.j,  1. + 0.j, -1. + 0.j, -1. + 0.j, -1. + 0.j,  1. + 0.j, -1. + 0.j,  1. + 0.j])
while True:
    X = cp.Variable((8,8), symmetric = True)
    constraints = [X >> 0]
    constraints += [
        X[i,i] == 1 for i in range(len(adj_matrix))
        ]
    objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
    prob = cp.Problem(cp.Maximize(objective), constraints)
    prob.solve()
    print(X)
    input("")
    x = sqrtm(X.value)
    print(x)
    input("")
    u = np.random.randn(len(adj_matrix))
    x = np.sign(x @ u)
    print(u)
    print(x)

    # Create a graph
    G = nx.Graph()

    # Add nodes and edges to the graph
    for i in range(len(adj_matrix)):
        G.add_node(i)

    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)

    # Create a dictionary to map node indices to colors based on the output data
    node_colors = {i: 'red' if x[i] == 1 else 'blue' for i in range(len(x))}

    # Define the position of nodes for the 3x3 grid
    pos = {0: (0, 2), 1: (1, 2), 2: (2, 2), 3: (0, 1), 4: (2, 1), 5: (0, 0), 6: (1, 0), 7: (2, 0)}

    # Draw the graph
    #pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')

    # Show the plot
    plt.show()

