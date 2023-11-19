from typing import Protocol, TextIO
from dataclasses import dataclass, field
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

    @property
    def class_names(self) -> list[str]:
        ...

    @class_names.setter
    def class_names(self, class_names: list[str]) -> None:
        ...

    @property
    def class_data(self) -> np.ndarray:
        ...

    @class_data.setter
    def class_data(self, class_data: np.ndarray) -> None:
        ...

    @property
    def alternative_names(self) -> list[str]:
        ...

    @alternative_names.setter
    def alternative_names(self, alternative_names: list[str]) -> None:
        ...


class DatasetLoaderStrategy(Protocol):
    def read(self, file: TextIO) -> None:
        ...

    def populate_model(self, model: Model) -> None:
        ...


@dataclass
class CSVDatasetLoader:
    datapoints: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)

    def read(self, file: TextIO) -> None:
        self.datapoints = pd.read_csv(file, index_col=0)

    def populate_model(self, model: Model) -> None:
        model.data = self.datapoints.values
        model.directions = ["Min"] * len(self.datapoints.columns)
        model.labels = self.datapoints.columns.tolist()


@dataclass
class ExcelDatasetLoader:
    alternatives: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)
    classes: pd.DataFrame = field(init=False, default_factory=pd.DataFrame)

    def read(self, file: TextIO) -> None:
        raise NotImplementedError

    def populate_model(self, model: Model) -> None:
        raise NotImplementedError


class DatasetLoaderPresenter:
    def __init__(
        self, model: Model, view: "DatasetLoaderView", loader: DatasetLoaderStrategy
    ) -> None:
        self.model = model
        self.view = view
        self.loader = loader
        self.view.init_ui(self)

    def save_data_to_model(self, filename: str) -> None:
        self.loader.read(filename)
        self.loader.populate_model(self.model)


class DatasetLoaderView:

    def __init__(self, title: str) -> None:
        self.title = title

    def init_ui(self, presenter: DatasetLoaderPresenter) -> None:
        st.subheader("Moduł ładujący zbiór danych", divider=True)
        uploaded_file = st.file_uploader("Dodaj plik z danymi")
        if (
            uploaded_file is not None
            and self.get_current_uploaded_file() != uploaded_file.name
        ):
            self.save_current_uploaded_file(uploaded_file.name)
            presenter.save_data_to_model(uploaded_file)
        if uploaded_file is None:
            self.save_current_uploaded_file("")

    def save_current_uploaded_file(self, filename: str) -> None:
        st.session_state["current_uploaded_file"] = filename

    def get_current_uploaded_file(self) -> str:
        return st.session_state.get("current_uploaded_file", "")
