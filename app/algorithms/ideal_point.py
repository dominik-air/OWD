from typing import Iterable
import numpy as np
from .point import Point


def distance_between_points(p1: Point, p2: Point):
    return np.sum(np.square(p1.x - p2.x))


def ideal_point_method(points: Iterable[Point]) -> list[Point]:
    min_values_per_dimension = []
    for dim_index in range(points[0].dim):
        min_value = min(points, key=lambda p: p.x[dim_index]).x[dim_index]
        min_values_per_dimension.append(min_value)

    ideal_point = Point(np.array(min_values_per_dimension))

    distances_and_indices = [
        (distance_between_points(ideal_point, p), idx) for idx, p in enumerate(points)
    ]
    distances_and_indices.sort(key=lambda item: item[0])
    sorted_indices = [idx for _, idx in distances_and_indices]

    current_index = 0
    total_points = len(points)
    non_dominated_points = []
    is_point_active = [True] * total_points

    while current_index <= total_points:
        if not is_point_active[sorted_indices[current_index]]:
            current_index += 1
            continue

        for idx, point in enumerate(points):
            if points[sorted_indices[current_index]] <= point:
                is_point_active[idx] = False
        is_point_active[sorted_indices[current_index]] = False
        non_dominated_points.append(points[sorted_indices[current_index]])

        total_points -= 1
        current_index += 1

    return non_dominated_points
