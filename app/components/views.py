from typing import Protocol
import streamlit as st
from matplotlib.figure import Figure
from ..algorithms.interface import ALGORITHMS


class Presenter(Protocol):
    def load_data(self) -> None:
        ...

    def run_algorithm(self) -> None:
        ...


class WebAppView:
    def __init__(self) -> None:
        if "initialized" not in st.session_state:
            st.session_state["initialized"] = True
            st.session_state["algorithm_selectbox_disabled"] = True
            st.session_state["run_button_disabled"] = True

    def init_ui(self, presenter: Presenter) -> None:
        left, middle, right = st.columns([1, 1, 2])
        with left:
            st.button("Load data", on_click=presenter.load_data)
        with right:
            self._selected_algorithm = st.selectbox(
                "OWD algorithm",
                options=list(ALGORITHMS.keys()),
                on_change=self.enable_run_button,
                disabled=st.session_state["algorithm_selectbox_disabled"],
            )
        with middle:
            st.button(
                "Run algorithm",
                disabled=st.session_state["run_button_disabled"],
                on_click=presenter.run_algorithm,
            )

    @property
    def selected_algorithm(self) -> str:
        return self._selected_algorithm

    def enable_algorithm_selectbox(self) -> None:
        st.session_state["algorithm_selectbox_disabled"] = False

    def enable_run_button(self) -> None:
        st.session_state["run_button_disabled"] = False

    def display_results(self, figure: Figure) -> None:
        st.pyplot(figure)
