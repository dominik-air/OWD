import streamlit as st
from app.components.model import Model
from app.components.dataset_display import (
    DataTableView,
    DataTablePresenter,
    build_alternatives_table_view_df,
    build_class_table_view_df,
    build_ranking_table_view_df,
)
from app.components.dataset_loader import (
    DatasetLoaderView,
    DatasetLoaderPresenter,
    ExcelDatasetLoader,
)
from app.components.ranking_action_menu import (
    RankingActionMenuPresenter,
    RankingActionMenuView,
)

st.set_page_config(
    page_title="Optymalizacja wielokryterialna - Metody rankingowe", layout="wide"
)
st.title("Metody rankingowe")

# models
if Model.streamlit_indentifier in st.session_state:
    model = st.session_state[Model.streamlit_indentifier]
else:
    model = Model()

# layout
left, right = st.columns(2)
with left:
    dataset_loader_placeholder = st.empty()
    alternatives_display_placeholder = st.empty()
with right:
    algorithm_runner_placeholder = st.empty()
    classes_display_placeholder = st.empty()
ranking_display_placeholder = st.empty()

# views
dataset_loader_view = DatasetLoaderView("Moduł ładujący zbiór danych")
alternatives_view = DataTableView("Alternatywy z kryteriami")
classes_view = DataTableView("Klasy")
ranking_view = DataTableView("Stworzony ranking")
algorithm_runner_view = RankingActionMenuView("Akcje")

# presenters
with dataset_loader_placeholder.container():
    DatasetLoaderPresenter(
        model=model, view=dataset_loader_view, loader=ExcelDatasetLoader()
    )
with algorithm_runner_placeholder.container():
    RankingActionMenuPresenter(model=model, view=algorithm_runner_view)
with alternatives_display_placeholder.container():
    DataTablePresenter(
        model=model, view=alternatives_view, build_df=build_alternatives_table_view_df
    )
with classes_display_placeholder.container():
    DataTablePresenter(
        model=model, view=classes_view, build_df=build_class_table_view_df
    )
with ranking_display_placeholder.container():
    DataTablePresenter(
        model=model, view=ranking_view, build_df=build_ranking_table_view_df
    )
