
"""
Doc Doc Doc
"""


class YoloTree:

    def __init__(self, graph_info):
        self.graph_dict = {}
        self.tree_dict = {}
        self.tree_info = {}
        self._on_init(graph_info)

    def _on_init(self, graph_info):
        """
        Root function for initialization.
        """

        self.graph_dict = graph_info["graph"]
        self.tree_info["root_nodes"] = graph_info["root_nodes"]
        self.tree_info["branch_nodes"] = graph_info["branch_nodes"]
        self.tree_info["branch_edges"] = []

        self._populate_branch_edges()
        self._populate_tree_dict()

    def _populate_branch_edges(self):
        """
        Doc Doc Doc
        """

        for branch_node in self.tree_info["branch_nodes"]:
            edges = self.graph_dict[branch_node]
            for e in edges:
                if e[-1] != branch_node[-1]:
                    self.tree_info["branch_edges"].append([branch_node, e])
                    # break

    def _populate_tree_dict(self):
        """
        Doc Doc Doc
        """

        branch_nodes = list(self.tree_info["root_nodes"])

        for branch_edge in self.tree_info["branch_edges"]:
            branch_nodes.append(branch_edge[-1])

        branch_nodes = [float(v) for v in branch_nodes]
        branch_nodes = sorted(branch_nodes)
        branch_nodes = [str(round(v, 1)) for v in branch_nodes]

        self.tree_dict = {n: [] for n in branch_nodes}

        for node in self.graph_dict:

            # print(node)

            if node in branch_nodes:
                continue

            edges = self.graph_dict[node]
            parent_node = edges[0]

            if parent_node in self.tree_dict:
                self.tree_dict[parent_node].append(node)
                continue

            for branch_node in self.tree_dict:
                try:
                    last_continue_node = self.tree_dict[branch_node][-1]
                except IndexError:
                    print("INDEX ERROR", branch_node)
                    continue
                if last_continue_node == parent_node:
                    self.tree_dict[branch_node].append(node)
                    break
