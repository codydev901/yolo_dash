import os
import csv
import json
from helpers.yolo_csv import YoloCSV
from helpers.yolo_csv_v2 import YoloCSVTwo
from helpers.yolo_tree import YoloTree
from helpers.yolo_tree_v2 import YoloTreeTwo
from helpers.yolo_plot import YoloPlot
from helpers.yolo_plot_v2 import YoloPlotTwo
from helpers.tree_analysis import TreeAnalysis

"""
Doc Doc Doc
"""


def get_rls_from_trap(source_file, trap_num, time_num):

    if "all" in source_file:
        print("V2 YoloCSV")
        yolo_csv = YoloCSVTwo("data/{}".format(source_file))
    else:
        print("V1 YoloCSV")
        yolo_csv = YoloCSV("data/{}".format(source_file))

    graph_info, query_df = yolo_csv.to_graph_info(trap_num, time_num)
    tree = YoloTreeTwo(graph_info=graph_info)
    rls_info = tree.get_rls_info()

    return rls_info


def main():

    f_n = "FT_BC8_all_traps_short.csv"

    all_traps = json.loads(YoloCSVTwo(file_path="data/FT_BC8_all_traps_short.csv").to_initial_json())["trap_nums"]

    rls_all = [["trap_num", "pred_id", "time_start", "time_end"]]
    did_error = [["trap_num", "error"]]

    for trap_num in all_traps:
        try:
            rls_info = get_rls_from_trap(source_file="FT_BC8_all_traps_short.csv", trap_num=trap_num, time_num=500)
        except ValueError:
            print("F-MultipleRoots", trap_num)
            did_error.append([trap_num, "multiple_roots"])
            continue
        except KeyError:
            print("F-ParseFail", trap_num)
            did_error.append([trap_num, "parse_fail"])
            continue
        print("P", trap_num)
        # Ignore Headers
        for v in rls_info[1:]:
            rls_all.append(v)

    with open("data/{}_rls_raw.csv".format(f_n.replace(".csv", "")), "w") as w_file:
        writer = csv.writer(w_file, delimiter=",")
        for row in rls_all:
            writer.writerow(row)

    with open("data/{}_rls_errors.csv".format(f_n.replace(".csv", "")), "w") as w_file:
        writer = csv.writer(w_file, delimiter=",")
        for row in did_error:
            writer.writerow(row)


if __name__ == "__main__":

    main()

