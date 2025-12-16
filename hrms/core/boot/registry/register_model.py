from sqlalchemy import inspect
from hrms.addons.base.model.ir_hr_model import IrHrModel

class RegisterModel:

    def register_model_in_model(self, db, model_class):
        inspector = inspect(db.bind)

        if not inspector.has_table("ir_hr_model", schema="public"):
            print("ir_hr_model table missing")
            return

        table_name = getattr(model_class, "__tablename__", None)
        if not table_name:
            return

        exists = db.query(IrHrModel).filter(IrHrModel.name == table_name).first()
        if exists:
            return 

        new_entry = IrHrModel(
            name=table_name,
            description=f"Model for table {table_name}",
            category="default"
        )
        db.add(new_entry)
        db.commit()

        print(f"Registered: {table_name}")
