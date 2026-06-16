from pathlib import Path

import polars as pl

from src.microdig.alarm_detector import AlarmDetector
from src.microdig.algorithm import MicroDigAlgorithm
from src.microdig.anomaly import AnomalyDetector
from src.microdig.data_structures import AlgorithmInput, CaseModel
from src.microdig.graph import GraphGenerator, get_connected_graph, merge_callings_by_level


def test_alarm_detector_extracts_hipster_shop_services(tmp_path: Path) -> None:
    detector = AlarmDetector(tmp_path)

    assert (
        detector._extract_service_from_span(
            "/hipstershop.EmailService/SendOrderConfirmation"
        )
        == "emailservice"
    )
    assert (
        detector._extract_service_from_span("POST /hipstershop.CartService/AddItem")
        == "cartservice"
    )
    assert (
        detector._extract_service_from_span("hipstershop.Frontend/Recv.")
        == "frontend"
    )
    assert detector._extract_service_from_span("HGET") is None


def test_alarm_detector_uses_conclusion_fallback_when_issues_are_empty(
    tmp_path: Path,
) -> None:
    pl.DataFrame(
        {
            "SpanName": [
                "hipstershop.CartService/AddItem",
                "hipstershop.Frontend/Recv.",
            ],
            "Issues": ["{}", "{}"],
            "AbnormalAvgDuration": [0.1, 0.1],
            "NormalAvgDuration": [0.1, 0.1],
            "AbnormalSuccRate": [0.2, 0.9],
            "NormalSuccRate": [1.0, 1.0],
        }
    ).write_parquet(tmp_path / "conclusion.parquet")

    assert AlarmDetector(tmp_path).detect_alarm_service() == "cartservice"


def test_unknown_alarm_item_does_not_empty_service_graph() -> None:
    callings = {
        "frontend|GET|cartservice|AddItem": {
            "name": "frontend|GET|cartservice|AddItem",
            "duration": {1: 1.0, 2: 2.0},
            "error_min": {1: 0, 2: 1},
            "error_rate": {1: 0.0, 2: 1.0},
            "request_min": {1: 1, 2: 1},
        }
    }
    case = CaseModel(
        alarm_start_time="2025-06-16 00:02:00",
        alarm_end_time="2025-06-16 00:07:00",
        alarm_start_minute=2,
        alarm_end_minute=7,
        monitor_id=1,
        alarm_item="unknown-service",
        sli_type="error_rate",
        where_info={"service": "unknown-service"},
        callings=callings,
    )
    hyper_params = AlgorithmInput(case=case).to_dict()

    graph = GraphGenerator(AnomalyDetector(hyper_params), hyper_params, case)
    service_callings = merge_callings_by_level(callings, "method", "service")
    service_graph = graph._build_asso_node_graph(service_callings)

    assert sorted(service_graph.nodes) == ["cartservice", "frontend"]
    assert sorted(service_graph.edges) == [("frontend", "cartservice")]


def test_empty_anomaly_graph_falls_back_to_base_service_graph() -> None:
    callings = {
        "frontend|cartservice": {
            "name": "frontend|cartservice",
            "duration": {1: 1.0, 2: 1.0},
            "error_min": {1: 0, 2: 0},
            "error_rate": {1: 0.0, 2: 0.0},
            "request_min": {1: 1, 2: 1},
        }
    }
    case = CaseModel(
        alarm_start_time="2025-06-16 00:02:00",
        alarm_end_time="2025-06-16 00:07:00",
        alarm_start_minute=2,
        alarm_end_minute=7,
        monitor_id=1,
        alarm_item="cartservice",
        sli_type="error_rate",
        where_info={"service": "cartservice"},
        callings=callings,
    )
    hyper_params = AlgorithmInput(case=case).to_dict()

    graph = GraphGenerator(AnomalyDetector(hyper_params), hyper_params, case)
    base_graph = graph._build_asso_node_graph(callings)
    anomaly_graph = graph._build_node_ano_graph(base_graph)

    assert sorted(anomaly_graph.nodes) == ["cartservice", "frontend"]
    assert sorted(anomaly_graph.edges) == [("frontend", "cartservice")]


def test_connected_graph_without_start_nodes_is_empty() -> None:
    import networkx as nx

    graph = nx.DiGraph()
    graph.add_edge("frontend", "cartservice")

    assert len(get_connected_graph(graph, [])) == 0


def test_result_extraction_accepts_non_train_ticket_services() -> None:
    algorithm = MicroDigAlgorithm()

    assert algorithm._extract_service_name("cartservice", "alg5") == "cartservice"
    assert algorithm._extract_service_name("redis", "alg5") == "redis-cart"
    assert (
        algorithm._extract_service_name("hipstershop.Frontend/Recv.", "alg5")
        == "frontend"
    )
    assert algorithm._extract_service_name("HGET", "alg5") is None
