import numpy as np
import streamlit as st
from ..algorithms.point import Point, create_points_from_datapoints
from ..algorithms.types import OWDAlgorithm, RankingMethod, Ranking


class PropertyNotReadyError(Exception):
    def __init__(self, property_name: str, method_name: str, *args):
        super().__init__(*args)
        self.message = f"Property '{property_name}' is not ready for access. Please make sure to run '{method_name}' method before accesing this property."

    def __str__(self):
        return self.message


class Model:

    def __init__(self, streamlit_indentifier: str) -> None:
        if streamlit_indentifier in st.session_state:
            raise ValueError(f"{streamlit_indentifier} streamlit_indentifier is already used!")
        self.streamlit_indentifier = streamlit_indentifier
        self._data: np.ndarray = np.random.normal(0, 1, size=(20, 2))
        self._labels: list[str] = ["x", "y"]
        self._directions: list[str] = ["Min", "Max"]
        self._dominated_points: list[Point] = None
        self._non_dominated_points: list[Point] = None

        # fields used by ranking methods
        self._alternative_names: list[str] = [f"alt{i}" for i in range(20)]
        self._class_names: list[str] = ["A1", "A2", "A1"]
        self._class_data: np.ndarray = np.random.normal(0, 1, size=(3, 2))
        self._criteria_weights: list[float] = [0.5, 0.5]
        self._ranking: Ranking = None

        if self.streamlit_indentifier not in st.session_state:
            st.session_state[self.streamlit_indentifier] = self

    @property
    def points(self) -> list[Point]:
        return create_points_from_datapoints(self._data)

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, data: np.ndarray) -> None:
        self._data = data
        self.checkpoint()

    @property
    def labels(self) -> list[str]:
        return self._labels

    @labels.setter
    def labels(self, labels: list[str]) -> None:
        self._labels = labels
        self.checkpoint()

    @property
    def criteria_weights(self) -> list[float]:
        return self._criteria_weights

    @criteria_weights.setter
    def criteria_weights(self, criteria_weights: list[float]) -> None:
        if sum(criteria_weights) > 1.0:
            raise ValueError("The criteria weights vector has to be normalized!")
        self._criteria_weights = criteria_weights
        self.checkpoint()

    @property
    def directions(self) -> list[str]:
        return self._directions

    @directions.setter
    def directions(self, directions: list[str]) -> None:
        self._directions = directions
        self.checkpoint()

    @property
    def dominated_points(self) -> list[Point]:
        if self._dominated_points is None:
            raise PropertyNotReadyError(
                "dominated_points", "process_points_with_naive_algorithm"
            )
        return self._dominated_points

    @property
    def non_dominated_points(self) -> list[Point]:
        if self._dominated_points is None:
            raise PropertyNotReadyError(
                "non_dominated_points", "process_points_with_naive_algorithm"
            )
        return self._non_dominated_points

    @property
    def class_names(self) -> list[str]:
        return self._class_names

    @class_names.setter
    def class_names(self, class_names: list[str]) -> None:
        self._class_names = class_names
        self.checkpoint()

    @property
    def class_data(self) -> np.ndarray:
        return self._class_data

    @class_data.setter
    def class_data(self, class_data: np.ndarray) -> None:
        self._class_data = class_data
        self.checkpoint()

    @property
    def alternative_names(self) -> list[str]:
        return self._alternative_names

    @alternative_names.setter
    def alternative_names(self, alternative_names: list[str]) -> None:
        self._alternative_names = alternative_names
        self.checkpoint()

    @property
    def ranking(self) -> Ranking:
        if self._ranking is None:
            raise PropertyNotReadyError("ranking", "process_points_with_ranking_method")
        return self._ranking

    def process_points_with_naive_algorithm(self, algorithm: OWDAlgorithm) -> None:
        points = self.points
        # flip the signs for optimisation
        for p in points:
            p.adjust_signs_for_optimization(self.directions)
        non_dominated = algorithm(points)
        # bring back the previous values
        for p in non_dominated:
            p.adjust_signs_for_optimization(self.directions)
        self._non_dominated_points = non_dominated
        self._dominated_points = self._filter_non_dominated(non_dominated)
        self.checkpoint()

    def process_points_with_ranking_method(self, algorithm: RankingMethod) -> None:
        # flip the signs for optimisation
        for p in self.non_dominated_points:
            p.adjust_signs_for_optimization(self.directions)
        ranking = algorithm(self.non_dominated_points, self.criteria_weights)
        self._ranking = ranking
        self.checkpoint()

    def _filter_non_dominated(self, non_dominated: list[Point]) -> list[Point]:
        dominated = []
        for p in self.points:
            if p not in non_dominated:
                dominated.append(p)
        return dominated

    def checkpoint(self) -> None:
        """Save the current state of the data model, since Streamlit is stateless by design."""
        st.session_state[self.streamlit_indentifier] = self


def get_model(streamlit_indentifier: str) -> Model:
    if streamlit_indentifier not in st.session_state:
        return Model(streamlit_indentifier)
    return st.session_state[streamlit_indentifier]
