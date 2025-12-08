import xml.etree.ElementTree as ET

def detect_view_id(xml_root):
    """Detects view ID from <record id='id'> tag."""
    for rec in xml_root.findall('record'):
        view_id = rec.get('id')
        if view_id:
            return view_id
    return "unknown"

def detect_view_name(xml_root):
    """Detects view name from <field name='name'> tag."""
    for rec in xml_root.findall('record'):
        name_field = rec.find(".//field[@name='name']")
        if name_field is not None:
            return name_field.text
    return "unknown"

def detect_view_type(xml_root):
    """Detects view type like form, tree, kanban, etc. from <field name='arch'> tag."""
    for rec in xml_root.findall('record'):
        view_type = rec.find(".//field[@name='arch']")
        if view_type is not None and len(view_type):
            for attr in view_type:
                return attr.tag.lower()
        else:
            return "unknown"

def detect_model_name(xml_root):
    """Detects model name from <field name='model'> tag."""
    for rec in xml_root.findall('record'):
        model_field = rec.find(".//field[@name='model']")
        if model_field is not None:
            return model_field.text
    return "unknown"

def detect_xml_root(xml_string):
    """Parses XML string and returns the root element."""
    try:
        xml_str = ET.tostring(xml_string, encoding='unicode')
        return xml_str
    except ET.ParseError:
        return None