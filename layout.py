import streamlit as st
from criteria_editor_poc import CriteriaEditorView, CriteriaModel, CriteriaPresenter
from data_display_poc import DataTableView, Model, Presenter
from dataset_generator_poc import DatasetGeneratorView


st.set_page_config(page_title="Appka", layout="wide")
st.title("Optymalizacja wielokryterialna")

# todo:
# 1. Dodaj z csv powinno być odzielone od DataTableView
# 2. Sprawdzić czy się da zrobić obramówkę wokół komponentów w prosty sposób
# 3. Na prawo przenieść DataTableView
# 4. Czy da się w jakiś prosty sposób zrównać elementy ze sobą na szerokość/wysokość?

left, right = st.columns(2)
with left:
    if CriteriaModel.streamlit_indentifier in st.session_state:
        criteria_model = st.session_state[CriteriaModel.streamlit_indentifier]
    else:
        criteria_model = CriteriaModel()
    criteria_view = CriteriaEditorView()
    criteria_presenter = CriteriaPresenter(model=criteria_model, view=criteria_view)

    DatasetGeneratorView().init_ui()
with right:
    st.data_editor([[1, 2, 3]*5, [4, 5, 6]*5, [7, 8, 9]*5]*5)


datatable_view = DataTableView()
if Model.streamlit_indentifier not in st.session_state:
    datatable_model = Model()
else:
    datatable_model = st.session_state[Model.streamlit_indentifier]
datatable_presenter = Presenter(model=datatable_model, view=datatable_view)