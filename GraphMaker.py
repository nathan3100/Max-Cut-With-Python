import numpy as np

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
matrix_size = int(input("How big should the matrix be? "))
max_edge_count = int(input("And how many edges? "))

# Generate and print the adjacency matrix with commas between values and each row starting with [ and ending with ]
adj_matrix = generate_adjacency_matrix(matrix_size, max_edge_count)
for row in adj_matrix:
    print("[", ", ".join(map(str, row)), "],")
