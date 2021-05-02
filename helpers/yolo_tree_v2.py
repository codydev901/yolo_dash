
"""
Note: Currently some overlap here w/ YoloPlotV2 5/2/2021
"""


class YoloTreeTwo:

    def __init__(self, graph_info):
        self.trap_num = graph_info["trap_num"]
        self.tree_info = {}
        self._on_init(graph_info)

    def _on_init(self, graph_info):
        """
        Root function for initialization.
        """

        nodes = list(graph_info["graph"].keys())
        all_pred_ids = [int(v.split(".")[-1]) for v in nodes]
        min_pred_id, max_pred_id = min(all_pred_ids), max(all_pred_ids)

        # Establish which nodes are active at each time stamp
        self.tree_info["pred_id_time_num"] = {k: [] for k in range(min_pred_id, max_pred_id + 1)}
        for node in graph_info["graph"]:
            time_num, pred_id = node.split(".")
            time_num = int(time_num)
            pred_id = int(pred_id)
            self.tree_info["pred_id_time_num"][pred_id].append(time_num)

        self._make_pred_id_rls_raw()

    def _make_pred_id_rls_raw(self):
        """
        Doc Doc Doc
        """

        self.tree_info["pred_id_rls_raw"] = {}

        for pred_id in self.tree_info["pred_id_time_num"]:

            active_time_nums = self.tree_info["pred_id_time_num"][pred_id]

            # Branch Chunks
            branch_chunks = []
            current_chunk = [active_time_nums[0]]
            last_time_num = active_time_nums[0]
            for time_num in active_time_nums[1:]:

                # Check if current time_num is += 1 of last time_num. If so, add to current chunk
                if time_num - 1 == last_time_num:
                    current_chunk.append(time_num)
                    last_time_num = time_num
                    continue

                # Start new chunk, add existing to branch chunks before clearing
                branch_chunks.append(current_chunk.copy())
                current_chunk = [time_num]
                last_time_num = time_num

            # Add the last one
            branch_chunks.append(current_chunk.copy())

            self.tree_info["pred_id_rls_raw"][pred_id] = branch_chunks

    def get_rls_info(self):
        """
        Doc Doc Doc
        """

        rls_info = [["trap_num", "pred_id", "time_start", "time_end"]]

        for pred_id in self.tree_info["pred_id_time_num"]:

            rls_raw = self.tree_info["pred_id_rls_raw"][pred_id]

            for chunk in rls_raw:

                rls_info.append([self.trap_num, pred_id, chunk[0], chunk[-1]])

        return rls_info


