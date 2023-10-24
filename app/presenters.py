from typing import Protocol
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .algorithms.point import Point
from .algorithms.interface import OWDAlgorithm, ALGORITHMS
from .algorithms.point import create_points_from_datapoints


class Model(Protocol):
    @property
    def data(self) -> list[Point]:
        ...

    @data.setter
    def data(self, value: list[Point]) -> None:
        ...

    @property
    def dominated(self) -> list[Point]:
        ...

    @property
    def non_dominated(self) -> list[Point]:
        ...

    def process_data_with_algorithm(self, algorithm: OWDAlgorithm) -> None:
        ...


class View(Protocol):
    def init_ui(self, presenter: "Presenter") -> None:
        ...

    @property
    def selected_algorithm(self) -> str:
        ...

    def enable_algorithm_selectbox(self) -> None:
        ...

    def display_results(self, figure: Figure) -> None:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        view.init_ui(self)

    def load_data(self) -> None:
        test_datapoints = [
            (5, 5),
            (3, 6),
            (4, 4),
            (5, 3),
            (3, 3),
            (1, 8),
            (3, 4),
            (4, 5),
            (3, 10),
            (6, 6),
            (4, 1),
            (3, 5),
        ]

        points = create_points_from_datapoints(test_datapoints)
        self.model.data = points
        self.view.enable_algorithm_selectbox()

    def run_algorithm(self) -> None:
        algorithm = ALGORITHMS[self.view.selected_algorithm]
        self.model.process_data_with_algorithm(algorithm)
        x = [p.x[0] for p in self.model.dominated]
        y = [p.x[1] for p in self.model.dominated]
        fig, ax = plt.subplots()
        plt.grid()
        ax.scatter(x, y, c="r", label="dominated", zorder=3)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Data points")

        x = [p.x[0] for p in self.model.non_dominated]
        y = [p.x[1] for p in self.model.non_dominated]
        ax.scatter(x, y, c="g", label="not dominated", zorder=3)
        plt.legend()
        self.view.display_results(fig)
