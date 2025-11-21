import importlib
from sqlalchemy.orm import registry, configure_mappers
from core.utilities.database import Base, engine

class LoadModulesMixin:
    
    def load_module(module_name):
        print(f"Registering models for module: {module_name}")
        model_package = f"addons.{module_name}.model"
        try:
            importlib.import_module(model_package)
            print(f"Loaded models for module: {module_name}")
        except ModuleNotFoundError:
            print(f"No models package for module: {module_name}")
        # registry.configure = lambda *args, **kwargs: None
        configure_mappers()
                
        # Base.metadata.create_all(bind=engine,checkfirst=True)