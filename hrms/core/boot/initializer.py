def initialize_system():

    from hrms.core.utilities.database import SessionLocal
    from hrms.core.boot.loaders.module_loader import register_all_models
    from hrms.core.boot.registry.register_fields import register_fields
    from hrms.core.boot.seed import seed_super_user
    from sqlalchemy import inspect
    from hrms.core.views.view_loader_utility import view
    
    db = SessionLocal()
    inspector = inspect(db.bind)
    
    try:
        if inspector.has_table("ir_hr_model"):
            register_all_models(db)
            register_fields(db)
            view(db)

            seed_super_user(db)
    finally:
        db.close()