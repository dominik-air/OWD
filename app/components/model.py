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

    def process_points_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
        non_dominated = algorithm(self.points)
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
