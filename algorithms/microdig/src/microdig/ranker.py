"""
Ranking algorithms for MicroDig.

This module provides various ranking algorithms to identify potential
root causes in microservice failure scenarios.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from rcabench_platform.v2.logging import logger

from .data_structures import CaseModel
from .graph import GraphGenerator


def pagerank(G: nx.DiGraph, weight: str = "weight") -> Dict[str, float]:
    """Calculate PageRank scores for nodes in graph."""
    try:
        pr = nx.pagerank(G, weight=weight)
    except nx.PowerIterationFailedConvergence:
        try:
            pr = nx.pagerank_numpy(G, weight=weight)
        except nx.PowerIterationFailedConvergence:
            logger.warning("PageRank failed to converge, using equal scores")
            n_nodes = len(G.nodes)
            pr = {n: 1 / n_nodes for n in G.nodes}
    return pr


def random_walk(
    G: nx.DiGraph,
    start_nodes: Dict[str, float],
    weight: str = "weight",
    iters: int = 1000,
) -> Dict[str, float]:
    """
    Perform random walk on graph.

    Args:
        G: Directed graph
        start_nodes: Starting nodes with initial probabilities
        weight: Edge weight attribute
        iters: Number of iterations

    Returns:
        Dictionary mapping nodes to visit probabilities
    """
    if not start_nodes:
        return {n: 0.0 for n in G.nodes}

    # Initialize starting probability vector
    node_list = list(G.nodes)
    v_s = np.zeros(len(node_list))

    for i, node in enumerate(node_list):
        if node in start_nodes:
            v_s[i] = start_nodes[node]

    if np.sum(v_s) > 0:
        v_s = v_s / np.sum(v_s)
    else:
        # Uniform distribution if no valid start nodes
        v_s = np.ones(len(node_list)) / len(node_list)

    # Create transition probability matrix
    try:
        p_mat = nx.to_numpy_array(G, nodelist=node_list, weight=weight)
        # Normalize rows (outgoing edges)
        row_sums = np.sum(p_mat, axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        p_mat = p_mat / row_sums
    except Exception as e:
        logger.warning(f"Error creating transition matrix: {e}")
        return {n: 1 / len(node_list) for n in node_list}

    # Perform random walk
    np.random.seed(2022)
    steps = min(50, len(G.nodes))
    visit_counts = np.zeros(len(node_list))

    for _ in range(iters):
        # Choose starting node
        try:
            current_idx = np.random.choice(len(node_list), p=v_s)
        except ValueError:
            current_idx = 0

        # Perform walk
        for _ in range(steps):
            visit_counts[current_idx] += 1
            try:
                current_idx = np.random.choice(len(node_list), p=p_mat[current_idx])
            except ValueError:
                # No outgoing edges, stop walk
                break

    # Normalize visit counts
    total_visits = np.sum(visit_counts)
    if total_visits > 0:
        visit_probs = visit_counts / total_visits
    else:
        visit_probs = np.ones(len(node_list)) / len(node_list)

    return dict(zip(node_list, visit_probs))


def last2_anomaly_hop_search(
    G_ano: nx.DiGraph,
    start_server: str,
    sim_threshold: float = 0.7,
    sim_key: str = "similarity",
) -> List[str]:
    """Search for anomalous nodes using last-2 hop strategy."""
    start_nodes = [n for n in G_ano.nodes if start_server in n]
    queue = deque(start_nodes)
    remaining_nodes = set()
    end_nodes = set()

    while queue:
        current = queue.popleft()
        successors = list(G_ano.successors(current))

        if not successors:
            end_nodes.add(current)
            continue

        for successor in successors:
            edge_data = G_ano[current][successor]
            if edge_data.get(sim_key, 0) > sim_threshold:
                queue.append(successor)
                remaining_nodes.add(current)
                remaining_nodes.add(successor)

    # Include predecessors of end nodes
    result = end_nodes.copy()
    for end_node in end_nodes:
        for predecessor in G_ano.predecessors(end_node):
            if predecessor in remaining_nodes:
                result.add(predecessor)

    return list(result)


def deepest2_anomaly_hop_search(
    G_ano: nx.DiGraph,
    start_server: str,
    sim_threshold: float = 0.7,
    sim_key: str = "similarity",
) -> List[str]:
    """Search for anomalous nodes using deepest-2 strategy."""
    start_nodes = [n for n in G_ano.nodes if start_server in n]
    queue = deque(start_nodes)
    node_depths = {n: 0 for n in start_nodes}

    # BFS to find depths
    while queue:
        current = queue.popleft()
        current_depth = node_depths[current]

        for successor in G_ano.successors(current):
            edge_data = G_ano[current][successor]
            if edge_data.get(sim_key, 0) >= sim_threshold:
                if successor not in node_depths:
                    node_depths[successor] = current_depth + 1
                    queue.append(successor)

    # Return nodes at max depth and max depth - 1
    if not node_depths:
        return []

    max_depth = max(node_depths.values())
    return [node for node, depth in node_depths.items() if depth >= max_depth - 1]


def calling_node_pagerank(
    G: nx.DiGraph, edge_weight_key: str = "weight"
) -> List[Tuple[str, float]]:
    """Calculate PageRank for calling nodes."""
    pr = pagerank(G, weight=edge_weight_key)
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)


class Ranker:
    """Main ranking component for MicroDig algorithm."""

    def __init__(
        self, hyper_params: Dict[str, Any], case: CaseModel, graph_gen: GraphGenerator
    ):
        """
        Initialize ranker.

        Args:
            hyper_params: Algorithm hyperparameters
            case: Case model with failure data
            graph_gen: Graph generator component
        """
        self.hyper_params = hyper_params
        self.case = case
        self.graph_gen = graph_gen
        self.candidate_root_causes: Optional[List[str]] = None

        logger.debug(f"Ranker initialized for case {case.alarm_start_time}")

    def get_candidate_root_causes(self) -> List[str]:
        """Get candidate root cause nodes."""
        if self.candidate_root_causes is not None:
            return self.candidate_root_causes

        start_server = self.case.alarm_item
        level = self.hyper_params["level"]

        # Get anomaly graph based on level
        if level == "method":
            G = self.graph_gen.get_asso_method_node_ano_graph()
        elif level == "service":
            G, _ = self.graph_gen.get_asso_service_node_ano_graph()
        else:
            raise ValueError(f"Unsupported level: {level}")

        # Search for candidates based on strategy
        search_method = self.hyper_params["search_method"]
        sim_threshold = -1  # Use all nodes by default

        if search_method == "all":
            candidates = list(G.nodes)
        elif search_method == "deepest2":
            candidates = deepest2_anomaly_hop_search(G, start_server, sim_threshold)
        elif search_method == "last2":
            candidates = last2_anomaly_hop_search(G, start_server, sim_threshold)
        else:
            raise ValueError(f"Unknown search method: {search_method}")

        self.candidate_root_causes = candidates
        logger.info(f"Found {len(candidates)} candidate root causes")
        return candidates

    def server_node_rank(self) -> pd.DataFrame:
        """Rank server nodes (Algorithm 5)."""
        G_server = self.graph_gen.get_server_node_graph()
        if len(G_server) == 0:
            logger.warning("Empty server graph")
            return pd.DataFrame()

        rankings = self._rank_server_node_graph(G_server)
        return pd.DataFrame(rankings, columns=["name", "final_score"])

    def mix_node_rank_without_detection(self) -> pd.DataFrame:
        """Mixed node ranking without method-level detection (Algorithm 4)."""
        G_mix = self.graph_gen.get_mix_server_node_graph_without_method_detection()
        if len(G_mix) == 0:
            logger.warning("Empty mixed graph")
            return pd.DataFrame()

        rankings = self._rank_mix_graph(G_mix)
        return pd.DataFrame(rankings, columns=["name", "final_score"])

    def mix_node_rank(self) -> pd.DataFrame:
        """Mixed node ranking with detection."""
        G_mix = self.graph_gen.get_mix_server_node_graph()
        if len(G_mix) == 0:
            logger.warning("Empty mixed graph")
            return pd.DataFrame()

        rankings = self._rank_mix_graph(G_mix)
        return pd.DataFrame(rankings, columns=["name", "final_score"])

    def algorithm1(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Algorithm 1: Basic method and server ranking.

        Returns:
            Tuple of (server_rankings, method_rankings)
        """
        logger.info("Running Algorithm 1")

        # Get method-level graph and rank
        candidates = self.get_candidate_root_causes()
        if not candidates:
            logger.warning("No candidate root causes found")
            return pd.DataFrame(), pd.DataFrame()

        # Method rankings
        method_rankings = []
        for candidate in candidates:
            # Calculate method score (simplified)
            score = self._calculate_method_score(candidate)
            method_rankings.append(
                {
                    "name": candidate,
                    "final_score": score,
                    "server": candidate.split("|")[0]
                    if "|" in candidate
                    else candidate,
                }
            )

        method_df = pd.DataFrame(method_rankings)
        if method_df.empty:
            return pd.DataFrame(), method_df

        # Server rankings (aggregate from method rankings)
        server_scores = method_df.groupby("server")["final_score"].sum().reset_index()
        server_scores.columns = ["name", "final_score"]
        server_scores = server_scores.sort_values("final_score", ascending=False)

        method_df = method_df.sort_values("final_score", ascending=False)

        logger.info(
            f"Algorithm 1 completed: {len(server_scores)} servers, {len(method_df)} methods"
        )
        return server_scores, method_df

    def _calculate_method_score(self, method_node: str) -> float:
        """Calculate score for a method node."""
        # This is a simplified scoring function
        # In the original implementation, this would involve more complex calculations
        try:
            G = self.graph_gen.get_asso_method_node_ano_graph()
            if method_node in G.nodes:
                # Use anomaly scores from incoming edges
                incoming_scores = [
                    data.get("score", 0)
                    for _, _, data in G.in_edges(method_node, data=True)
                ]
                return max(incoming_scores) if incoming_scores else 0.1
            return 0.0
        except Exception as e:
            logger.warning(f"Error calculating method score for {method_node}: {e}")
            return 0.0

    def _rank_server_node_graph(
        self, G: nx.DiGraph, edge_weight_key: str = "weight"
    ) -> List[Tuple[str, float]]:
        """Rank nodes in server graph."""
        # Convert to numpy array for manipulation
        try:
            arr = nx.to_numpy_array(G, weight=edge_weight_key)
            node_list = list(G.nodes)
        except Exception as e:
            logger.error(f"Error converting graph to array: {e}")
            return [(node, 0.0) for node in G.nodes]

        if len(node_list) == 0:
            logger.warning("Empty node list")
            return []

        # Add reverse edges with reduced weight
        rev_weight = self.hyper_params["rev_weight"]
        rev_mat = arr.T * (arr == 0) * rev_weight

        # Add self-loops for nodes with more incoming than outgoing edges
        try:
            in_weights = np.amax(arr, axis=0, keepdims=True)
            out_weights = np.amax(arr, axis=1, keepdims=True)

            # Ensure compatible shapes
            diff = np.maximum(0, in_weights.T - out_weights)
            # Create diagonal matrix only for the diagonal elements
            diag_values = (
                np.diag(diff)
                if diff.shape[0] == diff.shape[1]
                else np.zeros(len(node_list))
            )
            self_mat = np.diag(diag_values)
        except Exception as e:
            logger.warning(f"Error creating self-loop matrix: {e}")
            self_mat = np.zeros_like(arr)

        # Combine matrices
        arr += rev_mat + self_mat

        # Normalize rows
        row_sums = arr.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        arr = arr / row_sums

        # Create new graph and rank
        G_arr = nx.from_numpy_array(arr, create_using=nx.DiGraph)
        G_arr = nx.relabel_nodes(G_arr, dict(enumerate(node_list)))

        rankings = self._do_rank(G_arr, edge_weight_key)
        return sorted(rankings.items(), key=lambda x: x[1], reverse=True)

    def _rank_mix_graph(
        self, G_mix: nx.DiGraph, edge_weight_key: str = "weight"
    ) -> List[Tuple[str, float]]:
        """Rank nodes in mixed graph."""
        rank_method = self.hyper_params["rank_method"]

        if rank_method == "pagerank":
            # Add annotation for non-mix edges
            for fro, to, data in G_mix.edges.data():
                if data.get("type") != "mix":
                    G_mix[fro][to]["anno"] = 1

            rankings = pagerank(G_mix, weight="anno")

        elif rank_method == "random walk":
            # Find starting nodes (item nodes connected to alarm)
            start_nodes = {}
            alarm_item = self.case.alarm_item

            for node in G_mix.nodes:
                if G_mix.nodes[node].get("type") == "item" and alarm_item in node:
                    start_nodes[node] = 1.0

            if not start_nodes:
                # Fallback to any item nodes
                for node in G_mix.nodes:
                    if G_mix.nodes[node].get("type") == "item":
                        start_nodes[node] = 1.0
                        break

            rankings = random_walk(G_mix, start_nodes, weight=edge_weight_key)

        else:
            raise ValueError(f"Unknown rank method: {rank_method}")

        return sorted(rankings.items(), key=lambda x: x[1], reverse=True)

    def _do_rank(self, G: nx.DiGraph, edge_weight_key: str) -> Dict[str, float]:
        """Perform ranking on graph."""
        rank_method = self.hyper_params["rank_method"]

        if rank_method == "pagerank":
            return pagerank(G, weight=edge_weight_key)

        elif rank_method == "random walk":
            # Use alarm item as starting point
            start_nodes = {
                node: 1.0 for node in G.nodes if self.case.alarm_item in node
            }

            if not start_nodes:
                # Fallback to uniform start
                start_nodes = {list(G.nodes)[0]: 1.0} if G.nodes else {}

            return random_walk(G, start_nodes, weight=edge_weight_key)

        else:
            raise ValueError(f"Unknown rank method: {rank_method}")

    def run_all_algorithms(self) -> Dict[str, pd.DataFrame]:
        """
        Run all ranking algorithms.

        Returns:
            Dictionary with results from different algorithms
        """
        logger.info("Running all ranking algorithms")

        results = {}

        try:
            # Algorithm 1
            server_rank, method_rank = self.algorithm1()
            results["alg1_server"] = server_rank
            results["alg1_method"] = method_rank

            # Algorithm 4 (mixed without method detection)
            results["alg4"] = self.mix_node_rank_without_detection()

            # Algorithm 5 (server ranking)
            results["alg5"] = self.server_node_rank()

            logger.info("All algorithms completed successfully")

        except Exception as e:
            logger.error(f"Error running algorithms: {e}")
            # Return empty DataFrames for failed algorithms
            for key in ["alg1_server", "alg1_method", "alg4", "alg5"]:
                if key not in results:
                    results[key] = pd.DataFrame()

        return results
