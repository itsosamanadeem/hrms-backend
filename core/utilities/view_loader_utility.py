from .database import Session
import xml.etree.ElementTree as ET
from .view_type import detect_model_name,detect_view_id,detect_view_name,detect_view_type,detect_xml_root
import os
from core.views.record_view import RecordView

def view(db: Session,module_name,manifest_data:str, module_path:str):
    """Placeholder for saving views to DB."""
    print(f"Registering views for module: {module_name}, {module_path}")

    views = manifest_data.get("data", {}).get("views", [])
    for view_file in views:
        view_file_path = os.path.join("addons", module_name, view_file)
        print(f"Processing view file: {view_file_path}")

        if not os.path.exists(view_file_path):
            print(f"View file does not exist: {view_file_path}")
            continue
        try:
            tree = ET.parse(view_file_path)
            root = tree.getroot()
            view_id = detect_view_id(root)
            view_name = detect_view_name(root)
            view_type = detect_view_type(root)
            print(f"view type {view_type}")
            model_name = detect_model_name(root)
            print(f"Model Name {model_name}")
            xml_view = ET.tostring(root, encoding='unicode')
            rv = RecordView()
            rv.save_view_to_db(
                db=db,
                view_id=view_id,
                view_name=view_name,
                view_type=view_type,
                model_name=model_name,
                xml_view=xml_view
            )

            
        except ET.ParseError as e:
            print(f"XML Parse Error in {view_file_path}: {e}")
            continue

