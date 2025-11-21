# # from core.database import Base, engine, SessionLocal
# # from core.base.models.ir_hr_model import IrHrModel
# # from .initialize_db import RegisterNewModel as RNM

# def initialize_database():
#     pass
#     """Create tables and insert base models if running for the first time."""
#     # Base.metadata.create_all(bind=engine)
#     # db = SessionLocal()
#     # try:
#     #     # check if already initialized
#     #     existing = db.query(IrHrModel).count()
#     #     if existing > 0:
#     #         print("✅ Database already initialized. Skipping bootstrap.")
#     #         return

#     #     # Insert base models
#     #     base_models = [
#     #         IrHrModel(name="ir_hr_model", model="ir_hr_model", description="Base model registry"),
#     #         IrHrModel(name="ir_hr_view", model="ir_hr_view", description="UI View definitions"),
#     #         IrHrModel(name="ir_hr_menu", model="ir_hr_menu", description="System Menus"),
#     #         IrHrModel(name="ir_hr_report", model="ir_hr_report", description="Report templates"),
#     #     ]

#     #     db.add_all(base_models)

#     #     db.commit()
#     #     print("🎉 Base HRMS core models initialized successfully.")

#     # except Exception as e:
#     #     print(f"❌ Error initializing database: {e}")
#     #     db.rollback()
#     # finally:
#     #     db.close()
