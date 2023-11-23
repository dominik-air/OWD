import streamlit as st
from ..algorithms.interface import Ranking, RankingMethod, RANKING_ALGORITHMS


class RankingActionMenuPresenter:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        self.supported_algorithms = RANKING_ALGORITHMS
        self.view.init_ui(self)

    def run_algorithm(self) -> None:
        self.execute_the_algorithm(self.view.selected_algorithm)
        self.prepare_results_json()
        self.prepare_proper_figure()


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
            st.subheader(self.title, divider=True)
            st.button("Stwórz ranking", on_click=presenter.run_algorithm)
