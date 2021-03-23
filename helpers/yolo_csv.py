import pandas as pd
import math
import sys
import json

"""
Doc Doc Doc
"""


class YoloCSV:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.valid_trap_nums = None
        self._on_init()

    def _on_init(self):
        self.df = pd.read_csv(self.file_path)

    def to_initial_json(self):
        """
        Doc Doc Doc
        """

        res = dict()
        res["file_name"] = self.file_path
        res["trap_nums"] = [int(v) for v in list(self.df["trap_num"].unique())]

        return json.dumps(res)

    def get_time_nums(self, trap_num):
        """
        Doc Doc Doc
        """

        q = self.query(trap_num=trap_num)
        return [int(v) for v in list(q["time_num"].unique())]

    def query(self, trap_num=None, t_start=None, t_stop=None, total_objs=None, pred_id=None, write_csv=False):
        """
        Easy way to query the full .csv/df.
        """

        query = ""

        if trap_num:
            query += "trap_num == {}".format(trap_num)

        if t_start and t_stop:
            query += " and {} <= time_num <= {}".format(t_start, t_stop)
        else:
            if t_start:
                query += " and time_num >= {}".format(t_start)
            if t_stop:
                query += " and time_num <= {}".format(t_stop)

        if total_objs:
            query += " and total_objs == {}".format(total_objs)

        if pred_id:
            query += " and predecessorID == {}".format(pred_id)

        if query[0] == " ":
            query = query[5:]

        res = self.df.query(query)

        if write_csv:
            res.to_csv("data/recent_query.csv", index=False)

        return res

    @staticmethod
    def _establish_root_nodes(df, graph_dict, graph_helper):
        """
        :param df: intermediate used in to_graph_info()
        :return:
        """

        start_time = df["time_num"].unique()[0]
        start_time_df = df.query("time_num == {}".format(start_time))
        len_time_step = len(start_time_df.index)
        graph_dict["time_num_obj"].append([start_time, len_time_step])
        graph_helper["last_num_obj"] = len_time_step

        for i, node in enumerate(start_time_df.to_dict('records')):

            pred_id = node["predecessorID"]
            time_num = node["time_num"]

            # Set PredecessorId if NaN
            if math.isnan(pred_id):
                pred_id = i+1

            node_name = "{}.{}".format(time_num, pred_id)
            graph_dict["graph"][node_name] = []
            graph_dict["root_nodes"].append(node_name)
            graph_helper["pred_id_last_node"][pred_id] = node_name

    @staticmethod
    def _check_errors_step_info(step_info, graph_dict, graph_helper):
        """
        :param step_info:
        :param graph_dict:
        :param graph_helper:
        :return:
        """

        keep_step_info = step_info
        # Error Case 1 - False Branch Multiple Nodes (Single Pred Before and After) - Example Trap 1 Time 137
        if graph_helper["current_num_obj"] > graph_helper["last_num_obj"]+1 and graph_helper["current_num_obj"] > graph_helper["next_num_obj"]+1:
            print("Error 1 Triggered:", step_info)
            graph_dict["check_ts"].append([step_info[0]["time_num"], "Case1"])
            parsed_steps = []
            keep_step_info = []
            for step in step_info:
                step_arr = [step[k] for k in step]
                if step_arr not in parsed_steps:
                    parsed_steps.append(step_arr)
                    keep_step_info.append(step)

        return keep_step_info

    @staticmethod
    def _handle_step_info(step_info, graph_dict, graph_helper):
        """
        :param step_info:
        :param graph_dict:
        :param graph_helper:
        :return:
        """

        active_pred_ids = [v["predecessorID"] for v in step_info]

        parsed_steps = []
        for step in step_info:
            step_arr = [step[k] for k in step]
            if step_arr in parsed_steps:
                branch_node_name = "{}.{}".format(step["time_num"], int(step["predecessorID"]))
                graph_dict["branch_nodes"].append(branch_node_name)
                next_pred_id = step["predecessorID"] + 1.0
                if next_pred_id in active_pred_ids:  # New Branch while an existing branch continues
                    next_pred_id = max(active_pred_ids) + 1.0
                print("GOT BRANCH:", branch_node_name, step_arr, "NextPredID:{}".format(next_pred_id))
                step["predecessorID"] = next_pred_id
                graph_helper["pred_id_last_node"][step["predecessorID"]] = branch_node_name
                active_pred_ids += [next_pred_id]

            parsed_steps.append(step_arr)

        # Clear Non-Active Pred Id's
        # for k in graph_helper["pred_id_last_node"]:
        #     if k not in active_pred_ids:
        #         graph_helper["pred_id_last_node"][k] = None

        return step_info

    def to_graph_info(self, trap_num, t_stop):
        """
        Attempts to parse a yolo.csv into a tree data structure that can then be used for further analysis.
        Good amount of in-line doc to cover how its done.

        Note: Currently not safe for all scenarios. Built using only trap == 1 w/ t_stop of ~30. Will likely need
        to re-write a good deal, but wanted to get something up and going that could be used with some visual tools
        before continuing.
        """

        # graph_dict is returned
        graph_dict = dict()
        graph_dict["trap_num"] = trap_num
        graph_dict["t_stop"] = t_stop
        graph_dict["graph"] = {}
        graph_dict["check_ts"] = []
        graph_dict["time_num_obj"] = []
        graph_dict["root_nodes"] = []
        graph_dict["branch_nodes"] = []

        # graph_helper is used in parsing
        graph_helper = dict()
        graph_helper["pred_id_last_node"] = {}

        # Return a copy of the source data filtered to specific trap number and t_stop.
        df = self.query(trap_num=trap_num, t_start=0, t_stop=t_stop, write_csv=True)

        # Establish Root Nodes. Assumes sorted/in order.
        self._establish_root_nodes(df, graph_dict, graph_helper)

        # We are interested in changes that occur between time steps. So will create sub-df's using those times.
        # Start at 2nd index because _establish_root_nodes() handles above
        for t in df["time_num"].unique()[1:]:

            # Run another filter of our initial filtered df from above on loop time step.
            time_df = df.query("time_num == {}".format(t))
            next_time_df = df.query("time_num == {}".format(t+1))

            # The number of data points per time-step may dictate behavior.
            len_time_step = len(time_df.index)
            len_next_time_step = len(next_time_df.index)
            graph_helper["current_num_obj"] = len_time_step
            graph_helper["next_num_obj"] = len_next_time_step

            # Tracks number of obj seen per time step. Used in debug/display purposes.
            graph_dict["time_num_obj"].append([t, len_time_step])

            step_info = time_df.to_dict('records')
            step_info = self._check_errors_step_info(step_info, graph_dict, graph_helper)
            step_info = self._handle_step_info(step_info, graph_dict, graph_helper)

            graph_helper["last_num_obj"] = len(step_info)

            for node in step_info:

                pred_id = int(node["predecessorID"])
                time_num = int(node["time_num"])
                node_name = "{}.{}".format(time_num, pred_id)

                graph_dict["graph"][node_name] = []
                pred_id_last_node_name = graph_helper["pred_id_last_node"][pred_id]

                graph_dict["graph"][node_name].append(pred_id_last_node_name)
                try:
                    graph_dict["graph"][pred_id_last_node_name].append(node_name)
                except KeyError:
                    print("Error Pred_Id_Last_Node_Name")
                    print(node)
                    print(graph_helper)
                    sys.exit()

                graph_helper["pred_id_last_node"][pred_id] = node_name

        for k in graph_dict["graph"]:
            vals = [float(v) for v in graph_dict["graph"][k]]
            vals = sorted(vals)
            vals = [str(round(v, 1)) for v in vals]
            graph_dict["graph"][k] = vals

        print("Unsafe FILL NA")
        df = df.fillna(1.0)

        return graph_dict, df
