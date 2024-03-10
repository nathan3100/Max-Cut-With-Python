If you've having trouble running any of these because the python plugins aren't working then you should stick them all in a folder, shift right click the open folder and open in cmd or powershell, then run a command like 'python G+W.py' to run the first script. This is how I've got everything working. You may also need to install somethings with PIP.

G+W.py:

This file will run the algorithm once and display the graph with the nodes coloured based on the algorithms output. Closing the graph window will re-run the algorithm and display a new graph with the nodes coloured from the new data.
The algorithm used is made by Goemans and Williamsons here: https://dl.acm.org/doi/abs/10.1145/227683.227684 

G+W2.py:

This file does exactly the same thing as G+W.py but with a graph of 20 nodes instead of 8 nodes to show how a little increase in complexity very quickly makes the problem much much harder. Additionally this program now outputs 3 graphs: the original graph, the graph after the algorithm has coloured the nodes to mark which edges to cut, and the graph rearranged to make it very clear which lines are being cut. Notice that the name of the windows contains the cut length.

G+W3.py:

This file again does exactly the same thing as G+W2.py but now with 50 nodes.

G+W3Loop.py:

This file is a modified copy of G+W3.py which loops infinitely in an attempt to find the max cut of this large graph. For its accuracy stat, it's assuming the largest cut it finds is the cut and when it finds a bigger cut it resets this value. The largest I personally saw was a cut of 311. 

G+WUser.py:

This is sort of the final version of the program as it combines all the best bits. It will ask the user to pick the number of nodes and edges, produce a random graph, attempt to find its max cut, and then output the 3 graphs to show this. 

G+WGraph.py:

This file will run the algorithm over and over again, and each time it does it will compare the solution its found with a text file. If it's found a new solution it will record this and repeat, if it's refound an old output it will just go again. It also knows the correct solutions for this given graph so will in real time work out how accurate the algorithm is being.

G+WText.py:

This file is used to make the text file easier to understand. It will go through the text file one by one until you run out of entries, each time you close the graph window it will go onto the next one.

GraphMaker.py:

This is a nice little script that lets the user put in the size of the adjacency matrix (number of nodes) and how many edges the graph should have and it'll make a random graph. Very useful for quickly making some test data.



