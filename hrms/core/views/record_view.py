from sqlalchemy.orm import Session
from sqlalchemy import inspect
from hrms.addons.base.model.ir_hr_view import IrHrView
from hrms.addons.base.model.ir_hr_model import IrHrModel
import json
from .get_all_relationships import get_all_relationships
# from .xml_fields_check import xml_fields
from hrms.core.utilities.parser import XMLViewParser
import xml.etree.ElementTree as ET
class RecordView:

    def __init__(self):
        # self.xml_fields =  xml_fields
        self.inspector = None

    def get_columns(self,db,model):
        self.inspector = inspect(db.bind)
        columns = self.inspector.get_columns(model)
        return [col["name"] for col in columns]

    # def get_tables_relationships(self, model):
    #     orm_inspector = inspect(model)
    #     return {
    #         rel.key: rel.mapper.class_
    #         for rel in orm_inspector.relationships
    #     }
    
    def validate_xml_fields(self, xml_node, model_class):
        orm_inspector = inspect(model_class)

        columns = {c.key for c in orm_inspector.columns}
        relationships = {
            rel.key: rel.mapper.class_
            for rel in orm_inspector.relationships
        }

        valid_fields = columns | relationships.keys()

        for field in xml_node.findall("field"):
            field_name = field.get("name")

            if not field_name:
                continue

            if field_name not in valid_fields:
                raise ValueError(
                    f"Invalid field '{field_name}' for model '{model_class.__name__}'"
                )

            if field_name in relationships:
                related_model = relationships[field_name]

                for child in field:
                    self.validate_xml_fields(child, related_model)

    def save_view_to_db(self,db: Session, view_id, view_name, view_type, model_name, xml_view):
        try:
            print("Validating view before saving...")

            all_models = get_all_relationships()

            ModelClass = all_models.get(model_name)
            if not ModelClass:
                raise ValueError(f"Model class for '{model_name}' not found.")

            model = db.query(IrHrModel).filter(IrHrModel.name == model_name).first()
            
            # model_columns = self.get_columns(db,model_name)
            # print(model_columns)
            # relation_ships = self.get_tables_relationships(ModelClass)
            # print(relation_ships)

            if not model:
                raise ValueError(f"Model {model_name} not found in ir_hr_model table")

            root = ET.fromstring(xml_view)

            self.validate_xml_fields(root, ModelClass)

            print("XML fields validated successfully.")

            # xml_fields = self.xml_fields(xml_view)
            # model_fields = set(model_columns + relation_ships)
            # invalid_fields = set(xml_fields) - model_fields

            # if invalid_fields:
            #     raise ValueError(
            #         f"Invalid fields detected in view '{view_name}': {invalid_fields}\n"
            #         f"ℹ Valid fields for '{model_name}' are: {model_columns}"
            #     )

            print("XML fields validated successfully.")

            parser = XMLViewParser()
            parsed_view = parser.parse(xml_view)

            existing = db.query(IrHrView).filter(IrHrView.view_id == view_id).first()

            if existing:
                print(f"Updating existing view: {view_id}")
                existing.name = view_name
                existing.view_type = view_type
                existing.xml_data = xml_view
                existing.json_data = parsed_view
            else:
                print(f"Creating new view: {view_id}")
                new_view = IrHrView(
                    view_id=view_id,
                    name=view_name,
                    view_type=view_type,
                    model_id=model.id,
                    xml_data=xml_view,
                    json_data=parsed_view
                )
                db.add(new_view)

            db.commit()
            print(f"View '{view_name}' saved successfully!")
        except Exception as e:
            db.rollback()
            print(e)
