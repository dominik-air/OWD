from typing import Any, List
from numpy import ones, ndarray
from .point import Point


def naive_without_filtering(
    data: List[Point],
) -> List[Point]:
    n: int = len(data)
    active: ndarray = ones(n, dtype=bool)
    non_dominated_results: List[Any] = []
    for i, y in enumerate(data):
        if not active[i] and y not in non_dominated_results:
            continue
        candidate = y
        for j, x in enumerate(data[i + 1 :], i + 1):
            if not active[j]:
                continue
            if candidate <= x:
                active[j] = False
            elif x <= candidate:
                active[i] = False
                candidate = x
        non_dominated_results.append(candidate)
    return non_dominated_results
