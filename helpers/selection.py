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

    return cats.fig, query_df


def load_source_file(file_name):

    return YoloCSV("data/{}".format(file_name))
