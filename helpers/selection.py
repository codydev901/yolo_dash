import os
import json
from helpers.yolo_csv import YoloCSV
from helpers.yolo_tree import YoloTree
from helpers.yolo_plot import YoloPlot

"""
Doc Doc Doc
"""


def get_source_files():

    return [{"label": v, "value": v} for v in os.listdir("data") if "recent_query" not in v]


def get_trap_nums(yolo_csv_c):

    v_json = json.loads(yolo_csv_c)

    return [{"label": v, "value": v} for v in v_json["trap_nums"]]


def get_time_nums(yolo_csv_c, trap_num):

    loaded_yolo_csv_c = json.loads(yolo_csv_c)
    yolo_csv = YoloCSV(loaded_yolo_csv_c["file_name"])
    time_nums = yolo_csv.get_time_nums(trap_num=trap_num)

    return [{"label": int(v), "value": int(v)} for v in time_nums]


def run_query(source_file, trap_num, time_num):

    yolo_csv = YoloCSV("data/{}".format(source_file))
    graph_info, query_df = yolo_csv.to_graph_info(trap_num, time_num)
    yolo_tree = YoloTree(graph_info)

    cats = YoloPlot(yolo_tree=yolo_tree, graph_info=graph_info)

    tree_info = vars(YoloTree(graph_info=graph_info))

    print(tree_info)

    web_info = web_info_from_tree_info(tree_info)

    return cats.fig, query_df, web_info


def web_info_from_tree_info(tree_info):

    web_info = dict()

    # Total Branch Count
    web_info["total_branch_count"] = len(tree_info["tree_info"]["branch_nodes"])

    # Main Branch Count -- Unsafe on multiple mains atm
    branch_edges = list(tree_info["tree_info"]["branch_edges"])
    branch_edges = [v for v in branch_edges if v[0][-1] == "1"]
    web_info["main_branch_count"] = len(branch_edges)

    # Longest Main Branch -- Unsafe on multiple mains atm, uses branch edges from above
    longest_main_branch_count = 0
    longest_main_branch_node = ""
    shortest_main_branch_count = 10000000
    shortest_main_branch_node = ""
    for b_e in branch_edges:
        branch = tree_info["tree_dict"][b_e[-1]]
        branch_length = len(tree_info["tree_dict"][b_e[-1]]) + 1
        if branch_length > longest_main_branch_count:
            longest_main_branch_count = branch_length
            try:
                longest_main_branch_node = "{} To {}".format(b_e[-1], branch[-1])
            except IndexError:
                longest_main_branch_node = "{} To {}".format(b_e[0], b_e[-1])
        if branch_length < shortest_main_branch_count:
            shortest_main_branch_count = branch_length
            try:
                shortest_main_branch_node = "{} To {}".format(b_e[-1], branch[-1])
            except IndexError:
                shortest_main_branch_node = "{} To {}".format(b_e[0], b_e[-1])

    print("yeet")
    print(web_info)

    web_info["longest_main_branch_count"] = "{}".format(longest_main_branch_count)
    web_info["longest_main_branch_nodes"] = longest_main_branch_node
    web_info["shortest_main_branch_count"] = "{}".format(shortest_main_branch_count)
    web_info["shortest_main_branch_nodes"] = shortest_main_branch_node

    return web_info


def load_source_file(file_name):

    return YoloCSV("data/{}".format(file_name))
