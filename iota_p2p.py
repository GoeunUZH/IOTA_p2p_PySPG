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
    my_command = f'./sim_powerLawFloat -rho {round(rho,1):g} -R {R} -Zipfs {round(zipfs,1):g} -N {N} -k {k} -fname  {fname}' 

#    print(my_command)
    os.system(my_command)
    
    #filelist=glob.glob('outboundListrho'+ str(i)+'s'+ str(j) +'R'+ str(k)+'.txt')
    #file_deal(filelist)

    edge_list=[]
    with open("outboundList_" + fname + ".txt",'r') as f:
#        data=f.readlines()
        for line in f:
            odom = [_-1 for _ in map(int, line.split() ) ]
            n0 = odom[0]
            for z in odom[1:]:
                edge_list.append((n0,z))

    g=gt.Graph(directed=False)
    g.add_edge_list(edge_list)
    dist, ends = gt.pseudo_diameter(g)
    output = {}
    output['diameter'] = dist
    output['clustering'],_ = gt.global_clustering(g)
     
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
            os.system("rm manaListRho_*.txt")

