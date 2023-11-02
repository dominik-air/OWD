from typing import Any
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from numpy import mean
import matplotlib.cm as cm
from ..algorithms.interface import ALGORITHMS, Point, OWDAlgorithm, BenchmarkAnalyzer


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

    @property
    def points(self) -> list[Point]:
        ...

    def process_points_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
        ...


def point_to_json(p: Point, labels: list[str]) -> dict[str, Any]:
    return {labels[i]: p.x[i] for i in range(len(labels))}


class AlgorithmRunnerPresenter:
    cached_figure = "cached_figure"
    cached_json = "cached_json"
    cached_table = "cached_table"

    def __init__(self, model: Model, view: "AlgorithmRunnerView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def run_algorithm(self) -> None:
        self.execute_the_algorithm(self.view.selected_algorithm)
        self.prepare_results_json()
        self.prepare_proper_figure()

    def run_benchmark(self) -> None:
        self.execute_the_algorithm(self.view.selected_algorithm)
        self.prepare_proper_figure()
        self.prepare_benchmark_table(
            len(self.model.labels), self.model.points, self.view.repeats_for_benchmark
        )

    def prepare_results_json(self) -> None:
        labels = self.model.labels
        json = {
            "nondominated": [
                point_to_json(p, labels) for p in self.model.non_dominated_points
            ],
            "dominated": [
                point_to_json(p, labels) for p in self.model.dominated_points
            ],
        }
        st.session_state[self.cached_json] = json

    def execute_the_algorithm(self, algorithm: str) -> None:
        chosen_algorithm = ALGORITHMS[algorithm]
        self.model.process_points_with_algorithm(chosen_algorithm)
        self.clear_cache()

    def prepare_proper_figure(self) -> None:
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
                return

    def prepare_benchmark_table(
        self, dimensionality: int, dataset: list[Point], repeats: int
    ) -> None:
        table_data = []
        for algorithm_name in ALGORITHMS.keys():
            benchmark = BenchmarkAnalyzer(algorithm_name, dimensionality, dataset)
            benchmark_result = benchmark.run_algorithm(repeats)
            data = {
                "Algorytm": algorithm_name,
                "Średni czas porównania (ms)": mean(benchmark_result["times"]) * 1000,
                "Średnia liczba porównań punktów": mean(
                    benchmark_result["comparison_point_counter"]
                ),
                "Średnia liczba porównań współrzędnych": mean(
                    benchmark_result["comparison_coordinates_counter"]
                ),
            }
            table_data.append(data)

        st.session_state[self.cached_table] = pd.DataFrame(table_data)

    def clear_cache(self) -> None:
        if self.cached_table in st.session_state:
            del st.session_state[self.cached_table]
        if self.cached_json in st.session_state:
            del st.session_state[self.cached_json]
        if self.cached_figure in st.session_state:
            del st.session_state[self.cached_figure]

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
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.55))
        plt.grid()
        return fig

    def plot_3Dfigure(self) -> Figure:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

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
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.85))
        plt.grid()
        return fig

    def plot_4Dfigure(self) -> Figure:
        fig = plt.figure()
        fig.set_size_inches(12, 12)
        ax = fig.add_subplot(111, projection="3d")

        x_dominated = [p.x[0] for p in self.model.dominated_points]
        y_dominated = [p.x[1] for p in self.model.dominated_points]
        z_dominated = [p.x[2] for p in self.model.dominated_points]
        c_dominated = [p.x[3] for p in self.model.dominated_points]
        ax.scatter(
            x_dominated,
            y_dominated,
            z_dominated,
            c=c_dominated,
            cmap="Blues",
            marker="o",
            label="dominated",
            s=50,
            alpha=0.6,
        )

        x_non_dominated = [p.x[0] for p in self.model.non_dominated_points]
        y_non_dominated = [p.x[1] for p in self.model.non_dominated_points]
        z_non_dominated = [p.x[2] for p in self.model.non_dominated_points]
        c_non_dominated = [p.x[3] for p in self.model.non_dominated_points]
        ax.scatter(
            x_non_dominated,
            y_non_dominated,
            z_non_dominated,
            c=c_non_dominated,
            cmap="Oranges",
            marker="^",
            label="not dominated",
            s=50,
            alpha=0.6,
        )

        ax.set_xlabel(self.model.labels[0])
        ax.set_ylabel(self.model.labels[1])
        ax.set_zlabel(self.model.labels[2])

        cax1 = fig.add_axes([0.13, 0.5, 0.03, 0.35])
        sm1 = cm.ScalarMappable(
            cmap="Blues", norm=Normalize(min(c_dominated), max(c_dominated))
        )
        sm1.set_array([])
        fig.colorbar(sm1, cax=cax1, orientation="vertical")

        cax2 = fig.add_axes([0.13, 0.1, 0.03, 0.35])
        sm2 = cm.ScalarMappable(
            cmap="Oranges", norm=Normalize(min(c_non_dominated), max(c_non_dominated))
        )
        sm2.set_array([])
        fig.colorbar(sm2, cax=cax2, orientation="vertical")

        fig.text(0.12, 0.5, self.model.labels[3], rotation=90, va="center", ha="right")

        dominated_proxy = plt.Line2D(
            [0],
            [0],
            linestyle="none",
            c="blue",
            marker="o",
            markersize=10,
            label="Dominated",
        )
        non_dominated_proxy = plt.Line2D(
            [0],
            [0],
            linestyle="none",
            c="orange",
            marker="^",
            markersize=10,
            label="Non-Dominated",
        )

        ax.legend(
            handles=[dominated_proxy, non_dominated_proxy],
            loc="center right",
            bbox_to_anchor=(1, 0.9),
        )
        ax.grid(True)
        return fig


class AlgorithmRunnerView:
    def init_ui(self, presenter: AlgorithmRunnerPresenter) -> None:
        st.subheader("Akcje", divider=True)

        left, right = st.columns([2, 2])

        with left:
            self.selected_algorithm = st.selectbox(
                "Algorytm OWD", options=list(ALGORITHMS.keys())
            )
            st.button("Rozwiąż", on_click=presenter.run_algorithm)
        with right:
            self.repeats_for_benchmark = st.number_input(
                "Liczba analizowanych powtórzeń",
                value=50,
                min_value=1,
                max_value=200,
                step=10,
            )
            st.button("Benchmark", on_click=presenter.run_benchmark)

        if (
            presenter.cached_figure in st.session_state
            and presenter.cached_table in st.session_state
        ):
            self.display_figure_with_table(
                figure=st.session_state[presenter.cached_figure],
                table_data=st.session_state[presenter.cached_table],
            )
        elif (
            presenter.cached_figure in st.session_state
            and presenter.cached_json in st.session_state
        ):
            self.display_figure_with_json(
                figure=st.session_state[presenter.cached_figure],
                json=st.session_state[presenter.cached_json],
            )
        elif presenter.cached_json in st.session_state:
            self.display_json(st.session_state[presenter.cached_json])
        elif presenter.cached_table in st.session_state:
            self.display_table(table_data=st.session_state[presenter.cached_table])
        else:
            self.display_no_visualization_message_banner()

    def display_json(self, json: dict[str, Any]) -> None:
        """For solving 5+ dimensional problems (can't plot that)."""
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Wizualizacja", divider=True)
            st.info(
                "Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych."
            )
        with right:
            st.subheader("Rozwiązanie", divider=True)
            st.json(json)

    def display_table(self, table_data: dict) -> None:
        """For benchmarking algortihms on 5+ dimensional problems (can't plot that)."""
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Wizualizacja", divider=True)
            st.info(
                "Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych."
            )
        with right:
            st.subheader("Analiza benchmark", divider=True)
            st.data_editor(table_data, disabled=True)

    def display_figure_with_json(self, figure: Figure, json: dict[str, Any]) -> None:
        """For results of algorithms run on 2/3/4 dimensional problems."""
        left, right = st.columns([2, 1])
        with left:
            st.subheader("Wizualizacja", divider=True)
            st.pyplot(figure)
        with right:
            st.subheader("Rozwiązanie", divider=True)
            st.json(json)

    def display_figure_with_table(self, figure: Figure, table_data: dict) -> None:
        st.subheader("Analiza Benchmark", divider=True)
        left, right = st.columns([1, 1])
        with left:
            st.pyplot(figure)
        with right:
            st.data_editor(table_data, disabled=True)

    def display_no_visualization_message_banner(self) -> None:
        st.subheader("Wizualizacja", divider=True)
        st.info("Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych.")
