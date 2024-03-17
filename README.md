If you're having trouble running any of these because the Python plugins aren't working then you should stick them all in a folder, shift right-click the open folder and open in cmd or powershell, then run a command like 'python G+W.py' to run the first script. This is how I've got everything working. You may also need to install some things with PIP.

G+W.py:

This file will run the algorithm once and display the graph with the nodes coloured based on the algorithm's output. Closing the graph window will re-run the algorithm and display a new graph with the nodes coloured from the new data.
The algorithm used is made by Goemans and Williamson's here: https://dl.acm.org/doi/abs/10.1145/227683.227684 

G+W2.py:

This script does exactly the same thing as G+W.py but with a graph of 20 nodes instead of 8 nodes to show how a little increase in complexity very quickly makes the problem much much harder. Additionally, this program now outputs 3 graphs: the original graph, the graph after the algorithm has coloured the nodes to mark which edges to cut, and the graph rearranged to make it very clear which lines are being cut. Notice that the name of the windows contains the cut length.

G+W2Loop.py:

This script is a modified copy of G+W2.py, which loops infinitely in an attempt to find the max cut of this large graph. For its accuracy stat, it's assuming the largest cut it finds is the cut and when it finds a bigger cut it resets this value. It also doesn't draw the graphs out each time to increase efficiency so it can loop a lot quicker.

G+W3.py:

This script again does exactly the same thing as G+W2.py but now with 50 nodes.

G+W3Loop.py:

This script is a modified copy of G+W3.py which loops infinitely in an attempt to find the max cut of this large graph. For its accuracy stat, it's assuming the largest cut it finds is the cut and when it finds a bigger cut it resets this value. The largest I personally saw was a cut of 311. 

G+WUser.py:

This is sort of the final version of the program as it combines all the best bits. It will ask the user to pick the number of nodes and edges, produce a random graph, attempt to find its max cut, and then output the 3 graphs to show this. It can also colour the edges to show which should be cut (orange) and which can't be cut (green)

G+WText.py:

This script will run the algorithm over and over again, and each time it does it will compare the solution it found with a text file. If it's found a new solution it will record this and repeat, if it's refound an old output it will just go again. It also knows the correct solutions for this given graph so will in real time work out how accurate the algorithm is.

G+WGraph.py:

This script is used to make the text file easier to understand. It will go through the text file 'previous_values.txt' and sketch out all the graphs in the text file.

G+WGraph2.py

This script is for computers that struggle to have 80 windows open at once, as it lets the user pick which line of text to sketch out. This version also lets the user drag the nodes around to see how to form the cut. Sadly python won't do this when you have 80 windows open so I can't add this to the previous script.

G+W3Text.py:

This script is similar to G+WText.py, but instead uses the graph with 50 nodes from G+W3.py. Note this script is nowhere near as fast, that's expected.

G+W3Graph.py:

This script is again used to make the text file easier to understand. It will go to the line in the text file 'previous_values3.txt' the user specifies and sketch out as many as told to of the graphs in the text file.

G+W3Graph2.py

This script again will only show 1 graph to help with memory issues, and again the graphs output here have draggable nodes to help visualize the cut. 

G+W3Cuts.py:

This is a quick little script that goes through every recoreded cut in 'previous_values3.txt' and will output True if every cut is within 87.9% of the max-cut of this graph. (The max-cut is assumed to be 311)


GraphMaker.py:

This is a nice little script that lets the user put in the size of the adjacency matrix (number of nodes) and how many edges the graph should have and it'll make a random graph. Very useful for quickly making some test data.



