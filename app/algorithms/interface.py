from typing import Callable
from .point import Point
from .ideal_point import ideal_point_method
from .filtered import naive_with_filtering
from .naive_without_filtration import naive_without_filtering
from .vikor import vikor
from .topsis import topsis
import time
from numpy import mean, std

OWDAlgorithm = Callable[[list[Point]], list[Point]]
Ranking = tuple[list[int], list[float]]
RankingMethod = Callable[[list[Point], list[float]], Ranking]
distribution_callable = Callable[[int, int], list[Point]]

NAIVE_ALGORITHMS: dict[str, OWDAlgorithm] = {
    "ideal point method": ideal_point_method,
    "filtered naive": naive_with_filtering,
    "naive without filtration": naive_without_filtering
}


RANKING_ALGORITHMS: dict[str, RankingMethod] = {
    "TOPSIS": topsis,
    "RSM": lambda: exec('raise NotImplementedError'),
    "UTA Star": lambda: exec('raise NotImplementedError'),
    "VIKOR": vikor
}


class BenchmarkAnalyzer:
    def __init__(
            self,
            algorithm: str,
            dimensionality: int,
            dataset: list[Point]
    ):

        self.algorithm = algorithm
        self.dimensionality: int = dimensionality
        self.dataset: list[Point] = dataset
        self.cardinality: int = len(self.dataset)
        self.times: list[float] = []
        self.comparison_point_counter: list[int] = []
        self.comparison_coordinates_counter: list[int] = []
        self.recent_result: [dict[str, any] | None] = None

    def run_algorithm(self, repeats: int) -> dict[str, any]:
        self.times = []
        self.comparison_counter = []

        for _ in range(repeats):
            Point.reset_counter()

            start = time.perf_counter()

            NAIVE_ALGORITHMS[self.algorithm](self.dataset)

            self.times.append(time.perf_counter() - start)
            self.comparison_point_counter.append(Point.get_global_point_counter())
            self.comparison_coordinates_counter.append(Point.get_global_coordinate_counter())

        return {
            "algorithm": self.algorithm,
            "dimensionality": self.dimensionality,
            "cardinality": self.cardinality,
            "times": self.times,
            "comparison_point_counter": self.comparison_point_counter,
            "comparison_coordinates_counter": self.comparison_coordinates_counter
        }

    def parse_result(self, result: [dict[str, any] | None] = None) -> dict[str, any]:
        if result is None:
            result = self.recent_result
        return {
            "algorithm": result["algorithm"],
            "dimensionality": result["dimensionality"],
            "cardinality": result["cardinality"],
            "mean_time": {"mean": mean(result["times"]), "std": std(result["times"])},
            "comparison_point_counter": {
                "mean": mean(result["comparison_point_counter"]),
                "std": std(result["comparison_point_counter"])
            },
            "comparison_coordinates_counter": {
                "mean": mean(result["comparison_coordinates_counter"]),
                "std": std(result["comparison_coordinates_counter"])
            }
        }
