from typing import Any
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.cm as cm
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

        match len(self.model.labels):
            case 2:
                figure = self.plot_2Dfigure()
                st.session_state[self.cached_figure] = figure
            case 3:
                figure = self.plot_3Dfigure()
                st.session_state[self.cached_figure] = figure
            case 4:
                figure = self.plot_4Dfigure()
                st.session_state[self.cached_figure] = figure
            case _:
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

    def plot_2Dfigure(self) -> Figure:
        fig, ax = plt.subplots()

        x = [p.x[0] for p in self.model.dominated_points]
        y = [p.x[1] for p in self.model.dominated_points]
        ax.scatter(x, y, marker="o", label="dominated", zorder=3)

        x = [p.x[0] for p in self.model.non_dominated_points]
        y = [p.x[1] for p in self.model.non_dominated_points]
        ax.scatter(x, y, marker="^", label="not dominated", zorder=3)

        plt.xlabel(self.model.labels[0])
        plt.ylabel(self.model.labels[1])
        plt.title("Wyniki działania algorytmu dla podanego zbioru")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.55))
        plt.grid()
        return fig

    def plot_3Dfigure(self) -> Figure:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = [p.x[0] for p in self.model.dominated_points]
        y = [p.x[1] for p in self.model.dominated_points]
        z = [p.x[2] for p in self.model.dominated_points]
        ax.scatter(x, y, z, marker="o", label="dominated", s=50, alpha=0.6)

        x = [p.x[0] for p in self.model.non_dominated_points]
        y = [p.x[1] for p in self.model.non_dominated_points]
        z = [p.x[2] for p in self.model.non_dominated_points]
        ax.scatter(x, y, z, marker="^", label="not dominated", s=50, alpha=0.6)

        ax.set_xlabel(self.model.labels[0])
        ax.set_ylabel(self.model.labels[1])
        ax.set_zlabel(self.model.labels[2])
        ax.set_title("Wyniki działania algorytmu dla podanego zbioru")
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.85))
        plt.grid()
        return fig

    def plot_4Dfigure(self) -> Figure:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_dominated = [p.x[0] for p in self.model.dominated_points]
        y_dominated = [p.x[1] for p in self.model.dominated_points]
        z_dominated = [p.x[2] for p in self.model.dominated_points]
        c_dominated = [p.x[3] for p in self.model.dominated_points]
        ax.scatter(x_dominated, y_dominated, z_dominated, c=c_dominated, cmap='rainbow',
                   marker="o", label="dominated", s=50, alpha=0.6)

        x_non_dominated = [p.x[0] for p in self.model.non_dominated_points]
        y_non_dominated = [p.x[1] for p in self.model.non_dominated_points]
        z_non_dominated = [p.x[2] for p in self.model.non_dominated_points]
        c_non_dominated = [p.x[3] for p in self.model.non_dominated_points]
        ax.scatter(x_non_dominated, y_non_dominated, z_non_dominated, c=c_non_dominated,
                   cmap='rainbow', marker="^", label="not dominated", s=50, alpha=0.6)

        ax.set_xlabel(self.model.labels[0])
        ax.set_ylabel(self.model.labels[1])
        ax.set_zlabel(self.model.labels[2])
        ax.set_title("Wyniki działania algorytmu dla podanego zbioru")

        sm = cm.ScalarMappable(cmap='rainbow')
        sm.set_array(c_non_dominated)
        cbar = plt.colorbar(sm, ax=ax, pad=0.15)
        cbar.set_label(self.model.labels[3], rotation=90, labelpad=15)

        ax.legend(loc='center right', bbox_to_anchor=(1, 0.9))
        ax.grid(True)
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
        right, left = st.columns([1, 1])
        with right:
            st.subheader("Wizualizacja", divider=True)
            st.info("Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych.")
        with left:
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
