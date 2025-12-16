from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
from .view_details import detect_model_name, detect_view_id, detect_view_name, detect_view_type
import os
from hrms.core.views.record_view import RecordView
from hrms.core.utilities.discover_manifest import discover_manifests
from pathlib import Path
from hrms.core.boot.utils.addons_scanner import scan_addons

def view(db: Session):
    """Load XML views from addons and save to DB."""

    modules, addons_dir = scan_addons()
    # Process views
    for module_name, module_data in modules.items():
        views = module_data.get('manifest', {}).get("data", {}).get("views", [])
        for view_file in views:
            view_file_path = addons_dir / module_name / view_file
            print(f"Processing view file: {view_file_path}")
            if not view_file_path.exists():
                print(f"View file does not exist: {view_file_path}")
                continue

            tree = ET.parse(view_file_path)
            root = tree.getroot()
            view_id = detect_view_id(root)
            view_name = detect_view_name(root)
            view_type = detect_view_type(root)
            model_name = detect_model_name(root)
            xml_view = ET.tostring(root, encoding='unicode')
            try:

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

        print(f"Registered views for module: {module_name}")
