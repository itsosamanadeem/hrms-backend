from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from addons.base.model.ir_hr_model import IrHrModel
from addons.base.model.ir_hr_fields import IrHrField
from .get_all_models import get_all_models

def register_fields(db: Session):
    try:
        all_models = get_all_models()

        for model in all_models:

            # Skip unmapped models
            try:
                mapper = inspect(model)
            except Exception:
                print(f"Skipping unmapped class: {model.__name__}")
                continue

            # Get actual SQL table name
            table_name = mapper.local_table.name

            # Find model entry in ir_hr_model
            db_model = db.query(IrHrModel).filter_by(name=table_name).first()
            if not db_model:
                print(f"Model not found in ir_hr_model: {table_name}")
                continue

            # Loop columns safely
            for column in mapper.columns:

                field_name = column.name

                # Skip if already registered
                exists = db.query(IrHrField).filter_by(
                    model_id=db_model.id, name=field_name
                ).first()
                if exists:
                    continue

                # Get field type
                field_type = column.type.__class__.__name__.lower()

                # Get relation (safe)
                try:
                    relation = (
                        next(iter(column.foreign_keys)).column.table.name
                        if column.foreign_keys
                        else None
                    )
                except Exception:
                    relation = None

                # Create new field
                new_field = IrHrField(
                    model_id=db_model.id,
                    name=field_name,
                    field_type=field_type,
                    string=field_name.replace("_", " ").title(),
                    required=not column.nullable,
                    readonly=False,
                    relation=relation,
                    help=""
                )

                db.add(new_field)

        db.commit()
        print("Fields registered safely.")

    except Exception as e:
        db.rollback()
        print("Fatal error in register_fields:", e)
