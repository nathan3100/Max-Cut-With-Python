adj_matrix = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
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
from math import sqrt
loop = 1
correct = 0
reference_value = np.array([-1. + 0.j, -1. + 0.j,  1. + 0.j,  1. + 0.j,  1. + 0.j, -1. + 0.j,  1. + 0.j, -1. + 0.j])
reference_value2 = np.array([ 1. + 0.j,  1. + 0.j, -1. + 0.j, -1. + 0.j, -1. + 0.j,  1. + 0.j, -1. + 0.j,  1. + 0.j])

X = cp.Variable((len(adj_matrix),len(adj_matrix)), symmetric = True)
constraints = [X >> 0]
constraints += [
    X[i,i] == 1 for i in range(len(adj_matrix))
    ]
objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
prob = cp.Problem(cp.Maximize(objective), constraints)
prob.solve()
#print('Big X: ')
#for i in range(8):
#    for j in range(8):
#        print(str(i) + ',' + str(j) + ': ' + str(X[i,j].value))
#print(X)
#input("")

#x = sqrtm(X.value)

#print('Little x: ')
#for i in range(8):
#    for j in range(8):
#        print(str(i) + ',' + str(j) + ': ' + str(x[i,j]))
#print(x)
#input("")
unit = 0
'''
for i in range(8):
    unit += x[0,i].real * x[0,i].real
print(unit)
unit = 0
for i in range(8):
    unit += x[0,i].imag * x[0,i].imag
print(unit)

for k in range(8):
    unit = 0
    for i in range(8):
        unit += (x[k,i].real * x[k,i].real + x[k,i].imag * x[k,i].imag)
    print(unit)
#print(sqrt(unit))
'''
print(X.value)
u = np.random.randn(len(adj_matrix))
x = np.sign(X.value @ u)
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
#pos = {0: (0, 2), 1: (1, 2), 2: (2, 2), 3: (0, 1), 4: (2, 1), 5: (0, 0), 6: (1, 0), 7: (2, 0)}

# Draw the graph
pos = nx.spring_layout(G)  # You can choose a different layout if needed
nx.draw(G, pos, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')

# Show the plot
plt.show()

