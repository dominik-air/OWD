import streamlit as st
from app.components.model import Model
from app.components.criteria_editor import CriteriaEditorView, CriteriaPresenter
from app.components.dataset_display import DataTableView, DataTablePresenter
from app.components.dataset_generator import (
    DatasetGeneratorView,
    DatasetGeneratorPresenter,
)
from app.components.dataset_loader import DatasetLoaderView, DatasetLoaderPresenter
from app.components.algorithm_runner import AlgorithmRunnerView, AlgorithmRunnerPresenter

# models
if Model.streamlit_indentifier in st.session_state:
    model = st.session_state[Model.streamlit_indentifier]
else:
    model = Model()

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
dataset_loader_view = DatasetLoaderView()
criteria_view = CriteriaEditorView()
dataset_generator_view = DatasetGeneratorView()
datatable_view = DataTableView()
algorithm_runner_view = AlgorithmRunnerView()

# presenters
with dataset_loader_placeholder.container():
    DatasetLoaderPresenter(model=model, view=dataset_loader_view)
with criteria_editor_placeholder.container():
    CriteriaPresenter(model=model, view=criteria_view)
with dataset_generator_placeholder.container():
    DatasetGeneratorPresenter(model=model, view=dataset_generator_view)
with datatable_placeholder.container():
    DataTablePresenter(model=model, view=datatable_view)
with algorithm_runner_placeholder.container():
    AlgorithmRunnerPresenter(model=model, view=algorithm_runner_view)
