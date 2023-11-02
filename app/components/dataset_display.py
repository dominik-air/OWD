from typing import Protocol
import numpy as np
import streamlit as st
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


class DataTablePresenter:
    def __init__(self, model: Model, view: "DataTableView") -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def load_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.model.data)
        df.columns = self.model.labels
        return df


class DataTableView:
    streamlit_indentifier = "data_table_view"

    def __init__(self) -> None:
        self.clear_display()

    def init_ui(self, presenter: DataTablePresenter) -> None:
        st.subheader("Podgląd zbioru danych", divider=True)
        st.data_editor(
            presenter.load_dataframe(),
            key=self.streamlit_indentifier,
            disabled=True,
            use_container_width=True,
        )

    def clear_display(self):
        if self.streamlit_indentifier in st.session_state:
            del st.session_state[self.streamlit_indentifier]
