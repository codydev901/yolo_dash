import os
import json
from helpers.yolo_csv import YoloCSV
from helpers.yolo_csv_v2 import YoloCSVTwo
from helpers.yolo_tree import YoloTree
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import random

"""
Doc Doc Doc

https://stackoverflow.com/questions/11479624/is-there-a-way-to-guarantee-hierarchical-output-from-networkx
"""


def yolo_tree_to_plot(yolo_tree):

    print("yeet")
    print(vars(yolo_tree))

    # print(yolo_tree.tree_info["root_nodes"])

    root_node = yolo_tree.tree_info["root_nodes"][0]


    # nx_graph.nodes[1]['title'] = 'Number 1'
    # nx_graph.nodes[1]['group'] = 1
    # nx_graph.nodes[3]['title'] = 'I belong to a different group!'
    # nx_graph.nodes[3]['group'] = 10
    # nx_graph.add_node(20, size=20, title='couple', group=2)
    # nx_graph.add_node(21, size=15, title='couple', group=2)
    # nx_graph.add_edge(20, 21, weight=5)
    # nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)
    # nt = Network('500px', '500px')
    # # populates the nodes and edges data structures
    # nt.from_nx(nx_graph)
    # nt.show('nx.html')


def run_offline_plot(source_file="FT_BC8_all_traps_short.csv", trap_num=1, time_num=150):

    if "all" in source_file:
        yolo_csv = YoloCSVTwo("data/{}".format(source_file))
    else:
        yolo_csv = YoloCSV("data/{}".format(source_file))

    graph_info, query_df = yolo_csv.to_graph_info(trap_num, time_num)
    yolo_tree = YoloTree(graph_info)

    yolo_tree_to_plot(yolo_tree)


def main():

    run_offline_plot(trap_num=1, time_num=500)


if __name__ == "__main__":

    main()
