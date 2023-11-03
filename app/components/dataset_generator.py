import streamlit as st
import numpy as np
from numpy.random import exponential, normal, poisson, uniform


class Model:
    @property
    def data(self) -> np.ndarray:
        ...

    @data.setter
    def data(self, data: np.ndarray) -> None:
        ...

    @property
    def labels(self) -> list[str]:
        ...

    @property
    def directions(self) -> list[str]:
        ...


class DatasetGeneratorPresenter:
    def __init__(self, model: Model, view: "DatasetGeneratorView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def get_criterias(self) -> list[str]:
        return self.model.labels

    def generate_dataset(self, params) -> None:
        data_shape = (params["obj_count"], len(self.model.labels))
        distribution_functions = {
            "Gaussa": lambda: normal(
                loc=params["mean"], scale=params["std"], size=data_shape
            ),
            "Poissona": lambda: poisson(lam=params["lambda"], size=data_shape),
            "Wykładniczy": lambda: exponential(scale=params["lambda"], size=data_shape),
            "Jednostajny": lambda: uniform(
                low=params["a"], high=params["b"], size=data_shape
            ),
        }
        if params["dist"] not in distribution_functions:
            raise ValueError
        self.model.data = distribution_functions[params["dist"]]()

    def sort_by(self, criteria_name: str) -> None:
        col_index = self.model.labels.index(criteria_name)
        ascending = self.model.directions[col_index] == "Min"
        sorted_data = self.model.data[self.model.data[:, col_index].argsort()]
        self.model.data = sorted_data if ascending else sorted_data[::-1]


class DatasetGeneratorView:
    def __init__(self) -> None:
        self.distribution_to_parameters = {
            "Gaussa": self._display_gauss_parameters,
            "Poissona": self._display_poisson_parameters,
            "Wykładniczy": self._display_exponential_parameters,
            "Jednostajny": self._display_uniform_parameters,
        }

        self.generator_params = {}

    def init_ui(self, presenter: DatasetGeneratorPresenter) -> None:
        st.subheader("Generator zbioru danych", divider=True)

        left, right = st.columns([3, 1])
        with left:
            dist = st.selectbox(
                "Rozkład",
                key="distribution_selector",
                options=list(self.distribution_to_parameters.keys()),
            )

        with right:
            self._display_dataset_count()

        self.generator_params["dist"] = dist

        self.distribution_to_parameters[dist]()

        left, _, right = st.columns([1, 1, 2])
        with left:
            if st.button("Generuj"):
                presenter.generate_dataset(self.generator_params)
        with right:
            criteria = st.selectbox(
                "Sortowanie po kryterium:", options=presenter.get_criterias()
            )
            if st.button("Sortuj"):
                presenter.sort_by(criteria)

    def _display_object_count(self) -> None:
        obj_count = st.number_input(
            "Liczba obiektów", value=100, min_value=20, max_value=2000, step=100
        )
        self.generator_params["obj_count"] = obj_count

    def _display_dataset_count(self) -> None:
        dataset_count = st.number_input(
            "Liczba zbiorów danych", value=20, min_value=10, max_value=100, step=10
        )
        self.generator_params["dataset_count"] = dataset_count

    def _display_gauss_parameters(self):
        left, middle, right = st.columns([3, 3, 2])
        with left:
            mean = st.number_input(
                "Średnia", value=0, min_value=-10, max_value=10, step=1
            )
            self.generator_params["mean"] = mean
        with middle:
            std = st.number_input(
                "Odchylenie", value=1, min_value=-10, max_value=10, step=1
            )
            self.generator_params["std"] = std
        with right:
            self._display_object_count()

    def _display_uniform_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            a, b = st.slider("Przedział", -50, 50, (-5, 5))
            self.generator_params["a"] = a
            self.generator_params["b"] = b
        with right:
            self._display_object_count()

    def _display_exponential_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            lambda_ = st.number_input(
                "Lambda", value=1.0, min_value=0.0, max_value=10.0, step=0.1
            )
            self.generator_params["lambda"] = lambda_
        with right:
            self._display_object_count()

    def _display_poisson_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            lambda_ = st.number_input(
                "Lambda", value=1, min_value=-10, max_value=10, step=1
            )
            self.generator_params["lambda"] = lambda_
        with right:
            self._display_object_count()
