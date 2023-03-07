from graph_tool.all import *
import graph_tool.all as gt
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import math



def get_greedy_Partitioning(g, N, mana_list):
    
    G=g.copy()
    eweight=G.edge_properties["link_weight"]
    original_weight = eweight.fa
                                
    #  split node_1, split node_1 and node_2, ...  
    greedy_move_list=[]
    q=range(N)
    for n in range(N):
        greedy_move_list.append(list(q[0:n+1]))


    for m in range(N-1):
        cut_nodes=greedy_move_list[m]
    #  print("cut-nodes", cut_nodes)
        
        links=[]
        for node in range(len(cut_nodes)):        
            for s, t, h in G.iter_all_edges(cut_nodes[node], [g.edge_index]):
                links.append((s,t)) 

        for start,end in links:
            if end not in cut_nodes:
    #                                 print('end',end)
                G.remove_edge(G.edge(start,end)) 

        after_remove_weight = eweight.fa
        cost_ratio = (sum(original_weight)-sum((after_remove_weight)))/sum(original_weight)
    #                         print(cost_ratio)
        partition_cost = cost_ratio


        small_part_mana_list=[]
        for nodes in range(len(cut_nodes)):
            small_part_mana_list.append(mana_list[nodes])
            if len(cut_nodes) < 500:
                small_mana_percent = sum(small_part_mana_list)/sum(mana_list)
            else:
                small_mana_percent = 1-(sum(small_part_mana_list)/sum(mana_list))
            
        
        small_mana_percent = small_mana_percent         
        
                        
                        


    return(partition_cost, small_mana_percent)

