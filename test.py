# -*- coding: utf-8 -*-
"""
Created on Thu May 17 19:50:18 2018


1. color id  === cid   -1 not painted   0 any color id for isolated, then
 1,2,3,r+1

@author: yanshuai
"""
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy
import matplotlib.colors as colors

def HTT_Theta(G):
    deg = G.degree
    edgedeg = []
    for e in G.edges(data=True):       
        edgedeg.append(deg[e[0]] + deg[e[1]])       
    return max(edgedeg)
 
    # Given a graph, return a sorted graph
def HTT_SortGraph(G):    
    
    # Empty dict
    mapping = {}
    # Fill in the entries one by one
    degrees = numpy.array(list(G.degree))[:,1]
    loc = numpy.argsort(-degrees)    
    srcnames = list(dict(G.nodes).keys())
    
    B2Sval = sorted(degrees, reverse =True);
     
    for i in loc:
        mapping[srcnames[loc[i]]] = i
    G = nx.relabel_nodes(G, mapping, copy=True)
    
    G.degreearray = degrees
    G.B2Sloc = loc
    G.B2Sdeg = B2Sval
    return G


def HTT_Print_Attribute(G , attributename ):    
    graphcids  = nx.get_node_attributes(G, attributename)
    print(graphcids)

def HTT_GetAttribute(G , nodename, attributename ):       
    graphcids  = nx.get_node_attributes(G, attributename)
    return graphcids[nodename]

def HTT_SetAttribute(G , nodename, attvalue, attributename ):       
    graphcids  = nx.get_node_attributes(G, attributename)
    graphcids[nodename] = attvalue
    nx.set_node_attributes(G, graphcids,attributename)
    return G

def HTT_Paint(G , nodename, colorid):           
    return HTT_SetAttribute(G , nodename, colorid, 'cid')
    #graphcids  = nx.get_node_attributes(G, 'cid')
    #graphcids[nodename] = cid
    #nx.set_node_attributes(G, graphcids,'cid')
    #return G

def HTT_PreprocessGraph(G , plot = False):       
    #plt.subplot(1,2,1) 
    #pos=nx.circular_layout(G) # positions for all nodes 
    #nx.draw(G, pos, with_labels = True, node_cid = 'gray') 
    G = HTT_SortGraph(G)
    #plt.subplot(1,2,2)
    #nx.draw(G, pos, with_labels = True, node_cid = 'gray') 
    
 
    theta = HTT_Theta(G)
    r = math.ceil((theta-1)/2)
    n = G.number_of_nodes()
    s = math.ceil(n/(r+1))
    
#    print('n = '+ str(n) + ' theta = ' + 
#               str(theta) + ' r+1 =' + str(r+1) + '   s=' + str(s))
    IsoNum = s *(r+1) - n;
    
    #nx.set_node_attributes(G, -1, 'cid')    
    
    G.cid = list(-1 for i in range(n+IsoNum))
    
    pos=nx.circular_layout(G) # positions for all nodes 
    
    maxX= 0;
    for p in pos:
        if(pos[p][0]>maxX):
            maxX = pos[p][0];
            
    for i in range (IsoNum):
         G.add_node(i+n)
         #G = HTT_Paint(G, i+n, 0) # 0 means not care
         G.cid[i+n] = 0
         pos[i+n] = [maxX*1.2+0.2,1-i/IsoNum]
    
    if (plot):
        plt.figure(2)
        nx.draw(G, pos, with_labels = True, node_color = 'gray') 
        
    
    
    
    G.pltpos = pos;
    G.theta = theta
    G.r =r
    G.n =n
    G.s =s
    
    return {'theta': theta, 'r': r, 'n': n, 's':s,  'G': G}





# set manually list add z = list(set(x) + set(y))
# set manually list minus z = list(set(x) - set(y))
def HTT_UsedColor(G, i):
    
    usedcolor = []
    for j in range(i): 
        #if G.has_edge(i,j) and G.node[j]['cid']>0:  # j is neighbour of i            
        if G.has_edge(i,j) and G.cid[j]>0:  # j is neighbour of i            
            #usedcolor.append(G.node[j]['cid'])
            usedcolor.append(G.cid[j])
            
    return usedcolor
            
     
    

def HTT_Greedy_Paint(G):
    # Loop all node    
       
    n =G.n
    rp1 =G.r+1
    for i in range(n):
        usedcolor = HTT_UsedColor(G, i)
        
        availcolor = list(set(range(1,rp1+1)) - set(usedcolor))
        
        #G  = HTT_Paint( G, i,  availcolor[0])
        G.cid[i] =  availcolor[0]
        
    return G

def HTT_ConstructH(G):
    
    H = nx.DiGraph()    
    
     
    

def HTT_DrawGraph(G, colorNames):
    plt.figure    
    colors = [];    
    for i in G.nodes:
          #colors.append(colorNames[HTT_GetAttribute(G,i, 'cid')])
          colors.append(colorNames[G.cid[i]])

    nx.draw(G, G.pltpos, with_labels = True, node_color = colors, node_size=800) 
############################ Main Function ####################################
    
colorNames = list(colors.cnames.keys())[0:]

G=  nx.dense_gnm_random_graph(15, 25, 0)
 
GP =  HTT_PreprocessGraph(G, True) 

G = GP['G']

print('n = '+ str(GP['n']) + ' theta = ' + str(GP['theta']) + 
      ' r+1 =' + str(GP['r']+1) + '   s=' + str(GP['s']))
##############################Greedy Paint#####################################
 
G = HTT_Greedy_Paint(G)
HTT_DrawGraph(G, colorNames)




