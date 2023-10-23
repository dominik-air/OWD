from typing import Callable
from .point import Point
from .ideal_point import ideal_point_method
from .filtered import naive_with_filtering
from .naive_without_filtration import naive_without_filtering
from numpy.random import exponential, normal, poisson, uniform
import time
from numpy import mean, std

OWDAlgorithm = Callable[[list[Point]], list[Point]]
distribution_callable = Callable[[int, int], list[Point]]

ALGORITHMS: dict[str, OWDAlgorithm] = {
    "ideal point method": ideal_point_method,
    "filtered naive": naive_with_filtering,
    "naive without filtration": naive_without_filtering
}

DISTRIBUTIONS: dict[str, Callable[[int, int], list[Point]]] = {
    "uniform": lambda d, n : [Point(uniform(0, 2, d)) for _ in range(n)],
    "normal": lambda d, n : [Point(normal(0, 1, d)) for _ in range(n)],
    "exponential": lambda d, n : [Point(exponential(1, d)) for _ in range(n)],
    "poisson": lambda d, n : [Point(poisson(1, d)) for _ in range(n)],
}

class BenchmarkAnalyzer:
    def __init__(
            self,
            distribution: str,
            algorithm: str,
            dimensionality: int,
            cardinality: int,
        ):
        self.distribution = distribution
        self.algorithm = algorithm
        self.dimensionality: int = dimensionality
        self.cardinality: int = cardinality
        self.dataset: list[Point] = self._generate_dataset()
        self.times: list[float] = []
        self.comparison_point_counter: list[int] = []
        self.comparison_coordinates_counter: list[int] = []
        self.recent_result: [dict[str, any] | None] = None

    def _generate_dataset(self) -> list[list[Point]]:
        return DISTRIBUTIONS[self.distribution](self.dimensionality, self.cardinality)

    def run_algorithm(self, repeats: int) -> dict[str, any]:
        self.times = []
        self.comparison_counter = []
        
        for _ in range(repeats):
            Point.reset_counter()

            start = time.perf_counter()

            ALGORITHMS[self.algorithm](self.dataset)

            self.times.append(time.perf_counter() - start)
            self.comparison_point_counter.append(Point.get_global_point_counter())
            self.comparison_coordinates_counter.append(Point.get_global_coordinate_counter())
        
        return {
            "algorithm": self.algorithm,
            "distribution": self.distribution,
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
            "distribution": result["distribution"],
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


        
    