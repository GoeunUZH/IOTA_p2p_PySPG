from graph_tool.all import *
import graph_tool.all as gt
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import math


                                  
 def get_unweighted_Partitioning(rho, zipfs, bigR):
    dimension=len(rho)*len(zipfs)*len(bigR)*100
    partition_cost_array = np.zeros(dimension).reshape(len(rho),len(zipfs),len(bigR),100)
    small_mana_percent_array = np.zeros(dimension).reshape(len(rho),len(zipfs),len(bigR),100)
    N=1000
    for a,i in enumerate(rho):
        for b,j in enumerate(zipfs):
            for c,k in enumerate(bigR): 
                for l in range(1,101):
                    edge_list=[]
                    mana_list = [mana_zipf(i, j) for i in range(1,N+1)]
                    with open('/local/scratch/exported/p2p_iota_simul/sim_varyS_floatM_PowerLaw/outboundListrho'+
                              str(i)+'s'+ str(j) +'R'+ str(k)+'/loop'+ str(l)+'.txt','r') as f:
                        data=f.readlines()
                        for line in data:
                            odom = line.split()
                            for z in range(1,len(odom)):
                                e=min(mana_list[int(odom[0])-1], mana_list[int(odom[z])-1])
                                edge_list.append((int(odom[0])-1,int(odom[z])-1,e))
   
                                
                                
                    g = gt.Graph(directed=False)
                    
                    eweight = g.new_ep("float")
                    g.add_edge_list(edge_list, eprops=[eweight])
                    gt.remove_parallel_edges(g)
                    G=g.copy()
                    original_weight = eweight.fa  
#                     print("G_weight", original_weight)

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
                    
                    cost_ratio = (sum(original_weight)-sum((after_remove_weight)))/sum(original_weight)
                    partition_cost_array[a, b, c, l-1] = cost_ratio
        
                    
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
                    small_mana_percent_array[a, b, c, l-1] = small_mana_percent 

                
                  
    return(partition_cost_array, small_mana_percent_array)