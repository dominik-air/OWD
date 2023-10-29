from typing import Protocol
import streamlit as st
import numpy as np
import pandas as pd


class Model(Protocol):
    @property
    def data(self) -> np.ndarray:
        ...

    @data.setter
    def data(self, data: np.ndarray) -> None:
        ...

    @property
    def labels(self) -> list[str]:
        ...

    @labels.setter
    def labels(self, labels: list[str]) -> None:
        ...

    @property
    def directions(self) -> list[str]:
        ...

    @directions.setter
    def directions(self, directions: list[str]) -> None:
        ...


class DataserLoaderPresenter:
    def __init__(self, model: Model, view: "DatasetLoaderView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def save_data_to_model(self, dataframe: pd.DataFrame) -> None:
        self.model.data = dataframe.values
        self.model.directions = ["Min"] * len(dataframe.columns.tolist())
        self.model.labels = dataframe.columns.tolist()


class DatasetLoaderView:
    def init_ui(self, presenter: DataserLoaderPresenter) -> None:
        st.subheader("Moduł ładujący zbiór danych", divider=True)
        uploaded_file = st.file_uploader("Dodaj plik z danymi")
        if (
            uploaded_file is not None
            and self.get_current_uploaded_file() != uploaded_file.name
        ):
            self.save_current_uploaded_file(uploaded_file.name)
            dataframe = pd.read_csv(uploaded_file, index_col=0)
            presenter.save_data_to_model(dataframe)
        if uploaded_file is None:
            self.save_current_uploaded_file("")

    def save_current_uploaded_file(self, filename: str) -> None:
        st.session_state["current_uploaded_file"] = filename

    def get_current_uploaded_file(self) -> str:
        return st.session_state.get("current_uploaded_file", "")
