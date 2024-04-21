import numpy as np
import pyperclip

# Function to create an adjacency matrix with M edges for a N-node graph
def generate_adjacency_matrix(matrix_size, max_edge_count):  
  # Initialize a NxN matrix with zeros
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
matrix_size = int(input("How big should the matrix be? "))
max_edge_count = int((matrix_size * (matrix_size-1))/2)
edge_count = int(input("And how many edges? (Max of " + str(max_edge_count) + ", 95% is " + str(max_edge_count*0.95)+ ") "))

if edge_count <= (matrix_size * (matrix_size-1))/2:
  # Generate and print the adjacency matrix with commas between values and each row starting with [ and ending with ]
  adj_matrix = generate_adjacency_matrix(matrix_size, edge_count)
  matrix_str = ""
  for i, row in enumerate(adj_matrix):
      if i == len(adj_matrix) - 1:
          matrix_str += "[" + ", ".join(map(str, row)) + "]"
      else:
          matrix_str += "[" + ", ".join(map(str, row)) + "],\n"

  print(matrix_str)
  pyperclip.copy(matrix_str)
  print("Matrix copied to clipboard!")
else:
  print("Not Enough Nodes For That Many Edges.")
