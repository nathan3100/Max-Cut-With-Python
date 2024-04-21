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

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import sqrtm
import time
file_path = "previous_values.txt"
loop = 1
cuts = []
clicked_node = None
initial_pos = None
fig_cut = {}
fig_simplified = {}
pos_cut = {}
pos_simplified = {}
line = ''

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
            if x[i] == (1):
                file.write(" 1. ,")
            elif x[i] == (-1):
                file.write("-1. ,")
        if x[len(x)-1] == (1):
            file.write(" 1. ")
        elif x[len(x)-1] == (-1):
            file.write("-1. ")
        file.write("] \n")

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
            nx.draw(graph, positions, with_labels=True, labels={i: i+1 for i in graph.nodes}, node_color=[node_colors[i] for i in graph.nodes], font_color='white', font_weight='bold')
            nx.draw_networkx_edges(graph, positions, edgelist=edges, edge_color='green')
            nx.draw_networkx_edges(graph, positions, edgelist=orange_edges, edge_color='orange')
            plt.draw()
            
# Function to handle node movement on click
def on_click(event, pos):
    global clicked_node, initial_pos
    if event.inaxes:
        x, y = event.xdata, event.ydata
        for node in G.nodes:
            pos_x, pos_y = pos[node]
            dist = (pos_x - x) ** 2 + (pos_y - y) ** 2
            if dist < 0.001:  # Adjust this threshold as needed
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

# Function to handle mouse click for simplified graph
def on_click_simplified(event):
    on_click(event, pos_simplified)
    

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
line = input("Which line of text should I draw? (1 - " + str(len(previous_values)) + ") ")
if int(line) > 0 and int(line) <= len(previous_values):
    orange_edges = []
    x = previous_values[int(line) - 1]

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

    # Make a new graph window
    plt.figure(str(line) + ' Sorted: ' + str(cut[0]))

    # Define the position of nodes for the 3x3 grid
    #pos = {0: (0, 2), 1: (1, 2), 2: (2, 2), 3: (0, 1), 4: (2, 1), 5: (0, 0), 6: (1, 0), 7: (2, 0)}

    # Draw the graph
    pos_cut = nx.bipartite_layout(G, top_nodes, align='horizontal') 
    nx.draw(G, pos_cut, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')
    nx.draw_networkx_edges(G, pos_cut, edgelist=edges, edge_color='green')
    nx.draw_networkx_edges(G, pos_cut, edgelist=orange_edges, edge_color='orange')

    # 2nd window
    plt.figure(str(line) + ': ' + str(cut[0]))
    pos_simplified = {0: (0, 2), 1: (1, 2), 2: (2, 2), 3: (0, 1), 4: (2, 1), 5: (0, 0), 6: (1, 0), 7: (2, 0)}
    nx.draw(G, pos_simplified, with_labels=True, labels={i: i+1 for i in G.nodes}, node_color=[node_colors[i] for i in G.nodes], font_color='white', font_weight='bold')
    nx.draw_networkx_edges(G, pos_simplified, edgelist=edges, edge_color='green')
    nx.draw_networkx_edges(G, pos_simplified, edgelist=orange_edges, edge_color='orange')

    fig_cut = plt.figure(str(line) + ' Sorted: ' + str(cut[0]))
    fig_cut.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, G, pos_cut))
    fig_cut.canvas.mpl_connect('button_press_event', on_click_cut)
    fig_cut.canvas.mpl_connect('button_release_event', on_release)

    fig_simplified = plt.figure(str(line) + ': ' + str(cut[0]))
    fig_simplified.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, G, pos_simplified))
    fig_simplified.canvas.mpl_connect('button_press_event', on_click_simplified)
    fig_simplified.canvas.mpl_connect('button_release_event', on_release)


    # Show the plot
    print("Displaying graph " + line + " from file " + file_path + " with a cut of " + str(cut[0]))
    plt.show()
else:
    print("Invalid Line Selection")
