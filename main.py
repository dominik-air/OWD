import streamlit as st
from app.model import DataPointModel
from app.view import WebAppView
from app.presenter import Presenter

if __name__ == "__main__":
    view = WebAppView()
    if "data_model" in st.session_state:
        model = st.session_state["data_model"]
    else:
        model = DataPointModel()
    presenter = Presenter(model, view)
