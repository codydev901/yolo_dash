import plotly.graph_objects as go
import sys
import math

"""

XN [-1.0, -1.0, -1.0, -1.0, 0.0, 0.0, 1.0, 0.0, 1.0]
Yn [4.0, 5.0, 6.0, 7.0, 8.0, 7.0, 7.0, 6.0, 6.0]
traces ['1.1', '2.1', '3.1', '4.1', '5.1', '6.1', '6.2', '7.1', '7.2']

fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

could try shapes https://plotly.com/python/shapes/?

FLOW

1. Add Root Node Lines

https://www.w3schools.com/colors/colors_picker.asp

"""

COLOR_LU = {"1": {"symbol": "#000000", "line": "rgb(0, 0, 0)"},      # Black
            "2": {"symbol": "#ff0000", "line": "rgb(255, 0, 0)"},    # Red
            "3": {"symbol": "#00ff00", "line": "rgb(0, 255, 0)"},    # Green
            "4": {"symbol": "#0000ff", "line": "rgb(0, 0, 255)"},    # Blue
            "5": {"symbol": "#ff8000", "line": "rgb(255, 128, 0)"},  # Orange
            "6": {"symbol": "#00ff80", "line": "rgb(0, 255, 128)"},  # Md Green
            "7": {"symbol": "#0080ff", "line": "rgb(128, 0, 255)"},  # Purple
            "8": {"symbol": "#ff4000", "line": "rgb(255, 64, 0)"},   # Light Orange
            "9": {"symbol": "#00ff40", "line": "rgb(0, 255, 64)"},   # Light Green
            "10": {"symbol": "#4000ff", "line": "rgb(64, 0, 255)"}}  # Light Purple


class YoloPlot:

    def __init__(self, yolo_tree, graph_info):
        self.yolo_tree = yolo_tree
        self.graph_info = graph_info
        self.fig = go.Figure()
        self.plot_info = {}
        self._on_init()

    def _on_init(self):
        """
        Doc Doc Doc
        """

        self._plot_info_from_tree_dict()
        self.fig.update_xaxes(range=[0.0, float(self.plot_info["x_bound"])])
        self.fig.update_yaxes(range=[0.0, float(self.plot_info["y_bound"])])
        self.fig.layout.title["text"] = "TrapNum:{} TStop:{}".format(self.graph_info["trap_num"],
                                                                     self.graph_info["t_stop"])

        # Root Node Position(s)
        self.plot_info["root_pos"] = {}
        self._establish_root_positions()

        # Root Lines(s)
        root_lines = self._get_root_lines()
        self._add_traces(root_lines)

        # Root Branch Lines(s)
        root_branch_lines = self._get_root_branch_lines()
        self._add_traces(root_branch_lines)

        # # Daughter Branch Lines(s)
        # daughter_trace = self._get_daughter_branch_traces()
        # for d_t in daughter_trace:
        #     self.add_trace(d_t, mode="lines")
        #
        # # Branch and Leaf Points
        # branch_leaf_points = self._get_branch_leaf_points(daughter_trace)
        # for b_p in branch_leaf_points:
        #     self.add_trace(b_p, mode="markers+text", size=32)
        #
        # # # Time Num Obj
        # time_num_obj_trace = self._get_time_num_traces()
        # self.add_trace(time_num_obj_trace, symbol="square", mode="text", size=36)

    @staticmethod
    def _make_trace_info():
        """
        Doc Doc Doc
        """

        trace_info = dict()
        trace_info["x"] = []
        trace_info["y"] = []
        trace_info["labels"] = []
        trace_info["name"] = ""
        trace_info["mode"] = "markers"
        trace_info["size"] = 12
        trace_info["symbol"] = "circle"
        trace_info["color"] = "#000000"
        trace_info["line_color"] = "rgb(0, 0, 0)"

        return trace_info

    def _plot_info_from_tree_dict(self):
        """
        Doc Doc Doc
        """

        # print("PLOT INFO")
        # print(len(self.graph_info["time_num_obj"]))

        # To Establish X Bounds, check for max length of main branches
        # max_main_branch_length = 0
        # for n in self.yolo_tree.tree_info["root_nodes"]:
        #     main_branch_length = len(self.yolo_tree.tree_dict[n])
        #     if main_branch_length > max_main_branch_length:
        #         max_main_branch_length = main_branch_length

        # To Establish Y bounds, check for max length of daughter branches
        daughter_nodes = [n for n in self.yolo_tree.tree_dict if n not in self.yolo_tree.tree_info["root_nodes"]]
        max_daughter_branch_length = 0
        for n in daughter_nodes:
            daughter_branch_length = len(self.yolo_tree.tree_dict[n])
            if daughter_branch_length > max_daughter_branch_length:
                max_daughter_branch_length = daughter_branch_length

        self.plot_info["x_bound"] = len(self.graph_info["time_num_obj"]) + 3
        self.plot_info["y_bound"] = (max_daughter_branch_length + 2) * 2

    def _establish_root_positions(self):
        """
        Doc Doc Doc
        """

        num_root = len(self.yolo_tree.tree_info["root_nodes"])
        y_offset = self.plot_info["y_bound"] / (num_root + 1)
        for i, n in enumerate(self.yolo_tree.tree_info["root_nodes"]):
            x = float(n.split(".", 1)[0])
            y = (i + 1) * y_offset  # Fix this when multiple root nodes...
            self.plot_info["root_pos"][n] = {"x": x, "y": y}

    def _get_root_lines(self):
        """
        Doc Doc Doc
        """

        traces = []

        for r_n in self.yolo_tree.tree_info["root_nodes"]:

            trace_info = self._make_trace_info()
            pred_id = r_n[-1]
            trace_info["name"] = "{}_root_lines".format(pred_id)
            trace_info["mode"] = "markers+lines"
            trace_info["color"] = COLOR_LU[pred_id]["symbol"]
            trace_info["line_color"] = COLOR_LU[pred_id]["line"]

            x = self.plot_info["root_pos"][r_n]["x"]
            y = self.plot_info["root_pos"][r_n]["y"]
            trace_info["x"].append(x)
            trace_info["y"].append(y)
            trace_info["labels"].append(r_n)
            # Add Continuous Nodes
            for n in self.yolo_tree.tree_dict[r_n]:
                x = float(n.split(".", 1)[0])
                y = self.plot_info["root_pos"][r_n]["y"]
                trace_info["x"].append(x)
                trace_info["y"].append(y)
                trace_info["labels"].append(n)

            traces.append(trace_info)

        return traces

    def _get_root_branch_lines(self):
        """
        Doc Doc Doc
        """

        traces = []

        # Iterate Through Root Nodes
        for r_n in self.yolo_tree.tree_info["root_nodes"]:

            y_multiplier = 1  # Alternates

            root_y = self.plot_info["root_pos"][r_n]["y"]
            y_branch_offset = ((self.plot_info["y_bound"] - root_y) / 4)

            # Get Main Branch For That Root
            root_branch_nodes = self.yolo_tree.tree_dict[r_n]
            # Iterate Through Branch Nodes
            for branch_node in self.yolo_tree.tree_info["branch_nodes"]:
                # Keep only branch nodes that branch off the main branch
                if branch_node not in root_branch_nodes:
                    continue

                # Find The Edge
                edge_node = None
                for branch_edge in self.yolo_tree.tree_info["branch_edges"]:
                    if branch_edge[0] == branch_node:
                        edge_node = branch_edge[1]
                        break

                trace_info = self._make_trace_info()
                pred_id = edge_node[-1]
                trace_info["name"] = "{}_root_lines".format(pred_id)
                trace_info["mode"] = "markers+lines"
                trace_info["color"] = COLOR_LU[pred_id]["symbol"]
                trace_info["line_color"] = COLOR_LU[pred_id]["line"]

                # Add Branch Node Connection
                x = int(branch_node.split(".", 1)[0])
                y = root_y
                trace_info["x"].append(x)
                trace_info["y"].append(y)
                trace_info["labels"].append(branch_node)

                # Set an additional offset based on number of daughter nodes
                y_additive_offset = len(self.yolo_tree.tree_dict[edge_node]) / 2

                # Add Edge Node Connection
                x = int(edge_node.split(".", 1)[0])
                y = root_y + (y_branch_offset * y_multiplier) + (y_additive_offset * y_multiplier)
                trace_info["x"].append(x)
                trace_info["y"].append(y)
                trace_info["labels"].append(edge_node)

                # Add nodes in daughter branch
                for daughter_node in self.yolo_tree.tree_dict[edge_node]:
                    x = int(daughter_node.split(".", 1)[0])
                    y = root_y + (y_branch_offset * y_multiplier) + (y_additive_offset * y_multiplier)
                    trace_info["x"].append(x)
                    trace_info["y"].append(y)
                    trace_info["labels"].append(daughter_node)

                    # Check if one of these nodes is a sub_branch... # NOTE NEED TO REWORK THIS, BUT KINDA WORKS.
                    # d_y_multiplier = 1
                    if daughter_node in self.yolo_tree.tree_info["branch_nodes"]:

                        # Find The Edge
                        d_edge_node = None
                        for d_branch_edge in self.yolo_tree.tree_info["branch_edges"]:
                            if d_branch_edge[0] == daughter_node:
                                d_edge_node = d_branch_edge[1]
                                break

                        trace_info_d = self._make_trace_info()
                        pred_id_d = d_edge_node[-1]
                        trace_info_d["name"] = "{}_daughter_lines".format(pred_id)
                        trace_info_d["mode"] = "markers+lines"
                        trace_info_d["color"] = COLOR_LU[pred_id_d]["symbol"]
                        trace_info_d["line_color"] = COLOR_LU[pred_id_d]["line"]

                        # Add Daughter Branch Node Connection
                        d_x = x
                        d_y = y
                        trace_info_d["x"].append(d_x)
                        trace_info_d["y"].append(d_y)
                        trace_info_d["labels"].append(daughter_node)

                        # Add Edge Node Connection
                        d_x = int(d_edge_node.split(".", 1)[0])
                        d_y = (y + (y_branch_offset / 2)*y_multiplier)
                        trace_info_d["x"].append(d_x)
                        trace_info_d["y"].append(d_y)
                        trace_info_d["labels"].append(d_edge_node)

                        # Add Branch Daughter Nodes
                        for d_daughter_node in self.yolo_tree.tree_dict[d_edge_node]:
                            d_x = int(d_daughter_node.split(".", 1)[0])
                            d_y = (y + (y_branch_offset / 2)*y_multiplier)
                            trace_info_d["x"].append(d_x)
                            trace_info_d["y"].append(d_y)
                            trace_info_d["labels"].append(d_daughter_node)

                        traces.append(trace_info_d)

                y_multiplier *= -1
                traces.append(trace_info)

        return traces

    def _get_branch_leaf_points(self, daughter_traces):
        """
        Doc Doc Doc
        """

        res = []

        for d_t in daughter_traces:
            x_arr = []
            y_arr = []
            labels = []
            # Parent Point
            x_arr += [d_t["x"][0]]
            y_arr += [d_t["y"][0]]
            labels += [d_t["labels"][0]]
            # Daughter Point
            x_arr += [d_t["x"][1]]
            y_arr += [d_t["y"][1]]
            labels += [d_t["labels"][1]]
            # Leaf Point
            x_arr += [d_t["x"][-1]]
            y_arr += [d_t["y"][-1]]
            labels += [d_t["labels"][-1]]

            res.append({"x": x_arr, "y": y_arr, "labels": labels, "color": "#FFA500", "name": "dC"})

        return res

    def _get_time_num_traces(self):
        """
        Doc Doc Doc
        """

        x_arr = []
        y_arr = []
        labels = []

        for t_n in self.graph_info["time_num_obj"]:
            x = float(t_n[0])
            y = 1.0
            x_arr.append(x)
            y_arr.append(y)
            labels.append(t_n[1])

        return {"x": x_arr, "y": y_arr, "labels": labels, "color": "#008000", "name": "mC"}

    def _add_traces(self, traces):
        """
        Doc Doc Doc
        """

        for trace_info in traces:

            self.fig.add_trace(go.Scatter(x=trace_info["x"],
                                          y=trace_info["y"],
                                          mode=trace_info["mode"],
                                          name=trace_info["name"],
                                          marker=dict(symbol=trace_info["symbol"],
                                                      size=trace_info["size"],
                                                      color=trace_info["color"],
                                                      line=dict(color='rgb(0,0,0)', width=0.5)
                                                      ),
                                          text=trace_info["labels"],
                                          textfont=dict(color='#000000'),
                                          hoverinfo='text',
                                          opacity=0.8
                                          ))

    def show(self):

        self.fig.show()