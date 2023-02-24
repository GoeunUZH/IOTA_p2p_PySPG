#!/usr/bin/env python3

import sys
import os
import glob
#import natsort
#from natsort import realsorted, ns
import fileinput
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx
from graph_tool.all import *
import graph_tool.all as gt
import math

from betweenness_partition import get_unweighted_Partitioning

import spg
from spg.runner import SingleRunner

def run_simulation(par_dict):
    diameter={}
    
    
   
    rho=par_dict['rho']
    zipfs=par_dict['zipfs']
    R=par_dict['R']

    N=par_dict['N']
    k=par_dict['k']


    fname = f'N-{N}_k-{k}_rho-{round(rho,1):g}_zipfs-{round(zipfs,1):g}_R-{R}' 
    go_compile = f'go build sim_powerLawFloat.go'
    go_command = f'./sim_powerLawFloat -rho {round(rho,1):g} -R {R} -Zipfs {round(zipfs,1):g} -N {N} -k {k}' 

#    print(my_command)
    os.system(go_compile)
    os.system(go_command)
    
    def mana_zipf(i, zipfs):
        m=1e+10
        return m*(math.pow(i,-zipfs))

    edge_list=[]
    mana_list = [mana_zipf(i, zipfs) for i in range(1,N+1)]
    with open("outboundList_" + fname + ".txt",'r') as f:
#        data=f.readlines()
        for line in f:
            odom = [_-1 for _ in map(int, line.split() ) ]
            n0 = odom[0]
            for z in odom[1:]:
                e=min(mana_list[n0], mana_list[z])
                edge_list.append((n0, z, e))

    
    
    
    g=gt.Graph(directed=False)
    nodes = g.add_vertex(N)
    # add link weight(cheaper side mana value) as a base element in the generate graph
    eweight = g.new_ep("float")
    g.add_edge_list(edge_list, eprops=[eweight])
    g.edge_properties["link_weight"] = eweight
    # remove parallel links
    gt.remove_parallel_edges(g)
    v_mana = g.new_vertex_property("float")
    for node, mana in zip(nodes, mana_list):
        v_mana[node]= mana

    
    output = {}
    output['diameter'],_ = gt.pseudo_diameter(g)
    output['clustering'],_ = gt.global_clustering(g)
    output['assortativity'],_ = gt.scalar_assortativity(g, v_mana) 
    output['partition_cost_ratio'],output['small_mana_percent'] = get_unweighted_Partitioning(g, N, mana_list)
    # _,output['small_mana_percent'] = get_unweighted_Partitioning(g, N, mana_list)

     
    return output







#################  
#################  
#################  
#################  MAIN LOOP
#################  
#################  
#################  


def parse_command_line():
    import sys, optparse

    parser = optparse.OptionParser()

    parser.add_option("--repeat", action='store', dest="repeat", type='int',
                      default=None, help="number of repetitions")
    parser.add_option("--filter", action='store', dest="filter", type='str',
                      default=None, help="filter the parameters")
    parser.add_option("--workers", action='store', dest="workers", type='int',
                      default=None, help="number of workers")
    parser.add_option("--rewrite", action='store_true', dest="rewrite",
                        help = "if the csv file - if existing - should be rewritten. If not added, append operation is performed" )

    parser.add_option("--clear-outputs", action='store_true', dest="clean_outputs",
                        help = "if the csv file - if existing - should be rewritten. If not added, append operation is performed" )

    command = sys.argv[0]
    options, args = parser.parse_args()

    return command, options, args



command, options, args = parse_command_line()


# THIS SHOULD ALWAYS BE IN A __name__ == "__main__" block
if __name__ == '__main__':
    for arg in args:

        runner = SingleRunner(arg, options.repeat)
        if options.filter != None:
            runner.filter(options.filter)
        runner.run(run_simulation, options.workers)
        runner.save_results(options.rewrite)
        
        if options.clean_outputs:
            os.system("rm outboundList_*.txt")
            os.system("rm manaList_*.txt")

