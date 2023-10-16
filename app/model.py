from .algorithms.point import Point
from .algorithms.interface import OWDAlgorithm


class DataPointModel:
    def __init__(self) -> None:
        self._data: list[Point] = []
        self._dominated: list[Point] = []
        self._non_dominated: list[Point] = []

    @property
    def data(self) -> list[Point]:
        return self._data

    @data.setter
    def data(self, value: list[Point]) -> None:
        self._data = value

    @property
    def dominated(self) -> list[Point]:
        return self._dominated

    @property
    def non_dominated(self) -> list[Point]:
        return self._non_dominated

    def process_data_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
        non_dominated = algorithm(self.data)
        self._non_dominated = non_dominated
        self._dominated = self._filter_non_dominated(non_dominated)

    def _filter_non_dominated(self, non_dominated: list[Point]) -> list[Point]:
        dominated = []
        for p in self.data:
            if p not in non_dominated:
                dominated.append(p)
        return dominated
