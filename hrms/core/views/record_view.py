from sqlalchemy.orm import Session
from sqlalchemy import inspect
from hrms.addons.base.model.ir_hr_view import IrHrView
from hrms.addons.base.model.ir_hr_model import IrHrModel
import json
from .get_all_relationships import get_all_relationships
from .xml_fields_check import xml_fields
class RecordView:

    def __init__(self):
        self.xml_fields =  xml_fields
        self.inspector = None

    def get_columns(self,db,model):
        self.inspector = inspect(db.bind)
        columns = self.inspector.get_columns(model)
        return [col["name"] for col in columns]

    def get_tables_relationships(self,model):
        orm_inspector = inspect(model)
        return list(orm_inspector.relationships.keys())

    def save_view_to_db(self,db: Session, view_id, view_name, view_type, model_name, xml_view):
        try:
            print("Validating view before saving...")

            all_models = get_all_relationships()

            ModelClass = all_models.get(model_name)
            if not ModelClass:
                raise ValueError(f"Model class for '{model_name}' not found.")

            model = db.query(IrHrModel).filter(IrHrModel.name == model_name).first()
            
            model_columns = self.get_columns(db,model_name)

            relation_ships = self.get_tables_relationships(ModelClass)

            if not model:
                raise ValueError(f"Model {model_name} not found in ir_hr_model table")

            xml_fields = self.xml_fields(xml_view)
            model_fields = set(model_columns + relation_ships)
            invalid_fields = set(xml_fields) - model_fields

            if invalid_fields:
                raise ValueError(
                    f"Invalid fields detected in view '{view_name}': {invalid_fields}\n"
                    f"ℹ Valid fields for '{model_name}' are: {model_columns}"
                )

            print("XML fields validated successfully.")

            view_json = json.dumps({
                "fields": list(xml_fields),
                "type": view_type,
                "model": model_name
            })

            existing = db.query(IrHrView).filter(IrHrView.view_id == view_id).first()

            if existing:
                print(f"Updating existing view: {view_id}")
                existing.name = view_name
                existing.view_type = view_type
                existing.xml_data = xml_view
                existing.json_data = view_json
            else:
                print(f"Creating new view: {view_id}")
                new_view = IrHrView(
                    view_id=view_id,
                    name=view_name,
                    view_type=view_type,
                    model_id=model.id,
                    xml_data=xml_view,
                    json_data=view_json
                )
                db.add(new_view)

            db.commit()
            print(f"View '{view_name}' saved successfully!")
        except Exception as e:
            db.rollback()
            print(e)
