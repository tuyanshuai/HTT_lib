# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:00:41 2018

@author: yanshuai
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 17 19:50:18 2018

@author: yanshuai
"""
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy
    # Given a graph, return a sorted graph
G=  nx.dense_gnm_random_graph(10, 20, 0)

plt.subplot(1,2,1) 
pos=nx.circular_layout(G) # positions for all nodes 
nx.draw(G, pos, with_labels = True, node_color = 'gray') 
# Empty dict
mapping = {}
# Fill in the entries one by one
loc = numpy.argsort(G)
srcnames = list(G.nodes)
for i in loc:
    mapping[srcnames[loc[i]]] = i
G = nx.relabel_nodes(G, mapping, copy=True)
  
plt.subplot(1,2,2)
nx.draw(G, pos, with_labels = True, node_color = 'gray') 



 