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


class CriteriaPresenter:
    def __init__(self, model: Model, view: "CriteriaEditorView") -> None:
        self.model = model
        self.view = view
        view.init_ui(self)

    def get_model(self) -> pd.DataFrame:
        return pd.DataFrame(
            {"Nazwa": self.model.labels, "Kierunek": self.model.directions}
        )

    def get_columns(self) -> list[str]:
        return self.model.labels

    def get_default_new_criteria_name(self) -> str:
        index = 1
        new_criteria_name = f"Nowe Kryterium #{index}"
        while new_criteria_name in self.model.labels:
            index += 1
            new_criteria_name = f"Nowe Kryterium #{index}"
        return new_criteria_name

    def add_column(self) -> None:
        default_column_name = self.get_default_new_criteria_name()
        default_column_values = np.zeros(self.model.data.shape[0])
        self.model.labels.append(default_column_name)
        self.model.directions.append("Min")
        self.model.data = np.column_stack((self.model.data, default_column_values))

    def remove_column(self, column_name: str) -> None:
        if column_name in self.model.labels:
            idx = self.model.labels.index(column_name)
            self.model.directions.pop(idx)
            self.model.labels.pop(idx)
            self.model.data = np.delete(self.model.data, idx, axis=1)

    def update_model(self, updated: pd.DataFrame) -> None:
        self.model.labels = updated["Nazwa"].tolist()
        self.model.directions = updated["Kierunek"].tolist()


class CriteriaEditorView:
    def __init__(self, title: str) -> None:
        self.title = title
        self.streamlit_indentifier = "criteria_editor"

    def init_ui(self, presenter: CriteriaPresenter) -> None:
        st.subheader(self.title, divider=True)

        if st.button("Dodaj kolumnę"):
            presenter.add_column()

        self.delete_criteria_selector_placeholder = st.empty()
        column_to_remove = self.delete_criteria_selector_placeholder.selectbox(
            "Wybierz kolumnę do usunięcia", presenter.get_columns()
        )
        if st.button("Usuń kolumnę"):
            presenter.remove_column(column_to_remove)
            self.update_delete_criteria_selector(presenter.get_columns())

        self.update_edited_rows(presenter)

        st.data_editor(
            presenter.get_model(),
            key=self.streamlit_indentifier,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Nazwa": st.column_config.TextColumn(
                    "Nazwa",
                    width="large",
                    required=True,
                ),
                "Kierunek": st.column_config.SelectboxColumn(
                    "Kierunek",
                    width="medium",
                    default="Min",
                    options=["Min", "Max"],
                    required=True,
                ),
            },
        )

    def update_delete_criteria_selector(self, columns: list[str]) -> None:
        self.delete_criteria_selector_placeholder.selectbox(
            "Wybierz kolumnę do usunięcia", columns
        )

    def update_edited_rows(self, presenter: CriteriaPresenter) -> None:
        if self.streamlit_indentifier not in st.session_state:
            return
        edited_rows = st.session_state[self.streamlit_indentifier]["edited_rows"]
        if not edited_rows:
            return
        df = presenter.get_model()
        for row_id, columns in edited_rows.items():
            for column_name, column_value in columns.items():
                df.at[row_id, column_name] = column_value
        presenter.update_model(df)
        try:
            self.update_delete_criteria_selector(presenter.get_columns())
        except st.errors.DuplicateWidgetID:
            # there is no need to refresh, since the objects have the same parameters
            pass
