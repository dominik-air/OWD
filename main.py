import streamlit as st
from app.models import DataPointModel
from app.views import WebAppView
from app.presenters import Presenter

if __name__ == "__main__":
    view = WebAppView()
    if "data_model" in st.session_state:
        model = st.session_state["data_model"]
    else:
        model = DataPointModel()
    presenter = Presenter(model, view)
