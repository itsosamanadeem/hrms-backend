from sqlalchemy import inspect
from hrms.addons.base.model.ir_hr_model import IrHrModel
from hrms.core.boot.utils.get_module_name import get_module_name

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

        module_name = get_module_name(model_class=model_class)
        
        new_entry = IrHrModel(
            name=table_name,
            description=f"Model for table {table_name}",
            category="default",
            module_name=module_name
        )
        db.add(new_entry)
        db.commit()

        print(f"Registered: {table_name}")
