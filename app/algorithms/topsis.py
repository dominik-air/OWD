import numpy as np
from .point import Point
from .interface import Ranking


def topsis(points: list[Point], weights: list[float]) -> Ranking:
    """Reference: https://en.wikipedia.org/wiki/TOPSIS"""
    data_matrix = np.array([p.to_numpy() for p in points])

    norm_matrix = data_matrix / np.sqrt((data_matrix ** 2).sum(axis=0))

    weighted_matrix = norm_matrix * weights

    ideal_solution = np.max(weighted_matrix, axis=0)
    negative_ideal_solution = np.min(weighted_matrix, axis=0)

    separation_from_ideal = np.sqrt(((weighted_matrix - ideal_solution) ** 2).sum(axis=1))
    separation_from_negative_ideal = np.sqrt(((weighted_matrix - negative_ideal_solution) ** 2).sum(axis=1))

    relative_closeness = separation_from_negative_ideal / (separation_from_ideal + separation_from_negative_ideal)

    sorted_indices = np.argsort(-relative_closeness)
    sorted_scores = relative_closeness[sorted_indices]

    return sorted_indices.tolist(), sorted_scores.tolist()
