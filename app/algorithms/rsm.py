from typing import List
from .types import Ranking, Point
import numpy as np

def normalize(data: np.array) -> np.array:
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    return (data - min_vals) / (max_vals - min_vals)

def calculate_sum_of_distances(alternative: np.array, point_set: np.array) -> float:
    return np.sum(np.linalg.norm(point_set - alternative, axis=1))

def reference_set_method(alternatives: List[Point], weights: np.array, ideal_points_set: np.array, status_quo_points_set: np.array) -> Ranking:
    alternatives = [p.to_numpy() for p in alternatives]
    normalized_alternatives = normalize(np.array(alternatives))

    weighted_alternatives = normalized_alternatives * weights

    scores = []
    for alternative in weighted_alternatives:
        dist_ideal = calculate_sum_of_distances(alternative, ideal_points_set)
        dist_antiideal = calculate_sum_of_distances(alternative, status_quo_points_set)
        score = dist_ideal / (dist_ideal + dist_antiideal)
        scores.append(score)
    scores = np.array(scores)

    sorted_indices = np.argsort(-scores)
    sorted_scores = scores[sorted_indices]

    return sorted_indices.tolist(), sorted_scores.tolist()
