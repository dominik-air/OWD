import streamlit as st


class DatasetGeneratorView:
    def __init__(self) -> None:
        self.distribution_to_parameters = {
            "Gaussa": self._display_gauss_parameters,
            "Poissona": self._display_poisson_parameters,
            "Wykładniczy": self._display_exponential_parameters,
            "Jednostajny": self._display_uniform_parameters,
        }

    def init_ui(self) -> None:
        dist = st.selectbox(
            "Rozkład", options=list(self.distribution_to_parameters.keys())
        )

        self.distribution_to_parameters[dist]()

        left, middle, right = st.columns([1, 1, 2])
        with left:
            st.button("Generuj")
        with middle:
            st.button("Sortuj")
        with right:
            st.selectbox("Sortowanie po kryterium:", options=[1, 2, 3])

    def _display_gauss_parameters(self):
        left, middle, right = st.columns(3)
        with left:
            st.number_input("Średnia", value=0, min_value=-10, max_value=10, step=1)
        with middle:
            st.number_input("Odchylenie", value=1, min_value=-10, max_value=10, step=1)
        with right:
            st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )

    def _display_uniform_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            st.slider("Przedział", -50, 50, (-5, 5))
        with right:
            st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )

    def _display_exponential_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            st.number_input(
                "Lambda", value=1.0, min_value=0.0, max_value=10.0, step=0.1
            )
        with right:
            st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )

    def _display_poisson_parameters(self):
        left, right = st.columns([3, 1])
        with left:
            st.number_input("Lambda", value=1, min_value=-10, max_value=10, step=1)
        with right:
            st.number_input(
                "Liczba obiektów", value=20, min_value=10, max_value=100, step=10
            )


DatasetGeneratorView().init_ui()
