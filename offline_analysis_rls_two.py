import os
import csv
import json
from helpers.yolo_csv import YoloCSV

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

    f_n = "FT_BC8_yolo_short.csv"

    all_traps = json.loads(YoloCSV(file_path="data/{}".format(f_n)).to_initial_json())["trap_nums"]

    rls_all = [["trap_num", "root_pred_id", "num_branches", "branch_time_nums"]]

    for trap_num in all_traps:
        rls_info = get_rls_from_trap(source_file=f_n, trap_num=trap_num, time_num=500)
        print("P", trap_num)
        # Ignore Headers
        for v in rls_info[1:]:
            rls_all.append(v)

    with open("data/{}_rls_root_branches.csv".format(f_n.replace(".csv", "")), "w") as w_file:
        writer = csv.writer(w_file, delimiter=",")
        for row in rls_all:
            writer.writerow(row)

    # with open("data/{}_rls_errors.csv".format(f_n.replace(".csv", "")), "w") as w_file:
    #     writer = csv.writer(w_file, delimiter=",")
    #     for row in did_error:
    #         writer.writerow(row)


if __name__ == "__main__":

    main()
