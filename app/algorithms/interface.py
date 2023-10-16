from typing import Callable
from .point import Point
from .ideal_point import ideal_point_method

OWDAlgorithm = Callable[[list[Point]], list[Point]]

ALGORITHMS: dict[str, OWDAlgorithm] = {
    "ideal point method": ideal_point_method,
    "alg2": ideal_point_method,
    "alg3": ideal_point_method,
}
