from typing import Protocol
import streamlit as st
import pandas as pd


class Model(Protocol):
    @property
    def data(self) -> list[tuple[int | float]]:
        ...

    @data.setter
    def data(self, data: list[tuple[int | float]]) -> None:
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

    def save_data_to_model(self, dataframe: pd.DataFrame) -> None:
        self.model.data = dataframe.values.tolist()
        self.model.labels = dataframe.columns.tolist()


class DataTableView:
    streamlit_indentifier = "data_table_view"

    def __init__(self) -> None:
        self.clear_display()

    def init_ui(self, presenter: DataTablePresenter) -> None:
        st.subheader("Podgląd zbioru danych", divider=True)
        st.data_editor(
            presenter.load_dataframe(), key=self.streamlit_indentifier, disabled=True
        )

    def clear_display(self):
        if self.streamlit_indentifier in st.session_state:
            del st.session_state[self.streamlit_indentifier]
