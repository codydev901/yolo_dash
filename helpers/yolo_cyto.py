import csv


class YoloCyto:

    def __init__(self, graph_info):
        self.graph_info = graph_info

    def to_cytoscape_network_csv(self):

        res = [["source", "target", "interaction", "directed", "symbol", "value"]]
        has_parsed = []
        for source_node in self.graph_info["graph"]:
            for target_node in self.graph_info["graph"][source_node]:
                if target_node in has_parsed:
                    continue
                symbol = source_node
                value = 1.0
                directed = True
                interaction = "pp"
                if source_node in self.graph_info["root_nodes"]:
                    directed = False

                res.append([source_node, target_node, interaction, directed, symbol, value])
                has_parsed.append(source_node)

        with open("cytoscape_output/{}_{}_{}_cytoscape_network.csv".format(self.graph_info["file_name"],
                                                                           self.graph_info["trap_num"],
                                                                           self.graph_info["t_stop"]), "w") as w_file:
            writer = csv.writer(w_file, delimiter=",")
            for row in res:
                writer.writerow(row)


