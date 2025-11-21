from sqlalchemy.orm import registry, configure_mappers, clear_mappers
from .initialize_db import CreateTableMixin 
from .read_init_file import LoadModulesMixin
from .register_all_models import register_all_models
from core.fields.register_fields import register_fields

class DynamicDBSaveForModules:
    """Placeholder class for saving module info to DB."""
    
    
    @staticmethod
    def save_model_to_db(db, module_name: str):
        # try:
        #     clear_mappers()
        # except Exception:
        #     pass

        LoadModulesMixin.load_module(module_name)
        CreateTableMixin.crud_on_model()
        register_all_models(db)
        register_fields(db)
    
    # try:
    #     from .register_all_models import register_all_models
    #     from core.fields.register_fields import register_fields
    #     from core.utilities.database import SessionLocal

    #     db = SessionLocal()
        
    #     register_all_models(db)
    #     register_fields(db)

    # except Exception as e:
    #     print(e)
