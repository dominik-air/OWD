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

    def get_default_new_criteria_name(self) -> str:
        index = 1
        new_criteria_name = f"Nowe Kryterium #{index}"
        while new_criteria_name in self.model.labels:
            index += 1
            new_criteria_name = f"Nowe Kryterium #{index}"
        return new_criteria_name

    def update_model(self, updated: pd.DataFrame) -> None:
        new_labels = updated["Nazwa"].tolist()
        new_directions = updated["Kierunek"].tolist()

        label_to_index = {label: idx for idx, label in enumerate(self.model.labels)}
        default_value = 0

        new_data_columns = []

        for label in new_labels:
            if label in label_to_index:
                new_data_columns.append(self.model.data[:, label_to_index[label]])
            else:
                new_data_columns.append(
                    np.full(self.model.data.shape[0], default_value)
                )
        new_data = np.column_stack(new_data_columns)

        self.model.data = new_data
        self.model.labels = new_labels
        self.model.directions = new_directions


class CriteriaEditorView:
    streamlit_indentifier = "criteria_editor"

    def init_ui(self, presenter: CriteriaPresenter) -> None:
        st.subheader("Edytor kryteriów", divider=True)
        edited_df = st.data_editor(
            presenter.get_model(),
            key=self.streamlit_indentifier,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "Nazwa": st.column_config.TextColumn(
                    "Nazwa",
                    width="large",
                    default=presenter.get_default_new_criteria_name(),
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
        presenter.update_model(edited_df)
