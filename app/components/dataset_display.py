from typing import Protocol, Callable
import numpy as np
import streamlit as st
import pandas as pd
from ..algorithms.types import Ranking
from .model import PropertyNotReadyError


class Model(Protocol):
    @property
    def data(self) -> np.ndarray:
        ...

    @property
    def labels(self) -> list[str]:
        ...

    @property
    def class_names(self) -> list[str]:
        ...

    @property
    def class_data(self) -> np.ndarray:
        ...

    @property
    def alternative_names(self) -> list[str]:
        ...

    @property
    def ranking(self) -> Ranking:
        ...


BuildDataframeFn = Callable[[Model], pd.DataFrame]


def build_data_table_view_df(model: Model) -> pd.DataFrame:
    df = pd.DataFrame(model.data)
    df.columns = model.labels
    return df


def build_alternatives_table_view_df(model: Model) -> pd.DataFrame:
    df = pd.DataFrame(model.data)
    df.columns = model.labels
    df.insert(0, "Nazwa alternatywy", model.alternative_names)
    return df


def build_class_table_view_df(model: Model) -> pd.DataFrame:
    df = pd.DataFrame(model.class_data)
    df.columns = model.labels
    df.insert(0, "Nazwa klasy", model.class_names)
    return df


def build_ranking_table_view_df(model: Model) -> pd.DataFrame:
    try:
        indices, scores = model.ranking
    except PropertyNotReadyError:
        return pd.DataFrame([])
    alternatives = [model.alternative_names[i] for i in indices]
    df = pd.DataFrame({"Wynik": scores})
    df.insert(0, "Nazwa alternatywy", alternatives)
    return df


class DataTablePresenter:
    def __init__(
        self, model: Model, view: "DataTableView", build_df: BuildDataframeFn
    ) -> None:
        self.model = model
        self.view = view
        self.build_df = build_df
        self.view.init_ui(self)

    def load_dataframe(self) -> pd.DataFrame:
        return self.build_df(self.model)


class DataTableView:
    def __init__(self, title: str) -> None:
        self.title = title
        self.streamlit_indentifier = title
        self.clear_display()

    def init_ui(self, presenter: DataTablePresenter) -> None:
        st.subheader(self.title, divider=True)
        st.data_editor(
            presenter.load_dataframe(),
            key=self.streamlit_indentifier,
            disabled=True,
            use_container_width=True,
        )

    def clear_display(self):
        if self.streamlit_indentifier in st.session_state:
            del st.session_state[self.streamlit_indentifier]
