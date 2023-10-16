from app.model import DataPointModel
from app.view import WebAppView
from app.presenter import Presenter

if __name__ == "__main__":
    view = WebAppView()
    model = DataPointModel()
    presenter = Presenter(model, view)
