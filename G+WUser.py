
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
edges = []
orange_edges = []
coloured = ''

# Function to create an adjacency matrix with 50 edges for a 20-node graph
def generate_adjacency_matrix(matrix_size, max_edge_count):

  # Initialize a 20x20 matrix with zeros
  adj_matrix = np.zeros((matrix_size, matrix_size), dtype=int)

  # Counter for the number of edges added
  edge_count = 0

  # Loop until 50 edges are added
  while edge_count < max_edge_count:
    # Generate random indices for two nodes
    node1 = np.random.randint(0, matrix_size)
    node2 = np.random.randint(0, matrix_size)

    # Ensure nodes are different and the edge doesn't already exist
    if node1 != node2 and adj_matrix[node1][node2] == 0:
      # Add the edge to the matrix (symmetrically for an undirected graph)
      adj_matrix[node1][node2] = 1
      adj_matrix[node2][node1] = 1
      edge_count += 1

  return adj_matrix

# Get user input for matrix size and edge count
matrix_size = int(input("How many nodes on the graph? "))
max_edge_count = int(input("And how many edges? "))
adj_matrix = generate_adjacency_matrix(matrix_size, max_edge_count)
coloured = input("Should the edges be coloured? (y/n) ")
while coloured.lower() != 'y' and coloured.lower() != 'n':
  print("Invalid Input, should be \'y\' or \'n\'")
  coloured = input("Should the edges be coloured? (y/n) ")


# Iterate through the adjacency matrix and add edges to the list
for i in range(len(adj_matrix)):
    for j in range(i + 1, len(adj_matrix[i])):
        if adj_matrix[i][j] == 1:
            edges.append((i, j))  

#while True:

def sum_edges_between_sets(set1, set2, edges):
    total_weight = 0

    for edge in edges:
        node1, node2 = edge
        weight = 1  # Assuming an unweighted edge

        if (node1 in set1 and node2 in set2) or (node1 in set2 and node2 in set1):
            total_weight += weight
            orange_edges.append(edge)

    return total_weight, orange_edges

# Function to handle node movement while dragging
def on_move(event, graph, positions):
    global clicked_node, initial_pos
    if event.inaxes:
        x, y = event.xdata, event.ydata
        if event.button == 1 and clicked_node is not None:  # Check if left mouse button is pressed and a node is clicked
            positions[clicked_node] = x, y
            plt.clf()
            if graph == G:
                nx.draw(graph, positions, with_labels=True, labels={i: i+1 for i in graph.nodes}, node_color=[node_colors[i] for i in graph.nodes], font_color='white', font_weight='bold')
                if coloured.lower() == 'y':
                  nx.draw_networkx_edges(graph, positions, edgelist=edges, edge_color='green')
                  nx.draw_networkx_edges(graph, positions, edgelist=orange_edges, edge_color='orange')
            elif graph == G2:
                nx.draw(graph, positions, with_labels=True, labels={i: i+1 for i in graph.nodes}, font_weight='bold', node_size=500, node_color='white', font_color='black', edge_color='gray', linewidths=1, alpha=0.7)
            plt.draw()
            
# Function to handle node movement on click
def on_click(event, pos):
    global clicked_node, initial_pos
    if event.inaxes:
        x, y = event.xdata, event.ydata
        for node in G.nodes:
            pos_x, pos_y = pos[node]
            dist = (pos_x - x) ** 2 + (pos_y - y) ** 2
            if dist < 0.0015:  # Adjust this threshold as needed
                clicked_node = node
                initial_pos = pos[node]  # Update initial_pos only when a new node is clicked
                break

# Function to handle mouse release
def on_release(event):
    global clicked_node
    clicked_node = None

# Function to handle mouse click for cut graph
def on_click_cut(event):
    on_click(event, pos_cut)

# Function to handle mouse click for original graph
def on_click_original(event):
    on_click(event, pos_original)

# Function to handle mouse click for simplified graph
def on_click_simplified(event):
    on_click(event, pos_simplified)
    

X = cp.Variable((len(adj_matrix),len(adj_matrix)), symmetric = True)
constraints = [X >> 0]
constraints += [
    X[i,i] == 1 for i in range(len(adj_matrix))
    ]
objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
prob = cp.Problem(cp.Maximize(objective), constraints)
prob.solve()
#x = sqrtm(X.value)
u = np.random.randn(len(adj_matrix))
x = np.sign(X.value @ u)
#print(u)
#print(x)

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
plt.figure('The Cut Of ' + str(cut[0]))
seed_value = 42
pos_cut = nx.random_layout(G, seed=seed_value)  # You can choose a different layout if needed
nx.draw(G, pos_cut, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')
if coloured.lower() == 'y':
  nx.draw_networkx_edges(G, pos_cut, edgelist=edges, edge_color='green')
  nx.draw_networkx_edges(G, pos_cut, edgelist=orange_edges, edge_color='orange')

# Draw the simplified cut graph
plt.figure('Simplified View Of The Cut Of ' + str(cut[0]))
pos_simplified = nx.bipartite_layout(G, top_nodes, align='horizontal') # You can choose a different layout if needed
nx.draw(G, pos_simplified, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')
if coloured.lower() == 'y':
  nx.draw_networkx_edges(G, pos_simplified, edgelist=edges, edge_color='green')
  nx.draw_networkx_edges(G, pos_simplified, edgelist=orange_edges, edge_color='orange')
    
# Show the plot
#plt.show(block=False)

# Draw the original graph:
plt.figure('Original Graph')
G2 = nx.Graph()
G2.add_edges_from(edges)
pos_original = nx.random_layout(G, seed=seed_value)  # You can use different layout algorithms
nx.draw(G2, pos_original, with_labels=True, labels={i: i+1 for i in G2.nodes}, font_weight='bold', node_size=500, node_color='white', font_color='black', edge_color='gray', linewidths=1, alpha=0.7)

fig_cut = plt.figure('The Cut Of ' + str(cut[0]))
fig_cut.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, G, pos_cut))
fig_cut.canvas.mpl_connect('button_press_event', on_click_cut)
fig_cut.canvas.mpl_connect('button_release_event', on_release)

fig_simplified = plt.figure('Simplified View Of The Cut Of ' + str(cut[0]))
fig_simplified.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, G, pos_simplified))
fig_simplified.canvas.mpl_connect('button_press_event', on_click_simplified)
fig_simplified.canvas.mpl_connect('button_release_event', on_release)

fig_original = plt.figure('Original Graph')
fig_original.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, G2, pos_original))
fig_original.canvas.mpl_connect('button_press_event', on_click_original)
fig_original.canvas.mpl_connect('button_release_event', on_release)
    
# Show the plot
plt.show()

