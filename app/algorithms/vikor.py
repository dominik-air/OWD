from enum import Enum, auto
import numpy as np
from .point import Point
from .types import Ranking


class CompromiseStrategy(Enum):
    # pursue best solutions
    MaximumGroupUtility = auto()
    # balance between best and worst solutions
    ByConsensus = auto()
    # avoid worst case scenario
    ByVeto = auto()


def get_strategy_thresholds(strategy: CompromiseStrategy) -> float:
    """Returns a threshold for a given strategy."""
    if strategy == CompromiseStrategy.ByConsensus:
        # this values needs to be around 0.5
        return 0.5
    elif strategy == CompromiseStrategy.MaximumGroupUtility:
        # this value needs to be over 0.5
        return 0.75
    elif strategy == CompromiseStrategy.ByVeto:
        # this value needs to be below 0.5
        return 0.25
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def vikor(
    points: list[Point],
    weights: list[float],
    strategy: CompromiseStrategy = CompromiseStrategy.ByConsensus,
) -> Ranking:
    """Reference: https://en.wikipedia.org/wiki/VIKOR_method"""
    data = np.array([p.to_numpy() for p in points])

    min_values = data.min(axis=0)
    max_values = data.max(axis=0)
    norm_data = (data - min_values) / (max_values - min_values)

    weighted_data = norm_data * weights
    S = weighted_data.sum(axis=1)
    R = weighted_data.max(axis=1)
    
    S = (S - S.min()) / (S.max() - S.min() + 1e-6)
    R = (R - R.min()) / (R.max() - R.min() + 1e-6)

    v = get_strategy_thresholds(strategy)
    Q = v * S + (1 - v) * R

    sorted_indices = np.argsort(-Q)
    sorted_q_values = Q[sorted_indices]

    return sorted_indices.tolist(), sorted_q_values.tolist()
