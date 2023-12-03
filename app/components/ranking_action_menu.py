from typing import Protocol
from functools import partial
import numpy as np
import streamlit as st
from ..algorithms.ideal_point import ideal_point_method
from ..algorithms.rsm import reference_set_method
from ..algorithms.interface import RankingMethod, OWDAlgorithm, RANKING_ALGORITHMS


class Model(Protocol):
    @property
    def class_names(self) -> list[str]:
        ...

    @property
    def class_data(self) -> np.ndarray:
        ...

    def process_points_with_naive_algorithm(self, algorithm: OWDAlgorithm) -> None:
        ...

    def process_points_with_ranking_method(self, algorithm: RankingMethod) -> None:
        ...

def build_rsm_with_reference_sets(model: Model) -> RankingMethod:
    ideal_bool_index = np.array([cn == "A1" for cn in model.class_names])
    status_quo_bool_index = np.array([cn == "A0" for cn in model.class_names])

    ideal = model.class_data[ideal_bool_index]
    status_quo = model.class_data[status_quo_bool_index]

    return partial(reference_set_method, ideal_points_set=ideal, status_quo_points_set=status_quo)


class RankingActionMenuPresenter:
    def __init__(self, model: Model, view: "RankingActionMenuView") -> None:
        self.model = model
        self.view = view
        self.supported_algorithms = RANKING_ALGORITHMS
        self.view.init_ui(self)

    def run_algorithm(self) -> None:
        algorithm = self.supported_algorithms[self.view.selected_algorithm]
        if algorithm == reference_set_method:
            algorithm = build_rsm_with_reference_sets(self.model)
        self.model.process_points_with_naive_algorithm(ideal_point_method)
        self.model.process_points_with_ranking_method(algorithm)

class RankingActionMenuView:
    def __init__(self, title: str) -> None:
        self.title = title

    def init_ui(self, presenter: RankingActionMenuPresenter) -> None:
        st.subheader(self.title, divider=True)
        left, right = st.columns([2, 1])
        with left:
            self.selected_algorithm = st.selectbox(
                "Metoda rankingowa", options=list(presenter.supported_algorithms.keys())
            )
        with right:
            st.button("Stwórz ranking", on_click=presenter.run_algorithm)
