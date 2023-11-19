from typing import Any
import pandas as pd
import streamlit as st
from matplotlib.figure import Figure
import plotly.graph_objects as go
from numpy import mean
from ..algorithms.interface import Point, OWDAlgorithm, BenchmarkAnalyzer


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

    def __init__(self, model: Model, view: "AlgorithmRunnerView", algorithms: dict[str, OWDAlgorithm]) -> None:
        self.model = model
        self.view = view
        self.supported_algorithms = algorithms
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
        chosen_algorithm = self.supported_algorithms[algorithm]
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
        for algorithm_name in self.supported_algorithms.keys():
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

    def plot_2Dfigure(self) -> Figure:
        x_dom = [p.x[0] for p in self.model.dominated_points]
        y_dom = [p.x[1] for p in self.model.dominated_points]
        x_non_dom = [p.x[0] for p in self.model.non_dominated_points]
        y_non_dom = [p.x[1] for p in self.model.non_dominated_points]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_dom, y=y_dom, mode='markers',
                                 name='dominated', marker_symbol='circle', marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=x_non_dom, y=y_non_dom, mode='markers',
                                 name='not dominated', marker_symbol='circle', marker=dict(size=10)))

        fig.update_layout(
            xaxis_title=self.model.labels[0],
            yaxis_title=self.model.labels[1],
            legend=dict(x=1.1, y=0.5),
        )

        return fig

    def plot_3Dfigure(self) -> Figure:
        x_dom = [p.x[0] for p in self.model.dominated_points]
        y_dom = [p.x[1] for p in self.model.dominated_points]
        z_dom = [p.x[2] for p in self.model.dominated_points]
        x_non_dom = [p.x[0] for p in self.model.non_dominated_points]
        y_non_dom = [p.x[1] for p in self.model.non_dominated_points]
        z_non_dom = [p.x[2] for p in self.model.non_dominated_points]

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x_dom, y=y_dom, z=z_dom, mode='markers', name='dominated',
                                   marker=dict(symbol='circle', size=5, opacity=0.6)))
        fig.add_trace(go.Scatter3d(x=x_non_dom, y=y_non_dom, z=z_non_dom, mode='markers', name='not dominated',
                                   marker=dict(symbol='circle', size=5, opacity=0.6)))

        fig.update_layout(
            scene=dict(
                xaxis_title=self.model.labels[0],
                yaxis_title=self.model.labels[1],
                zaxis_title=self.model.labels[2],
            ),
            legend=dict(x=1.1, y=0.5),
        )

        return fig

    def plot_4Dfigure(self) -> Figure:
        x_dom = [p.x[0] for p in self.model.dominated_points]
        y_dom = [p.x[1] for p in self.model.dominated_points]
        z_dom = [p.x[2] for p in self.model.dominated_points]
        c_dom = [p.x[3] for p in self.model.dominated_points]
        x_non_dom = [p.x[0] for p in self.model.non_dominated_points]
        y_non_dom = [p.x[1] for p in self.model.non_dominated_points]
        z_non_dom = [p.x[2] for p in self.model.non_dominated_points]
        c_non_dom = [p.x[3] for p in self.model.non_dominated_points]

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x_dom, y=y_dom, z=z_dom, mode='markers', name='dominated',
                                   marker=dict(symbol='circle', size=5, opacity=0.6, color=c_dom,
                                               colorscale='Blues', colorbar=dict(),
                                               colorbar_x=-0.07)))
        fig.add_trace(go.Scatter3d(x=x_non_dom, y=y_non_dom, z=z_non_dom, mode='markers', name='not dominated',
                                   marker=dict(symbol='circle', size=5, opacity=0.6, color=c_non_dom,
                                               colorscale='Reds', colorbar=dict(),
                                               colorbar_x=0.07)))

        fig.update_layout(
            scene=dict(
                xaxis_title=self.model.labels[0],
                yaxis_title=self.model.labels[1],
                zaxis_title=self.model.labels[2],
            ),
            legend=dict(x=1.1, y=0.5),
            annotations=[
                dict(
                    text=self.model.labels[3],
                    font_size=16,
                    font_family='arial',
                    font_color='white',
                    textangle=90,
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.025,
                    y=0.32
                )
            ]
        )

        return fig

    def is_table_cached(self) -> bool:
        return self.cached_table in st.session_state

    def is_json_cached(self) -> bool:
        return self.cached_json in st.session_state

    def is_figure_cached(self) -> bool:
        return self.cached_figure in st.session_state

    def clear_cache(self) -> None:
        if self.cached_table in st.session_state:
            del st.session_state[self.cached_table]
        if self.cached_json in st.session_state:
            del st.session_state[self.cached_json]
        if self.cached_figure in st.session_state:
            del st.session_state[self.cached_figure]


class AlgorithmRunnerView:

    def __init__(self, title: str) -> None:
        self.title = title

    def init_ui(self, presenter: AlgorithmRunnerPresenter) -> None:
        st.subheader(self.title, divider=True)

        left, right = st.columns([2, 2])

        with left:
            self.selected_algorithm = st.selectbox(
                "Algorytm OWD", options=list(presenter.supported_algorithms.keys())
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

        if presenter.is_figure_cached() and presenter.is_table_cached():
            self.display_figure_with_table(figure=st.session_state[presenter.cached_figure],
                                           table_data=st.session_state[presenter.cached_table])
        elif presenter.is_figure_cached() and presenter.is_json_cached():
            self.display_figure_with_json(figure=st.session_state[presenter.cached_figure],
                                          json=st.session_state[presenter.cached_json])
        elif presenter.is_json_cached():
            self.display_json(st.session_state[presenter.cached_json])
        elif presenter.is_table_cached():
            self.display_table(st.session_state[presenter.cached_table])
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
            figure.update_layout(margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(figure, use_container_width=True, use_container_height=True)
        with right:
            st.subheader("Rozwiązanie", divider=True)
            st.json(json)

    def display_figure_with_table(self, figure: Figure, table_data: dict) -> None:
        """For results of benchmark run on 2/3/4 dimensional problems."""
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Wizualizacja", divider=True)
            figure.update_layout(margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(figure, use_container_width=True, use_container_height=True)
        with right:
            st.subheader("Analiza Benchmark", divider=True)
            st.data_editor(
                table_data, disabled=True
            )

    def display_table(self, table_data: dict) -> None:
        """For 5+ dimensional problems (can't plot that)."""
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Wizualizacja", divider=True)
            st.info("Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych.")
        with right:
            st.subheader("Analiza Benchmark", divider=True)
            st.data_editor(
                table_data, disabled=True
            )

    def display_no_visualization_message_banner(self) -> None:
        """Initial message about visualization"""
        st.subheader("Wizualizacja", divider=True)
        st.info("Wizualizacja jest możliwa jedynie dla problemów 2/3/4 wymiarowych.")
