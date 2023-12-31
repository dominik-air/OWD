import streamlit as st
from app.components.model import get_model
from app.components.criteria_editor import CriteriaEditorView, CriteriaPresenter
from app.components.dataset_display import (
    DataTableView,
    DataTablePresenter,
    build_data_table_view_df,
)
from app.components.dataset_generator import (
    DatasetGeneratorView,
    DatasetGeneratorPresenter,
)
from app.components.dataset_loader import (
    DatasetLoaderView,
    DatasetLoaderPresenter,
    CSVDatasetLoader,
)
from app.components.naive_action_menu import (
    NaiveActionMenuView,
    NaiveActionMenuPresenter,
)

st.set_page_config(
    page_title="Optymalizacja wielokryterialna - Algorytmy naiwne", layout="wide"
)
st.title("Algorytmy naiwne")

# models
model = get_model("naive-algorithms-model")

# layout
left, right = st.columns(2)
with left:
    criteria_editor_placeholder = st.empty()
    dataset_generator_placeholder = st.empty()
with right:
    datatable_placeholder = st.empty()
    dataset_loader_placeholder = st.empty()
algorithm_runner_placeholder = st.empty()

# views
dataset_loader_view = DatasetLoaderView("Moduł ładujący zbiór danych")
criteria_view = CriteriaEditorView("Edytor kryteriów")
dataset_generator_view = DatasetGeneratorView("Generator zbioru danych")
datatable_view = DataTableView("Podgląd zbioru danych")
algorithm_runner_view = NaiveActionMenuView("Akcje")

# presenters
with dataset_loader_placeholder.container():
    DatasetLoaderPresenter(
        model=model, view=dataset_loader_view, loader=CSVDatasetLoader()
    )
with criteria_editor_placeholder.container():
    CriteriaPresenter(model=model, view=criteria_view)
with dataset_generator_placeholder.container():
    DatasetGeneratorPresenter(model=model, view=dataset_generator_view)
with datatable_placeholder.container():
    DataTablePresenter(
        model=model, view=datatable_view, build_df=build_data_table_view_df
    )
with algorithm_runner_placeholder.container():
    NaiveActionMenuPresenter(model=model, view=algorithm_runner_view)
