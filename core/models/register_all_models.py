from .register_model import RegisterModel
from core.utilities.getAll_models import get_all_models

def register_all_models(db):
    registrar = RegisterModel()

    for model in get_all_models():
        if hasattr(model, "__tablename__"):
            registrar.register_model_in_model(db, model)
