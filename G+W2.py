adj_matrix = [
     [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
     [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
     [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
     [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
     [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0],
     [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
     [1, 1 ,0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1],
     [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
     [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
     [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
     [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
     [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1],
     [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
     [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
     [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
     [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
]



edges = []

# Iterate through the adjacency matrix and add edges to the list
for i in range(len(adj_matrix)):
    for j in range(i + 1, len(adj_matrix[i])):
        if adj_matrix[i][j] == 1:
            edges.append((i, j))  

#print(edges)
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

def sum_edges_between_sets(set1, set2, edges):
    total_weight = 0

    for edge in edges:
        if len(edge) == 3:
            node1, node2, weight = edge
        elif len(edge) == 2:
            node1, node2 = edge
            weight = 1  # Assuming an unweighted edge
        else:
            raise ValueError("Invalid edge format")

        if (node1 in set1 and node2 in set2) or (node1 in set2 and node2 in set1):
            total_weight += weight

    return total_weight


while True:
    X = cp.Variable((len(adj_matrix),len(adj_matrix)), symmetric = True)
    constraints = [X >> 0]
    constraints += [
        X[i,i] == 1 for i in range(len(adj_matrix))
        ]
    objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
    prob = cp.Problem(cp.Maximize(objective), constraints)
    prob.solve()
    x = sqrtm(X.value)
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

    # Puts all the red nodes into a set for sorting the graph
    top_nodes = [None] * len(x)
    bottom_nodes = [None] * len(x)

    for i in range(len(x)):
        if x[i]==1:
            top_nodes[i] = i
        else:
            bottom_nodes[i] = i

            
    cut = sum_edges_between_sets(top_nodes, bottom_nodes, edges)

    #Draw the cut graph
    plt.figure('The Cut Of ' + str(cut))
    seed_value = 42
    pos = nx.random_layout(G, seed=seed_value)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')


    # Draw the simplified cut graph
    plt.figure('Simplified View Of The Cut Of ' + str(cut))
    pos = nx.bipartite_layout(G, top_nodes, align='horizontal') # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')

    # Draw the original graph:
    plt.figure('Original Graph')
    G2 = nx.Graph()
    G2.add_edges_from(edges)
    pos = nx.random_layout(G, seed=seed_value)  # You can use different layout algorithms
    nx.draw(G2, pos, with_labels=True, labels={i: i+1 for i in G2.nodes}, font_weight='bold', node_size=500, node_color='white', font_color='black', edge_color='gray', linewidths=1, alpha=0.7)


    # Show the plot
    plt.show()


