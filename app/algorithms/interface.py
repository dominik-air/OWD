from typing import Callable
from .point import Point
from .ideal_point import ideal_point_method
from .filtered import naive_with_filtering
from .naive_without_filtration import naive_without_filtering

OWDAlgorithm = Callable[[list[Point]], list[Point]]

ALGORITHMS: dict[str, OWDAlgorithm] = {
    "ideal point method": ideal_point_method,
    "filtered naive": naive_with_filtering,
    "naive without filtration": naive_without_filtering
}
