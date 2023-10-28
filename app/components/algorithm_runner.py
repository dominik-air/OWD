from typing import Any
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from ..algorithms.interface import ALGORITHMS, Point, OWDAlgorithm


class Model:
    @property
    def labels(self) -> list[str]:
        ...

    @property
    def dominated_points(self) -> list[Point]:
        ...

    @property
    def non_dominated_points(self) -> list[Point]:
        ...

    def process_points_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
        ...

def point_to_json(p: Point, labels: list[str]) -> dict[str, Any]:
    return {labels[i]: p.x[i] for i in range(len(labels))}


class AlgorithmRunnerPresenter:

    cached_figure = "cached_figure"
    cached_json = "cached_json"

    def __init__(self, model: Model, view: "AlgorithmRunnerView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def run_algorithm(self) -> None:
        algorithm = ALGORITHMS[self.view.selected_algorithm]
        self.model.process_points_with_algorithm(algorithm)

        json = self.prepare_results_json()
        st.session_state[self.cached_json] = json

        # TODO: extend for 3D and 4D problems
        if len(self.model.labels) == 2:
            figure = self.plot_figure()
            st.session_state[self.cached_figure] = figure
        else:
            del st.session_state[self.cached_figure]

    def run_benchmark(self) -> None:
        raise NotImplementedError

    def prepare_results_json(self) -> dict[str, Any]:
        labels = self.model.labels
        return {
            "nondominated": [
                point_to_json(p, labels) for p in self.model.non_dominated_points
            ],
            "dominated": [
                point_to_json(p, labels) for p in self.model.dominated_points
            ],
        }

    def plot_figure(self) -> Figure:
        x = [p.x[0] for p in self.model.dominated_points]
        y = [p.x[1] for p in self.model.dominated_points]
        fig, ax = plt.subplots()
        plt.grid()
        ax.scatter(x, y, c="r", label="dominated", zorder=3)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Data points")

        x = [p.x[0] for p in self.model.non_dominated_points]
        y = [p.x[1] for p in self.model.non_dominated_points]
        ax.scatter(x, y, c="g", label="not dominated", zorder=3)
        plt.legend()
        return fig


class AlgorithmRunnerView:

    def init_ui(self, presenter: AlgorithmRunnerPresenter) -> None:

        st.subheader("Akcje", divider=True)

        left, middle, right = st.columns([2, 1, 1])

        with left:
            self.selected_algorithm = st.selectbox(
                "Algorytm OWD", options=list(ALGORITHMS.keys())
            )
        with middle:
            st.button("Rozwiąż", on_click=presenter.run_algorithm)
        with right:
            st.button("Benchmark", on_click=presenter.run_benchmark)
        
        if presenter.cached_figure in st.session_state:
            self.display_figure_with_json(figure=st.session_state[presenter.cached_figure],
                                          json=st.session_state[presenter.cached_json])
        elif presenter.cached_json in st.session_state:
            self.display_json(st.session_state[presenter.cached_json])

    def display_json(self, json: dict[str, Any]) -> None:
        """For benchmark results and 5+ dimensional problems (can't plot that)."""
        st.subheader("Rozwiązanie", divider=True)
        st.json(json)

    def display_figure_with_json(self, figure: Figure, json: dict[str, Any]) -> None:
        """For results of algorithms run on 2/3/4 dimensional problems."""
        right, left = st.columns([2, 1])
        with right:
            st.subheader("Wizualizacja", divider=True)
            st.pyplot(figure)
        with left:
            st.subheader("Rozwiązanie", divider=True)
            st.json(json)
