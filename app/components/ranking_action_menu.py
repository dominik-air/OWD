from typing import Protocol
import streamlit as st
from ..algorithms.interface import RankingMethod, RANKING_ALGORITHMS


class Model(Protocol):
    def process_points_with_ranking_method(self, algorithm: RankingMethod) -> None:
        ...


class RankingActionMenuPresenter:
    def __init__(self, model: Model, view: "RankingActionMenuView") -> None:
        self.model = model
        self.view = view
        self.supported_algorithms = RANKING_ALGORITHMS
        self.view.init_ui(self)

    def run_algorithm(self) -> None:
        algorithm = self.supported_algorithms[self.view.selected_algorithm]
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
