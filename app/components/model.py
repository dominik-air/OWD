import numpy as np
import streamlit as st
from ..algorithms.point import Point, create_points_from_datapoints
from ..algorithms.interface import OWDAlgorithm


class Model:
    streamlit_indentifier = "data_model"

    def __init__(self) -> None:
        self._data: np.ndarray = np.random.normal(0, 1, size=(20, 2))
        self._labels: list[str] = ["x", "y"]
        self._directions: list[str] = ["Min", "Max"]
        self._dominated_points: list[Point] = []
        self._non_dominated_points: list[Point] = []

        # fields used by ranking methods
        self._alternative_names: list[str] = []
        self._class_names: list[str] = []
        self._class_data: np.ndarray = np.array([])

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
    def directions(self) -> list[str]:
        return self._directions

    @directions.setter
    def directions(self, directions: list[str]) -> None:
        self._directions = directions
        self.checkpoint()

    @property
    def dominated_points(self) -> list[Point]:
        return self._dominated_points

    @property
    def non_dominated_points(self) -> list[Point]:
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

    def process_points_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
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

    def _filter_non_dominated(self, non_dominated: list[Point]) -> list[Point]:
        dominated = []
        for p in self.points:
            if p not in non_dominated:
                dominated.append(p)
        return dominated

    def checkpoint(self) -> None:
        """Save the current state of the data model, since Streamlit is stateless by design."""
        st.session_state[self.streamlit_indentifier] = self
