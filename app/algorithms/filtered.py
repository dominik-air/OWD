from typing import Any, List
from numpy import ones, ndarray, argmax
from .point import Point


def naive_with_filtering(
    data: List[Point],
) -> List[Point]:
    """Naive implementation of the naive algorithm for non-dominated elements in set."""
    n: int = len(data)
    active: ndarray = ones(n, dtype=bool)
    non_dominated_results: List[Any] = []
    for i, y in enumerate(data):
        if not active[i]: continue
        candidate = y
        candidate_index = i
        for j, x in enumerate(data[i + 1 :], i + 1):
            if not active[j]: continue
            if candidate <= x:
                active[j] = False
            elif x <= candidate:
                active[i] = False
                active[candidate_index] = False
                candidate_index = j
                candidate = x
        non_dominated_results.append(candidate)
        for i, x in enumerate(data):
            if active[i] and candidate <= x:
                active[i] = False
        if sum(active) == 1:
            non_dominated_results.append(data[argmax(active)])
            break
    return non_dominated_results
