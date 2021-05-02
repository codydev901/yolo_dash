import plotly.graph_objects as go

"""
Doc Doc Doc
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
            "10": {"symbol": "#4000ff", "line": "rgb(64, 0, 255)"},  # Light Purple
            "11": {"symbol": "#000000", "line": "rgb(0, 0, 0)"},
            "12": {"symbol": "#ff0000", "line": "rgb(255, 0, 0)"},
            "13": {"symbol": "#00ff00", "line": "rgb(0, 255, 0)"},
            "14": {"symbol": "#0000ff", "line": "rgb(0, 0, 255)"},
            "15": {"symbol": "#ff8000", "line": "rgb(255, 128, 0)"},
            "16": {"symbol": "#00ff80", "line": "rgb(0, 255, 128)"},
            "17": {"symbol": "#0080ff", "line": "rgb(128, 0, 255)"},
            "18": {"symbol": "#ff4000", "line": "rgb(255, 64, 0)"},
            "19": {"symbol": "#00ff40", "line": "rgb(0, 255, 64)"},
            "20": {"symbol": "#4000ff", "line": "rgb(64, 0, 255)"}}


class YoloPlotTwo:

    def __init__(self, graph_info):
        self.graph_info = graph_info
        self.fig = go.Figure()
        self.plot_info = {}
        self._on_init()

    def _on_init(self):
        """
        Doc Doc Doc
        """

        self._make_plot_info()

        self.fig.update_xaxes(range=self.plot_info["x_bounds"])
        self.fig.update_yaxes(range=self.plot_info["y_bounds"])
        self.fig.update_layout(showlegend=True)
        self.fig.layout.title["text"] = "TrapNum:{} TStop:{}".format(self.graph_info["trap_num"],
                                                                     self.graph_info["t_stop"])

        self.fig.layout.yaxis["title"] = "Pred Id"
        self.fig.layout.yaxis["dtick"] = 1
        self.fig.layout.xaxis["title"] = "Time Num"

        for pred_id in self.plot_info["pred_id_time_num"]:
            node_points = self._get_node_points(pred_id)
            self._add_traces(node_points)

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

    def _make_plot_info(self):
        """
        Doc Doc Doc
        """

        nodes = list(self.graph_info["graph"].keys())
        start_time_num = int(nodes[0].split(".")[0])
        end_time_num = int(nodes[-1].split(".")[0])
        all_pred_ids = [int(v.split(".")[-1]) for v in nodes]
        min_pred_id, max_pred_id = min(all_pred_ids), max(all_pred_ids)

        # X Correlates to time_num
        self.plot_info["x_bounds"] = [start_time_num-1, end_time_num+1]

        # Y Correlates to pred_id
        self.plot_info["y_bounds"] = [min_pred_id-1, max_pred_id+1]

        # Establish Which Nodes are active at each time stamp
        self.plot_info["pred_id_time_num"] = {k: [] for k in range(min_pred_id, max_pred_id+1)}
        for node in self.graph_info["graph"]:
            time_num, pred_id = node.split(".")
            time_num = int(time_num)
            pred_id = int(pred_id)
            self.plot_info["pred_id_time_num"][pred_id].append(time_num)

    def _get_node_points(self, pred_id):
        """
        Doc Doc Doc
        """

        res = []

        trace_info = self._make_trace_info()
        trace_info["x"] = []
        trace_info["y"] = []
        trace_info["labels"] = []
        trace_info["name"] = "PredID_{}".format(pred_id)
        trace_info["mode"] = "markers"
        trace_info["size"] = 4
        trace_info["symbol"] = "circle"
        trace_info["color"] = COLOR_LU[str(pred_id)]["symbol"]
        trace_info["line_color"] = COLOR_LU[str(pred_id)]["line"]

        for time_num in self.plot_info["pred_id_time_num"][pred_id]:
            trace_info["x"].append(time_num)
            trace_info["y"].append(pred_id)
            trace_info["labels"].append("{}.{}".format(time_num, pred_id))

        res.append(trace_info)

        return res

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
