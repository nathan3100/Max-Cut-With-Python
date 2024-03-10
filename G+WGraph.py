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

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import sqrtm
import time
file_path = "previous_values.txt"

def read_previous_values(file_path):
    try:
        with open(file_path, 'r') as file:
            previous_values = [np.array(eval(line)) for line in file.readlines()]
        return previous_values
    except FileNotFoundError:
        print("File Not Found")
        return []

def write_previous_value(file_path, x):
    with open(file_path, 'a') as file:
        file.write("[")
        for i in range (len(x)-1):
            if x[i] == (1+0j):
                file.write(" 1. + 0.j, ")
            elif x[i] == (-1+0j):
                file.write("-1. + 0.j, ")
        if x[len(x)-1] == (1+0j):
            file.write(" 1. + 0.j")
        elif x[len(x)-1] == (-1+0j):
            file.write("-1. + 0.j")
        file.write("] \n")

# Create a graph
G = nx.Graph()

# Add nodes and edges to the graph
for i in range(len(adj_matrix)):
    G.add_node(i)

for i in range(len(adj_matrix)):
    for j in range(i + 1, len(adj_matrix[i])):
        if adj_matrix[i][j] == 1:
            G.add_edge(i, j)
            
previous_values = read_previous_values(file_path)
for x in previous_values:
    # Create a dictionary to map node indices to colors based on the output data
    node_colors = {i: 'red' if x[i] == 1 else 'blue' for i in range(len(x))}

    # Define the position of nodes for the 3x3 grid
    pos = {0: (0, 2), 1: (1, 2), 2: (2, 2), 3: (0, 1), 4: (2, 1), 5: (0, 0), 6: (1, 0), 7: (2, 0)}

    # Draw the graph
    #pos = nx.spring_layout(G)  # You can choose a different layout if needed
    nx.draw(G, pos, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')

    # Show the plot
    plt.show()
