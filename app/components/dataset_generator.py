import streamlit as st
from numpy.random import exponential, normal, poisson, uniform


class Model:
    @property
    def data(self) -> list[tuple[int | float]]:
        ...

    @data.setter
    def data(self, data: list[tuple[int | float]]) -> None:
        ...

    @property
    def labels(self) -> list[str]:
        ...


class DatasetGeneratorPresenter:
    def __init__(self, model: Model, view: "DatasetGeneratorView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def generate_dataset(self, params) -> None:
        # TODO: needs a refactor, there is a better way of doing this
        data_shape = (params["obj_count"], len(self.model.labels))
        if params["dist"] == "Gaussa":
            data = normal(loc=params["mean"], scale=params["std"], size=data_shape)
        elif params["dist"] == "Poissona":
            data = poisson(lam=params["lambda"], size=data_shape)
        elif params["dist"] == "Wykładniczy":
            data = exponential(lam=params["lambda"], size=data_shape)
        elif params["dist"] == "Jednostajny":
            data = uniform(low=params["a"], high=params["b"], size=data_shape)
        else:
            raise ValueError
        self.model.data = data.tolist()


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
        dist = st.selectbox(
            "Rozkład",
            key="distribution_selector",
            options=list(self.distribution_to_parameters.keys()),
        )

        self.generator_params["dist"] = dist

        self.distribution_to_parameters[dist]()

        left, middle, right = st.columns([1, 1, 2])
        with left:
            if st.button("Generuj"):
                presenter.generate_dataset(self.generator_params)
        with middle:
            st.button("Sortuj")
        with right:
            st.selectbox("Sortowanie po kryterium:", options=[1, 2, 3])

    def _display_gauss_parameters(self):
        left, middle, right = st.columns(3)
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
            obj_count = st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )
            self.generator_params["obj_count"] = obj_count

    def _display_uniform_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            a, b = st.slider("Przedział", -50, 50, (-5, 5))
            self.generator_params["a"] = a
            self.generator_params["b"] = b
        with right:
            obj_count = st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )
            self.generator_params["obj_count"] = obj_count

    def _display_exponential_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            lambda_ = st.number_input(
                "Lambda", value=1.0, min_value=0.0, max_value=10.0, step=0.1
            )
            self.generator_params["lambda"] = lambda_
        with right:
            obj_count = st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )
            self.generator_params["obj_count"] = obj_count

    def _display_poisson_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            lambda_ = st.number_input(
                "Lambda", value=1, min_value=-10, max_value=10, step=1
            )
            self.generator_params["lambda"] = lambda_
        with right:
            obj_count = st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )
            self.generator_params["obj_count"] = obj_count
