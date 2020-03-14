#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 17:13:51 2020

@author: meli
"""

#lirbaries needed to run analysis
import csv
from operator import itemgetter
import networkx as nx

# Openning and reading files
with open('RQ1ATT.csv', 'r') as nodecsv:
    nodereader = csv.reader(nodecsv)
    nodes = [n for n in nodereader][1:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open('RQ1EL.csv', 'r') as edgecsv: # Open the file
    edgereader = csv.reader(edgecsv) # Read the csv
    edges = [tuple(e[0:3]) for e in edgereader][1:] # Retrieve the data


#Creating the Network
DG = nx.DiGraph()
DG.add_nodes_from(node_names)
DG.add_weighted_edges_from(edges)

weight =nx.get_edge_attributes(DG,'weight')


# Centrality Measures
degree_dict = dict(DG.degree(weight=weight.values()))
betweenness_dict = nx.betweenness_centrality(DG, weight = weight.values(), normalized = False)
eigenvector_dict = nx.eigenvector_centrality (DG)

# Setting node attributes for centrality measures
nx.set_node_attributes(DG, degree_dict, 'degree')
nx.set_node_attributes(DG, betweenness_dict, 'betweenness')
nx.set_node_attributes(DG, eigenvector_dict, 'eigenvector')

betweenness_dict.keys()



lst = list(zip(degree_dict.keys(), degree_dict.values(), betweenness_dict.values(), eigenvector_dict.values()))

with open('Centrality_Measures.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Subreddit', 'Degree', 'Betweenness', 'Eigenvector'])
    for row in lst:
        csv_out.writerow(row)
#----------------------------------------------------------------------#

def Get_Promient_Actors_by_cent(cent):
    if cent == "degree":
        cent = degree_dict.items()
    elif cent == "betweenness":
        cent = betweenness_dict.items()
    else:
        cent = eigenvector_dict.items()
    sorted_cent = sorted(cent, key=itemgetter(1), reverse=True)
    Prom_Act = sorted_cent[:int(len(sorted_cent) * .20)]
    Prom_Act_No_0 = [ i for i in Prom_Act if i[1] != 0.0]
    return Prom_Act_No_0

Betweenness_Prom_Act = Get_Promient_Actors_by_cent("betweenness")

#ask if this can be cleaned up of if there's a better way of doing this
def Get_Top_Egin_of_Top_Cent(x):
    res = [[ i for i, j in x ],
           [ j for i, j in x ]]
    Prom_Bet_node = list(res[0])
    lst = []
    for element in Prom_Bet_node:
        Y = eigenvector_dict[element]
        lst.append(Y)
    Prom_Act_Eigen = {}
    for key in Prom_Bet_node:
        for value in lst:
            Prom_Act_Eigen[key] = value
            lst.remove(value)
            break
    sorted_egin_of_top_bet  = sorted(Prom_Act_Eigen.items(), key=itemgetter(1), reverse=True)
    Top_Egin_of_Top_Bet = sorted_egin_of_top_bet[:int(len(sorted_egin_of_top_bet) * .20)]
    return [nodes[0] for nodes in Top_Egin_of_Top_Bet]


Prom_Act = Get_Top_Egin_of_Top_Cent(Betweenness_Prom_Act)
print(Prom_Act)

#################### need to clean up  code from  this point on ##############

# Write Ego Nodes List
def get_nodes_of_egos_networks(x):
    return [n for n in DG[x]]
ego_net_nodes = [get_nodes_of_egos_networks(t) for t in Prom_Act]

flat_ego_node_list = []
for sublist in ego_net_nodes:
    for item in sublist:
        flat_ego_node_list.append(item)

complete_ego_nodes_list = Prom_Act + flat_ego_node_list

res1 = []
for i in complete_ego_nodes_list:
    if i not in res1:
        res1.append(i)
######################## Need to clean above########

with open('Ego_Nodes_List.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Subreddit Name'])
    for val in res1:
        writer.writerow([val])

# Write Ego Network Edgelist
def get_Egos_of_Prom_Act(x):
    return [n for n in DG[x]]
Egos_of_Prom_Act = [get_Egos_of_Prom_Act(t) for t in Prom_Act]
edge = [[i[0],j] for i in Egos_of_Prom_Act for j in i[1:]]

with open('Ego_Network_EL.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['source', 'target'])
    for i in edge:
        writer.writerow(i)
