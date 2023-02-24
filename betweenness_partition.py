from graph_tool.all import *
import graph_tool.all as gt
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import math


                                  
def get_unweighted_Partitioning(g):
    
    G=g.copy()
    original_weight = eweight.fa  
    #  print("G_weight", original_weight)

    for link in range(N):
        u = gt.extract_largest_component(g,prune=True)
        if len(list(u.vertices())) == N:
            vp, ep = gt.betweenness(g)
            list_ep=list(ep.fa)
            top_bt=list_ep.index(max(list_ep))
            g.remove_edge(list(g.edges())[top_bt])
        else:
            break
    after_remove_weight = eweight.fa

    partition_cost_ratio = (sum(original_weight)-sum((after_remove_weight)))/sum(original_weight)


    sp = gt.GraphView(g, vfilt=gt.label_largest_component(g))
    big_part_index=list(sp.vertex_index)
    total_index=range(N)
    small_part_index=[]
    for m in total_index:
        if m not in big_part_index:
            small_part_index.append(m)
    small_part_mana_list=[]
    for s in small_part_index:
        small_part_mana_list.append(mana_list[s])
    small_mana_percent = sum(small_part_mana_list)/sum(mana_list)


                    
    return(partition_cost_ratio, small_mana_percent)