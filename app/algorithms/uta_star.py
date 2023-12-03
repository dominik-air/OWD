from .point import Point
from .types import Ranking
from typing import List
import numpy as np


def divide_into_parts(points: List[Point], num_of_parts: List[int]) -> List[List[List[float]]]:
    parts = []
    for i in range(len(points[0].x)):
        values = [point.x[i] for point in points]
        elem = np.percentile(values, np.linspace(0, 100, num_of_parts[i]))
        parts.append(elem.tolist())
    return parts


def create_usability_function_values(weights: List[float], size: int, parts: List[List[List[float]]]) -> List[dict]:
    function_values = []
    for i in range(size):
        num_of_parts = len(parts[i])
        value = {parts[i][j]: weights[i] * j for j in range(num_of_parts)}
        function_values.append(value)
    return function_values


def create_functions(function_values: List[dict]) -> List[dict]:
    function_values_in_intervals = []
    for i in range(len(function_values)):
        key_list = list(function_values[i].keys())
        value_list = list(function_values[i].values())
        values_for_interval = {}
        for j in range(len(function_values[i]) - 1):
            a = (value_list[j] - value_list[j + 1]) / (key_list[j] - key_list[j + 1])
            b = value_list[j] - a * key_list[j]
            values_for_interval[(key_list[j], key_list[j + 1])] = (a, b)
        function_values_in_intervals.append(values_for_interval)
    return function_values_in_intervals


def create_solution_table(points: List[Point], size: int, function_values_in_intervals: List[dict]) -> List[float]:
    uta_star_values = []
    for point in points:
        u_values = []
        for i in range(size):
            for key, value in function_values_in_intervals[i].items():
                if key[0] <= point.x[i] <= key[1]:
                    u_values.append(value[0] * point.x[i] + value[1])
                    break
        uta_star_values.append(sum(u_values))
    return uta_star_values


def return_solution(uta_star_values: List[float]) -> Ranking:
    ranking = sorted(range(len(uta_star_values)), key=lambda k: uta_star_values[k], reverse=True)
    points_values = [uta_star_values[i] for i in ranking]
    return ranking, points_values


def uta_star(points: List[Point], weights: List[float]) -> Ranking:
    size = len(points[0].x)
    num_of_parts = [2] * size
    parts = divide_into_parts(points, num_of_parts)

    function_values = create_usability_function_values(weights, size, parts)
    function_values_in_intervals = create_functions(function_values)

    uta_star_values = create_solution_table(points, size, function_values_in_intervals)
    ranking, points_values = return_solution(uta_star_values)
    return ranking, points_values
