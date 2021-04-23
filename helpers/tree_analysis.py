import csv

"""
Doc Doc Doc
"""


class TreeAnalysis:

    def __init__(self, yolo_tree):
        self.yolo_tree = yolo_tree

    def get_analysis_csv(self):

        res = [["PredID", "BranchStartTime", "BranchStopTime"]]

        # print("Tree Analysis CSV")
        # print(self.yolo_tree)
        for root_node in self.yolo_tree["tree_info"]["root_nodes"]:
            root_pred_id = root_node.split(".", 1)[-1]
            for branch_edge in self.yolo_tree["tree_info"]["branch_edges"]:
                branch_time_num, branch_pred_id = branch_edge[0].split(".")
                if branch_pred_id == root_pred_id:
                    branch_leaf_node = self.yolo_tree["tree_dict"][branch_edge[-1]][-1]
                    leaf_time_num, leaf_pred_id = branch_leaf_node.split(".", 1)
                    res.append([root_pred_id, branch_time_num, leaf_time_num])

        with open("data/recent_analysis.csv", "w") as w_file:
            writer = csv.writer(w_file, delimiter=",")
            for row in res:
                writer.writerow(row)

