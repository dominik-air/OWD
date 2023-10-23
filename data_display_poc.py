import streamlit as st
import pandas as pd


class Model:
    streamlit_indentifier = "model"

    def __init__(self) -> None:
        self._data = pd.DataFrame(
            {
                "Kryterium 1": [1, 1, 1, 1, 1],
                "Kryterium 2": [2, 2, 2, 2, 2],
                "Kryterium 3": [3, 3, 3, 3, 3],
            }
        )
        if self.streamlit_indentifier not in st.session_state:
            st.session_state[self.streamlit_indentifier] = self

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
        self.checkpoint()

    def checkpoint(self) -> None:
        """Save the current state of the criteria model, since Streamlit is stateless by design."""
        st.session_state[self.streamlit_indentifier] = self


class Presenter:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        self.view.init_ui(self)

    def load_data(self):
        return self.model.data

    def save_data_to_model(self, new_data):
        self.model.data = new_data


class DataTableView:
    streamlit_indentifier = "data_table_view"

    def init_ui(self, presenter) -> None:
        uploaded_file = st.file_uploader("Dodaj z csv")
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file, index_col=0)
            presenter.save_data_to_model(dataframe)
            self.clear_display()
        st.data_editor(
            presenter.load_data(), key=self.streamlit_indentifier, disabled=True
        )

    def clear_display(self):
        if self.streamlit_indentifier in st.session_state:
            del st.session_state[self.streamlit_indentifier]


view = DataTableView()
if Model.streamlit_indentifier not in st.session_state:
    model = Model()
else:
    model = st.session_state[Model.streamlit_indentifier]
presenter = Presenter(model=model, view=view)
