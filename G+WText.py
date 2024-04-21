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

#print(edges)
#print(len(edges))

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import sqrtm
import time
loop = 1
correct = 0
file_path = "previous_values_new.txt"
reference_value = np.array([-1. , -1. ,  1. ,  1. ,  1. , -1. ,  1. , -1. ])
reference_value2 = np.array([ 1. ,  1. , -1. , -1. , -1. ,  1. , -1. ,  1. ])
#previous_values = []

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

X = cp.Variable((8,8), symmetric = True)
constraints = [X >> 0]
constraints += [
    X[i,i] == 1 for i in range(8)
    ]
objective = sum(0.5*(1 - X[i,j]) for (i,j) in edges)
prob = cp.Problem(cp.Maximize(objective), constraints)
prob.solve()
#x1 = sqrtm(X.value)
#print(x1)
while True:    
    u = np.random.randn(8)
    x = np.sign(X.value @ u)
    #print(u)
    #print(x)
    
    #test = read_previous_values("previous_values.txt")
    #print(test)

    previous_values = read_previous_values(file_path)
    if any(np.array_equal(x, prev_x) for prev_x in previous_values):
        print("x is a previous value.")
        if  np.array_equal(x, reference_value) or np.array_equal(x, reference_value2):
            print("Max-Cut Found.")
            correct += 1
        else:
            print("Re-Found Wrong Solution")
    else:
        print("x is not a previous value. Adding to the file.")
        write_previous_value(file_path, x)
        #time.sleep(6)
    
    accuracy = correct/loop * 100
    print("Current Accuracy is " + str(accuracy) +"%")
    print("Current Loop is " + str(loop) + ".")
    loop += 1

