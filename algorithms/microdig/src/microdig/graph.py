"""
Graph generation module for MicroDig.

This module handles the creation and manipulation of various graph structures
used in the MicroDig algorithm for microservice failure analysis.
"""

import time
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
import numpy as np
from rcabench_platform.v2.logging import logger
from scipy.stats import pearsonr

from .anomaly import AnomalyDetector
from .data_structures import CaseModel
from .utils import merge_callings


def timeit(comment: Optional[str] = None):
    """Decorator for timing function execution."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            func_name = comment or func.__name__
            logger.debug(f"{func_name} completed in {elapsed:.3f}s")
            return result

        return wrapper

    return decorator


def split_calling(name: str) -> Tuple[str, str]:
    """Split calling name into caller and callee parts."""
    parts = name.split("|")
    mid = len(parts) // 2
    caller = "|".join(parts[:mid])
    callee = "|".join(parts[mid:])
    return caller, callee


def get_connected_graph(G: nx.DiGraph, start_nodes: List[str]) -> nx.DiGraph:
    """Get connected subgraph starting from given nodes."""
    if not start_nodes:
        return nx.DiGraph()

    result_graph = nx.DiGraph()
    visited = set()

    # Forward traversal
    queue = deque(start_nodes)
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        for successor in G.successors(current):
            edge_data = G[current][successor]
            result_graph.add_node(current, **G.nodes.get(current, {}))
            result_graph.add_node(successor, **G.nodes.get(successor, {}))
            result_graph.add_edge(current, successor, **edge_data)
            queue.append(successor)

    # Backward traversal
    queue = deque(start_nodes)
    visited = set()
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        for predecessor in G.predecessors(current):
            edge_data = G[predecessor][current]
            result_graph.add_node(predecessor, **G.nodes.get(predecessor, {}))
            result_graph.add_node(current, **G.nodes.get(current, {}))
            result_graph.add_edge(predecessor, current, **edge_data)
            queue.append(predecessor)

    return result_graph


def get_sorted_values(data_dict: Dict[int, float], start: int, end: int) -> List[float]:
    """Get sorted values from dictionary within time range."""
    filtered = {k: v for k, v in data_dict.items() if start <= k < end}
    return [v for k, v in sorted(filtered.items())]


def calculate_data_rates(
    data: Dict[str, Any], time_keys: List[int]
) -> Tuple[Dict[int, float], Dict[int, float]]:
    """Calculate error rate and duration from data."""
    error_rate = {k: data["error_rate"].get(k, 0) for k in time_keys}
    duration = {k: data["duration"].get(k, 0) for k in time_keys}
    return error_rate, duration


def merge_callings_by_level(
    callings: Dict[str, Any], from_level: str, to_level: str
) -> Dict[str, Any]:
    """Merge callings from one level to another (method -> service -> server)."""
    if from_level == to_level:
        return callings

    import pandas as pd

    calling_df = pd.DataFrame(list(callings.values()))
    if calling_df.empty:
        return {}

    # Filter for appropriate calling patterns based on the target level
    if to_level == "service":
        # For service level, we want 4-part calling patterns (inter-service calls)
        filtered_callings = {}
        for name, data in callings.items():
            parts = name.split("|")
            if (
                len(parts) == 4
            ):  # caller_service|caller_method|callee_service|callee_method
                filtered_callings[name] = data

        if not filtered_callings:
            logger.warning(
                "No inter-service calling patterns found for service-level analysis"
            )
            return {}

        calling_df = pd.DataFrame(list(filtered_callings.values()))
        gb_cols = ["caller_service", "callee_service"]

        # Extract service names from the 4-part format
        for col in gb_cols:
            if col not in calling_df.columns:
                if col == "caller_service":
                    calling_df[col] = calling_df["name"].apply(
                        lambda x: x.split("|")[0]
                    )
                elif col == "callee_service":
                    calling_df[col] = calling_df["name"].apply(
                        lambda x: x.split("|")[2]
                    )

    elif to_level == "server":
        # For server level, extract server names from service names
        gb_cols = ["caller_server", "callee_server"]

        # First filter for 4-part patterns
        filtered_callings = {}
        for name, data in callings.items():
            parts = name.split("|")
            if len(parts) == 4:
                filtered_callings[name] = data

        if not filtered_callings:
            logger.warning(
                "No inter-service calling patterns found for server-level analysis"
            )
            return {}

        calling_df = pd.DataFrame(list(filtered_callings.values()))

        # Extract server names from service names (assume server = service for simplicity)
        for col in gb_cols:
            if col not in calling_df.columns:
                if col == "caller_server":
                    calling_df[col] = calling_df["name"].apply(
                        lambda x: x.split("|")[0]
                    )
                elif col == "callee_server":
                    calling_df[col] = calling_df["name"].apply(
                        lambda x: x.split("|")[2]
                    )
    else:
        raise ValueError(f"Unsupported to_level: {to_level}")

    return merge_callings(calling_df, gb_cols)


class GraphGenerator:
    """Generates various graph structures for MicroDig analysis."""

    def __init__(
        self,
        anomaly_detector: AnomalyDetector,
        hyper_params: Dict[str, Any],
        case: CaseModel,
    ):
        """
        Initialize graph generator.

        Args:
            anomaly_detector: Anomaly detection component
            hyper_params: Algorithm hyperparameters
            case: Case model with data
        """
        self.anomaly_detector = anomaly_detector
        self.hyper_params = hyper_params
        self.case = case

        # Calculate time windows
        self.sim_start = (
            case.alarm_start_minute - hyper_params["test_length_before"] + 1
        )
        self.sim_end = case.alarm_start_minute + hyper_params["test_length_after"]
        self.time_keys = list(
            range(self.sim_start - 1 - hyper_params["train_length"], self.sim_end + 1)
        )

        # Cache for generated graphs
        self._method_node_graph: Optional[nx.DiGraph] = None
        self._service_node_graph: Optional[nx.DiGraph] = None
        self._server_node_graph: Optional[nx.DiGraph] = None
        self._method_calling_node_graph: Optional[nx.DiGraph] = None
        self._asso_method_node_ano_graph: Optional[nx.DiGraph] = None
        self._asso_service_node_ano_graph: Optional[Tuple[nx.DiGraph, Dict]] = None
        self._mix_method_node_graph: Optional[nx.DiGraph] = None
        self._mix_server_node_graph: Optional[nx.DiGraph] = None

        # Additional state
        self.method_score_df = None

        logger.debug(f"GraphGenerator initialized for case {case.alarm_start_time}")

    def aggregate_data_list(
        self, data_list: List[Dict[str, Any]]
    ) -> Dict[str, Dict[int, float]]:
        """Aggregate multiple data dictionaries."""
        from collections import Counter

        aggregated = {}
        keys = ["error_rate", "duration"]

        for key in keys:
            counter = Counter({t: 0 for t in self.time_keys})
            for data_dict in data_list:
                if key in data_dict:
                    counter.update(data_dict[key])
            aggregated[key] = dict(counter)

        return aggregated

    @timeit("Building method node graph")
    def get_method_node_graph(self, require_data: bool = False) -> nx.DiGraph:
        """Get method-level node graph."""
        if self._method_node_graph is None:
            self._method_node_graph = self._build_node_graph(
                self.case.callings, require_edge_data=require_data
            )
        return self._method_node_graph

    @timeit("Building service node graph")
    def get_service_node_graph(self, require_data: bool = False) -> nx.DiGraph:
        """Get service-level node graph."""
        if self._service_node_graph is None:
            service_callings = merge_callings_by_level(
                self.case.callings, "method", "service"
            )
            self._service_node_graph = self._build_node_graph(
                service_callings, require_edge_data=require_data
            )
        return self._service_node_graph

    @timeit("Building server node graph")
    def get_server_node_graph(
        self, node_data_key: str = "data", edge_weight_key: str = "weight"
    ) -> nx.DiGraph:
        """Get server-level node graph."""
        if self._server_node_graph is not None:
            return self._server_node_graph

        # Get base anomaly graph based on level
        if self.hyper_params["level"] == "service":
            G_ano, service_callings = self.get_asso_service_node_ano_graph()
            callings = {
                f"{fro}|{to}": service_callings[f"{fro}|{to}"]
                for fro, to in G_ano.edges
            }
            merged_callings = merge_callings_by_level(callings, "service", "server")
        else:  # method level
            G_ano = self.get_asso_method_node_ano_graph()
            callings = {
                f"{fro}|{to}": self.case.callings[f"{fro}|{to}"]
                for fro, to in G_ano.edges
            }
            merged_callings = merge_callings_by_level(callings, "method", "server")

        # Build server graph with aggregated data
        as_callee = defaultdict(list)
        as_caller = defaultdict(list)
        G_out = nx.DiGraph()

        for name, data in merged_callings.items():
            caller, callee = split_calling(name)
            as_callee[callee].append(data)
            as_caller[caller].append(data)
            G_out.add_edge(caller, callee)

        # Add node data (aggregated from incoming and outgoing edges)
        for node in set(as_callee) | set(as_caller):
            node_data = self.aggregate_data_list(as_callee[node] + as_caller[node])
            G_out.nodes[node][node_data_key] = node_data

        # Add edge weights based on correlation
        for fro, to in G_out.edges:
            fro_data = G_out.nodes[fro][node_data_key]
            to_data = G_out.nodes[to][node_data_key]
            weight = 0

            for metric in ["duration", "error_rate"]:
                x_vals = get_sorted_values(
                    fro_data[metric], self.sim_start, self.sim_end
                )
                y_vals = get_sorted_values(
                    to_data[metric], self.sim_start, self.sim_end
                )

                if np.std(x_vals) != 0 and np.std(y_vals) != 0:
                    corr, _ = pearsonr(x_vals, y_vals)
                    weight = max(weight, abs(corr))

            G_out[fro][to][edge_weight_key] = weight

        self._server_node_graph = G_out
        return G_out

    @timeit("Building association method node anomaly graph")
    def get_asso_method_node_ano_graph(
        self, require_edge_data: bool = False
    ) -> nx.DiGraph:
        """Get association method node anomaly graph."""
        if self._asso_method_node_ano_graph is None:
            G = self._build_asso_node_graph(
                self.case.callings, require_edge_data=require_edge_data
            )
            G_ano = self._build_node_ano_graph(G)
            self._asso_method_node_ano_graph = G_ano
        return self._asso_method_node_ano_graph

    @timeit("Building association service node anomaly graph")
    def get_asso_service_node_ano_graph(
        self, require_edge_data: bool = False
    ) -> Tuple[nx.DiGraph, Dict]:
        """Get association service node anomaly graph."""
        if self._asso_service_node_ano_graph is None:
            callings = merge_callings_by_level(self.case.callings, "method", "service")
            G = self._build_asso_node_graph(
                callings, require_edge_data=require_edge_data
            )
            G_ano = self._build_node_ano_graph(G)
            self._asso_service_node_ano_graph = (G_ano, callings)
        return self._asso_service_node_ano_graph

    @timeit("Building method calling node graph")
    def get_method_calling_node_graph(
        self, data_key: str = "data", edge_weight_key: str = "weight"
    ) -> nx.DiGraph:
        """Get method calling node graph."""
        if self._method_calling_node_graph is None:
            G_ano = self.get_asso_method_node_ano_graph(require_edge_data=True)
            self._method_calling_node_graph = self._build_calling_node_graph(
                G_ano, node_data_key=data_key, edge_weight_key=edge_weight_key
            )
        return self._method_calling_node_graph

    @timeit("Building mixed server node graph")
    def get_mix_server_node_graph(self) -> nx.DiGraph:
        """Get mixed server node graph."""
        if self._mix_server_node_graph is not None:
            return self._mix_server_node_graph

        level = self.hyper_params["level"]

        if level == "service":
            G_ano, base_callings = self.get_asso_service_node_ano_graph()
        else:  # method
            G_ano = self.get_asso_method_node_ano_graph()
            base_callings = self.case.callings

        # Extract relevant callings
        callings = {
            f"{fro}|{to}": base_callings[f"{fro}|{to}"] for fro, to in G_ano.edges()
        }

        # Merge to server level
        merged_callings = merge_callings_by_level(callings, level, "server")

        self._mix_server_node_graph = self._build_mix_node_graph(merged_callings)
        return self._mix_server_node_graph

    @timeit("Building mixed server node graph without method detection")
    def get_mix_server_node_graph_without_method_detection(self) -> nx.DiGraph:
        """Get mixed server node graph without method-level detection."""
        if self._mix_server_node_graph is not None:
            return self._mix_server_node_graph

        # Merge directly to server level
        server_callings = merge_callings_by_level(
            self.case.callings, "method", "server"
        )
        G_asso = self._build_asso_node_graph(server_callings)
        G_ano = self._build_node_ano_graph(G_asso)

        # Extract relevant callings
        callings = {
            f"{fro}|{to}": server_callings[f"{fro}|{to}"] for fro, to in G_ano.edges()
        }

        self._mix_server_node_graph = self._build_mix_node_graph(callings)
        return self._mix_server_node_graph

    @timeit("Building association node graph")
    def _build_asso_node_graph(
        self,
        callings: Dict[str, Any],
        edge_score_key: str = "score",
        edge_similarity_key: str = "similarity",
        edge_data_key: str = "data",
        require_edge_data: bool = False,
    ) -> nx.DiGraph:
        """Build association node graph."""
        # Create full graph
        G_total = nx.DiGraph()
        for name in callings.keys():
            caller, callee = split_calling(name)
            G_total.add_edge(caller, callee)

        # Find nodes connected to alarm item
        start_server = self.case.alarm_item
        start_nodes = [node for node in G_total.nodes if start_server in node]

        # Get connected subgraph
        G = get_connected_graph(G_total, start_nodes) if start_nodes else G_total.copy()

        # Add edge attributes (anomaly scores, similarity, data)
        for fro, to in G.edges:
            name = f"{fro}|{to}"
            data = callings[name]

            # Calculate anomaly scores
            error_rate, duration = calculate_data_rates(data, self.time_keys)
            is_alarm = self.case.alarm_item in name
            scores = self.anomaly_detector.edge_score(
                self.case.alarm_start_minute, [error_rate, duration], is_alarm
            )

            edge_attrs = {edge_score_key: max(scores)}

            if require_edge_data:
                duration_vals = get_sorted_values(
                    duration, self.sim_start, self.sim_end
                )
                error_vals = get_sorted_values(error_rate, self.sim_start, self.sim_end)
                edge_attrs[edge_data_key] = {
                    "duration": np.array(duration_vals),
                    "error": np.array(error_vals),
                }

            G.add_edge(fro, to, **edge_attrs)

        return G

    @timeit("Building node graph")
    def _build_node_graph(
        self,
        callings: Dict[str, Any],
        edge_score_key: str = "score",
        edge_data_key: str = "data",
        require_edge_data: bool = False,
    ) -> nx.DiGraph:
        """Build basic node graph with anomaly scores."""
        G = nx.DiGraph()

        for name, data in callings.items():
            caller, callee = split_calling(name)

            # Calculate anomaly scores
            error_rate, duration = calculate_data_rates(data, self.time_keys)
            is_alarm = self.case.alarm_item in name
            scores = self.anomaly_detector.edge_score(
                self.case.alarm_start_minute, [error_rate, duration], is_alarm
            )

            edge_attrs = {edge_score_key: max(scores)}

            if require_edge_data:
                duration_vals = get_sorted_values(
                    duration, self.sim_start, self.sim_end
                )
                error_vals = get_sorted_values(error_rate, self.sim_start, self.sim_end)
                edge_attrs[edge_data_key] = {
                    "duration": np.array(duration_vals),
                    "error_rate": np.array(error_vals),
                }

            G.add_edge(caller, callee, **edge_attrs)

        return G

    @timeit("Building node anomaly graph")
    def _build_node_ano_graph(
        self, G: nx.DiGraph, ano_score_key: str = "score"
    ) -> nx.DiGraph:
        """Build anomaly subgraph from node graph."""
        G_ano = nx.DiGraph()

        # Filter edges with non-zero anomaly scores
        for fro, to, data in G.edges(data=True):
            if data.get(ano_score_key, 0) != 0:
                G_ano.add_edge(fro, to, **data)

        if len(G_ano.edges) == 0:
            return G.copy()

        # Get connected component containing alarm item
        start_server = self.case.alarm_item
        start_nodes = [node for node in G_ano.nodes if start_server in node]
        return get_connected_graph(G_ano, start_nodes) if start_nodes else G_ano.copy()

    @timeit("Building calling node graph")
    def _build_calling_node_graph(
        self,
        G: nx.DiGraph,
        corr_method: str = "pearson",
        node_data_key: str = "data",
        edge_weight_key: str = "weight",
    ) -> nx.DiGraph:
        """Build calling node graph (nodes are edges from original graph)."""
        # Build skeleton without weights
        G_out = self._build_calling_node_graph_skeleton(G)

        # Add edge weights based on correlation
        for start, end in G_out.edges():
            x_data = G_out.nodes[start][node_data_key]
            y_data = G_out.nodes[end][node_data_key]

            corr_val = 0
            if corr_method == "pearson":
                for metric in ["duration", "error_rate"]:
                    x_vals = x_data[metric]
                    y_vals = y_data[metric]

                    if np.std(x_vals) != 0 and np.std(y_vals) != 0:
                        corr, _ = pearsonr(x_vals, y_vals)
                        corr_val = max(corr_val, abs(corr))

            G_out[start][end][edge_weight_key] = corr_val

        return G_out

    def _build_calling_node_graph_skeleton(self, G: nx.DiGraph) -> nx.DiGraph:
        """Build skeleton of calling node graph."""
        start_server = self.case.alarm_item
        start_nodes = [node for node in G.nodes if start_server in node]

        G_out = nx.DiGraph()

        # Find initial calling edges connected to alarm nodes
        callings_set = set()
        for end_node in start_nodes:
            for caller in G.predecessors(end_node):
                callings_set.add(f"{caller}|{end_node}")

        # If no predecessors, start with successors
        if not callings_set:
            for start_node in start_nodes:
                for callee in G.successors(start_node):
                    callings_set.add(f"{start_node}|{callee}")

        # Breadth-first search upstream
        queue = deque(callings_set)
        visited = set()

        while queue:
            end_calling = queue.popleft()
            caller, callee = split_calling(end_calling)

            # Add current calling as node
            G_out.add_node(end_calling, **G[caller][callee])

            # Add predecessor callings
            for grandparent in G.predecessors(caller):
                start_calling = f"{grandparent}|{caller}"
                edge_key = f"{start_calling}|{end_calling}"

                if edge_key not in visited:
                    visited.add(edge_key)
                    G_out.add_node(start_calling, **G[grandparent][caller])
                    G_out.add_edge(start_calling, end_calling)
                    queue.append(start_calling)

        # Breadth-first search downstream
        queue = deque(callings_set)
        visited = set()

        while queue:
            start_calling = queue.popleft()
            caller, callee = split_calling(start_calling)

            # Add current calling as node
            G_out.add_node(start_calling, **G[caller][callee])

            # Add successor callings
            for grandchild in G.successors(callee):
                end_calling = f"{callee}|{grandchild}"
                edge_key = f"{start_calling}|{end_calling}"

                if edge_key not in visited:
                    visited.add(edge_key)
                    G_out.add_node(end_calling, **G[callee][grandchild])
                    G_out.add_edge(start_calling, end_calling)
                    queue.append(end_calling)

        return G_out

    @timeit("Building mixed node graph")
    def _build_mix_node_graph(
        self,
        callings: Dict[str, Any],
        node_data_key: str = "data",
        edge_weight_key: str = "weight",
    ) -> nx.DiGraph:
        """Build mixed node graph combining calling nodes and server nodes."""
        # Build base node graph
        G = self._build_node_graph(callings, require_edge_data=True)

        # Build calling node graph
        G_mix = self._build_calling_node_graph(
            G,
            corr_method="pearson",
            node_data_key=node_data_key,
            edge_weight_key=edge_weight_key,
        )

        # Prepare server data aggregation
        as_callee = defaultdict(list)
        as_caller = defaultdict(list)

        for name, data in callings.items():
            caller, callee = split_calling(name)
            as_callee[callee].append(data)
            as_caller[caller].append(data)

        # Add server nodes and mix edges
        calling_nodes = list(G_mix.nodes)
        for calling_node in calling_nodes:
            caller, callee = split_calling(calling_node)

            # Add server nodes if not present
            if caller not in G_mix.nodes:
                caller_data = self.aggregate_data_list(
                    as_caller[caller] + as_callee[caller]
                )
                G_mix.add_node(caller, type="item", data=caller_data)

            if callee not in G_mix.nodes:
                callee_data = self.aggregate_data_list(
                    as_caller[callee] + as_callee[callee]
                )
                G_mix.add_node(callee, type="item", data=callee_data)

            # Add mix edges (calling -> server nodes)
            G_mix.add_edge(calling_node, caller, type="mix")
            G_mix.add_edge(calling_node, callee, type="mix")

        # Calculate weights for mix edges
        self._calculate_mix_edge_weights(G_mix, node_data_key, edge_weight_key)

        return G_mix

    def _calculate_mix_edge_weights(
        self, G_mix: nx.DiGraph, node_data_key: str, edge_weight_key: str
    ) -> None:
        """Calculate weights for mix edges."""
        server_scores = {}
        new_col = self.hyper_params["new_col"]
        beta = self.hyper_params["beta"]

        # Get server scores from method scores if available
        if (
            beta != 0.0
            and self.method_score_df is not None
            and len(self.method_score_df) != 0
        ):
            for server, group in self.method_score_df.groupby("server"):
                server_scores[server] = group[new_col].max()

        # Calculate weights for each calling node
        for node in G_mix.nodes:
            if G_mix.nodes[node].get("type") == "item":
                continue

            caller, callee = split_calling(node)

            # Calculate base weight from incoming/outgoing edges
            in_weights = [
                data.get(edge_weight_key, 0)
                for _, _, data in G_mix.in_edges(node, data=True)
            ]
            out_weights = [
                data.get(edge_weight_key, 0)
                for _, _, data in G_mix.out_edges(node, data=True)
                if data.get("type") != "mix"
            ]

            max_in = max(in_weights) if in_weights else 0
            max_out = max(out_weights) if out_weights else 0

            total_weight = max(0, max_in - max_out)
            if max_in == 0 and max_out == 0:
                total_weight = 1
            elif max_in == 0:
                total_weight = 1 - max_out
            elif max_out == 0:
                total_weight = max_in

            # Distribute weight between caller and callee
            if self.hyper_params.get("server_data", False):
                # Use correlation-based distribution
                self._calculate_correlation_based_weights(
                    G_mix,
                    node,
                    caller,
                    callee,
                    total_weight,
                    node_data_key,
                    edge_weight_key,
                )
            else:
                # Use score-based distribution
                if beta != 0.0:
                    caller_score = server_scores.get(caller, 0)
                    callee_score = server_scores.get(callee, 0)
                    if caller_score > callee_score:
                        caller_w, callee_w = 0.5 + beta, 0.5 - beta
                    else:
                        caller_w, callee_w = 0.5 - beta, 0.5 + beta
                else:
                    caller_w, callee_w = 0.5, 0.5

                G_mix[node][caller][edge_weight_key] = total_weight * caller_w
                G_mix[node][callee][edge_weight_key] = total_weight * callee_w

    def _calculate_correlation_based_weights(
        self,
        G_mix: nx.DiGraph,
        calling_node: str,
        caller: str,
        callee: str,
        total_weight: float,
        node_data_key: str,
        edge_weight_key: str,
    ) -> None:
        """Calculate correlation-based weights for mix edges."""
        calling_data = G_mix.nodes[calling_node][node_data_key]
        caller_data = G_mix.nodes[caller]["data"]
        callee_data = G_mix.nodes[callee]["data"]

        caller_corr = 0
        callee_corr = 0

        for metric in ["error_rate", "duration"]:
            x_vals = get_sorted_values(
                calling_data[metric], self.sim_start, self.sim_end
            )
            caller_vals = get_sorted_values(
                caller_data[metric], self.sim_start, self.sim_end
            )
            callee_vals = get_sorted_values(
                callee_data[metric], self.sim_start, self.sim_end
            )

            if np.std(x_vals) != 0:
                if np.std(caller_vals) != 0:
                    corr, _ = pearsonr(x_vals, caller_vals)
                    caller_corr = max(caller_corr, abs(corr))

                if np.std(callee_vals) != 0:
                    corr, _ = pearsonr(x_vals, callee_vals)
                    callee_corr = max(callee_corr, abs(corr))

        # Distribute weight based on correlations
        if caller_corr == 0 and callee_corr == 0:
            G_mix[calling_node][caller][edge_weight_key] = total_weight * 0.5
            G_mix[calling_node][callee][edge_weight_key] = total_weight * 0.5
        else:
            total_corr = caller_corr + callee_corr
            G_mix[calling_node][caller][edge_weight_key] = (
                total_weight * caller_corr / total_corr
            )
            G_mix[calling_node][callee][edge_weight_key] = (
                total_weight * callee_corr / total_corr
            )
