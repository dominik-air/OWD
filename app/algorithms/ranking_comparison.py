from typing import List, Dict, Callable
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


COMPARISON_FN = Callable[[np.ndarray, np.ndarray], float]


def absolute_difference(rank1: np.ndarray, rank2: np.ndarray) -> float:
    """Sum of absolute differences between rankings."""
    return np.sum(np.abs(rank1 - rank2))

def weighted_absolute_difference(rank1: np.ndarray, rank2: np.ndarray) -> float:
    """Weighted sum of absolute differences between rankings."""
    diff = np.abs(rank1 - rank2)
    weights = np.maximum(len(rank2) - rank1, len(rank2) - rank2)
    return np.sum(weights * diff)

def spearman_correlation(rank1: np.ndarray, rank2: np.ndarray) -> float:
    """Spearman rank correlation coefficient."""
    distance, _ = scipy.stats.spearmanr(rank1, rank2)
    return round(distance, 3)

def kendall_tau(rank1: np.ndarray, rank2: np.ndarray) -> float:
    """Kendall's tau coefficient."""
    distance, _ = scipy.stats.kendalltau(rank1, rank2)
    return round(distance, 3)

COMPARISON_FUNCTIONS: Dict[str, COMPARISON_FN] = {
        "absolute difference": absolute_difference,
        "weighted absolute difference": weighted_absolute_difference,
        "spearman correlation": spearman_correlation,
        "kendall tau": kendall_tau
    }


def compare(rank1: np.ndarray, rank2: np.ndarray, comparison_type: str) -> float:
    if len(rank1) != len(rank2):
        raise ValueError("Rankings are not the same size.")
    
    if comparison_type not in COMPARISON_FUNCTIONS:
        raise ValueError("Wrong comparison type")

    return COMPARISON_FUNCTIONS[comparison_type](rank1, rank2)

def build_comparison_graph(matrix: np.ndarray) -> nx.Graph:
    G = nx.Graph()
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            G.add_edge(i + 1, j + 1, weight=matrix[i, j])
    return G


def draw_comparison_graph(rankings: np.ndarray, comparison_type: str, methods: List[str]) -> None:
    n_methods = len(rankings)
    D = np.zeros((n_methods, n_methods))

    for i in range(n_methods):
        for j in range(n_methods):
            if i != j:
                D[i, j] = compare(rankings[i], rankings[j], comparison_type)

    G = build_comparison_graph(D)
    labeldict = {i + 1: method for i, method in enumerate(methods)}
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, width=2, node_size=1000, labels=labeldict, font_color="red")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title(f"{comparison_type.title()} Ranking Comparison")
    plt.show()

