import os
import csv
import json
from helpers.yolo_csv import YoloCSV
from helpers.yolo_cyto import YoloCyto

"""
Doc Doc Doc
"""


def get_rls_from_trap(source_file, trap_num, time_num):

    yolo_csv = YoloCSV("data/{}".format(source_file))

    root_branch_info = yolo_csv.to_root_branch_info(trap_num, time_num)

    rls_info = [["trap_num", "root_pred_id", "num_branches", "branch_time_nums"]]
    for root_node in root_branch_info["root_nodes"]:
        pred_id = root_node.split(".", 1)[-1]
        branches = root_branch_info["root_branches"][pred_id]
        rls_info.append([trap_num, pred_id, len(branches)] + branches)

    return rls_info


def main():

    f_n = "FT_BC8_mrcnn_short_v2.csv"

    all_traps = json.loads(YoloCSV(file_path="data/{}".format(f_n)).to_initial_json())["trap_nums"]

    trap_num = 1
    time_num = 500

    # for t in all_traps:
    #
    #     print("****")
    #     print(t)

    graph_info, df = YoloCSV(file_path="data/{}".format(f_n)).to_graph_info(trap_num, time_num)

    cyto = YoloCyto(graph_info=graph_info)
    cyto.to_cytoscape_network_csv()

    # print(graph_info)




if __name__ == "__main__":

    main()

