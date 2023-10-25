from typing import Protocol
import streamlit as st
import pandas as pd


class Model(Protocol):
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

    def update_criteria_model(self, updated: pd.DataFrame) -> None:
        self.model.labels = updated["Nazwa"].tolist()
        self.model.directions = updated["Kierunek"].tolist()


class CriteriaEditorView:
    streamlit_indentifier = "criteria_editor"

    def __init__(self) -> None:
        self.clear_editor()

    def init_ui(self, presenter: CriteriaPresenter) -> None:
        st.subheader("Edytor kryteriów", divider=True)
        edited_df = st.data_editor(
            presenter.get_model(),
            key=self.streamlit_indentifier,
            num_rows="dynamic",
            column_config={
                "Nazwa": st.column_config.TextColumn(
                    "Nazwa", width="large", default="Nowe Kryterium", required=True
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
        presenter.update_criteria_model(edited_df)

    def clear_editor(self) -> None:
        if self.streamlit_indentifier in st.session_state:
            del st.session_state[self.streamlit_indentifier]
