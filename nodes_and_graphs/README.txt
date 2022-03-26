==================
Basic information
==================
Created on 25-March-2022
Author: Shiv Muthukumar
Version: 1
Python: 3.9.10 64-bit

============
Description
============
A simple script that generates a graph using the nodes from a file and allows user to check for upstreams or downstreams and the processing time of a node.

=============
Requirements
=============
A text file, in the same directory as the nodes_n_graph.py, containing list of nodes to be created. Example file available - nodes.txt. Format of the file contents:
"""
<node1_name>|<downstream1_1>,<downstream1_2>,...|<node_processing_time>
<node2_name>|<downstream2_1>,<downstream2_2>,...|<node_processing_time>
...
"""

=============
How it works
=============
Uses the nodes file to create nodes and adds it to a graph.
Get user inputs - Action, Stream, Node name
Based of the Action user selects, calls the relevant function.
	Find streams > Downstream --> Lists all the unique downstreams of the current node in no specific order
	Find streams > Upstream --> Lists all the unique upstreams of the current node in no specific order
	Processing time > Upstream --> Calculates the total time it takes to complete the current node from the very first node
	Processing time > Downstream --> Throw alert! Processing time does not make sense when looking forward in graph.

========
Contact
========
Email: shivsmk.pr@gmail.com