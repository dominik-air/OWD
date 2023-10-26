import streamlit as st
from app.components.model import Model
from app.components.criteria_editor import CriteriaEditorView, CriteriaPresenter
from app.components.dataset_display import DataTableView, DataTablePresenter
from app.components.dataset_generator import DatasetGeneratorView, DatasetGeneratorPresenter
from app.components.dataset_loader import DatasetLoaderView, DataserLoaderPresenter

st.set_page_config(page_title="Optymalizacja wielokryterialna", layout="wide")
st.title("Optymalizacja wielokryterialna")


if Model.streamlit_indentifier in st.session_state:
    model = st.session_state[Model.streamlit_indentifier]
else:
    model = Model()

left, right = st.columns(2)
with left:
    dataset_loader_view = DatasetLoaderView()
    dataset_loader_presenter = DataserLoaderPresenter(model=model, view=dataset_loader_view)
    
    criteria_view = CriteriaEditorView()
    criteria_presenter = CriteriaPresenter(model=model, view=criteria_view)

    dataset_generator_view = DatasetGeneratorView()
    dataset_generator_presenter = DatasetGeneratorPresenter(model=model, view=dataset_generator_view)

with right:
    datatable_view = DataTableView()
    datatable_presenter = DataTablePresenter(model=model, view=datatable_view)
