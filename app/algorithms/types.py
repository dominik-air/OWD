from typing import Callable
from .point import Point

OWDAlgorithm = Callable[[list[Point]], list[Point]]
Ranking = tuple[list[int], list[float]]
RankingMethod = Callable[[list[Point], list[float]], Ranking]
distribution_callable = Callable[[int, int], list[Point]]
