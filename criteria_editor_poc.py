import streamlit as st
import pandas as pd


class CriteriaModel:
    streamlit_indentifier = "criteria_model"

    def __init__(self):
        self._names: list[str] = ["Kryterium 1", "Kryterium 2"]
        self._directions: list[str] = ["Min", "Min"]
        if self.streamlit_indentifier not in st.session_state:
            st.session_state[self.streamlit_indentifier] = self

    @property
    def names(self) -> list[str]:
        return self._names.copy()

    @property
    def directions(self) -> list[str]:
        return self._directions.copy()

    @names.setter
    def names(self, updated: list[str]) -> None:
        self._names = updated
        self.checkpoint()

    @directions.setter
    def directions(self, updated: list[str]) -> None:
        self._directions = updated
        self.checkpoint()

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({"Nazwa": self.names, "Kierunek": self.directions})

    def checkpoint(self) -> None:
        """Save the current state of the criteria model, since Streamlit is stateless by design."""
        st.session_state[self.streamlit_indentifier] = self


class CriteriaPresenter:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        view.init_ui(self)

    def get_model(self) -> pd.DataFrame:
        return self.model.to_dataframe()

    def update_criteria_model(self, updated: pd.DataFrame) -> None:
        self.model.names = updated["Nazwa"].tolist()
        self.model.directions = updated["Kierunek"].tolist()


class CriteriaEditorView:
    streamlit_indentifier = "criteria_editor"

    def __init__(self) -> None:
        self.clear_editor()

    def init_ui(self, presenter) -> None:
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


if CriteriaModel.streamlit_indentifier in st.session_state:
    model = st.session_state[CriteriaModel.streamlit_indentifier]
else:
    model = CriteriaModel()
view = CriteriaEditorView()
presenter = CriteriaPresenter(model=model, view=view)
