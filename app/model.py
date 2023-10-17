import streamlit as st
from .algorithms.point import Point
from .algorithms.interface import OWDAlgorithm


class DataPointModel:
    def __init__(self) -> None:
        self._data: list[Point] = []
        self._dominated: list[Point] = []
        self._non_dominated: list[Point] = []

        if "data_model" not in st.session_state:
            st.session_state["data_model"] = self

    @property
    def data(self) -> list[Point]:
        return self._data

    @data.setter
    def data(self, value: list[Point]) -> None:
        self._data = value
        self.checkpoint()

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
        self.checkpoint()

    def _filter_non_dominated(self, non_dominated: list[Point]) -> list[Point]:
        dominated = []
        for p in self.data:
            if p not in non_dominated:
                dominated.append(p)
        return dominated

    def checkpoint(self) -> None:
        """Save the current state of the data model, since Streamlit is stateless by design."""
        st.session_state["data_model"] = self
