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
cut = 0
max_cut = 0
#while True:

def sum_edges_between_sets(set1, set2, edges):
    total_weight = 0

    for edge in edges:
        node1, node2 = edge
        weight = 1  # Assuming an unweighted edge

        if (node1 in set1 and node2 in set2) or (node1 in set2 and node2 in set1):
            total_weight += weight

    return total_weight

X = cp.Variable((len(adj_matrix),len(adj_matrix)), symmetric = True)
constraints = [X >> 0]
constraints += [
    X[i,i] == 1 for i in range(len(adj_matrix))
    ]
objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
prob = cp.Problem(cp.Maximize(objective), constraints)
prob.solve()
while True:
    #x = sqrtm(X.value)
    u = np.random.randn(len(adj_matrix))
    x = np.sign(X.value @ u)

    # Puts all the red nodes into a set for sorting the graph
    top_nodes = [None] * len(x)
    bottom_nodes = [None] * len(x)

    for i in range(len(x)):
        if x[i]==1:
            top_nodes[i] = i
        else:
            bottom_nodes[i] = i

            
    cut = sum_edges_between_sets(top_nodes, bottom_nodes, edges)
    if cut > max_cut:
        print("A new max-cut of " + str(cut) + " has been found")
        max_cut = cut
        correct = 1
    elif cut == max_cut:
        print("The previous max-cut of " + str(cut) + " has been found again")
        correct += 1
    else:
        print("This cut of " + str(cut) + " isn't bigger than the current max-cut of " + str(max_cut))

    accuracy = correct/loop * 100
    if correct == 1:
        print("The Current Maximum has been found " + str(correct) + " time")
    else:
        print("The Current Maximum has been found " + str(correct) + " times")
    print("Current Accuracy is " + str(accuracy) + "%")    
    print("Current Loop is " + str(loop))
    loop +=1
    


