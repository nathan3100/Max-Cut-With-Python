G+W.py
This file will run the algorithm once and display the graph with the nodes coloured based on the algorithms output. Closing the graph window will re-run the algorithm and display a new graph with the nodes coloured from the new data.
The algorithm used is made by Goemans and Williamsons here: https://dl.acm.org/doi/abs/10.1145/227683.227684 

G+WGraph.py
This file will run the algorithm over and over again, and each time it does it will compare the solution its found with a text file. If it's found a new solution it will record this and repeat, if it's refound an old output it will just go again. It also knows the correct solutions for this given graph so will in real time work out how accurate the algorithm is being.

G+WText.py
This file is used to make the text file easier to understand. It will go through the text file one by one until you run out of entries, each time you close the graph window it will go onto the next one.
