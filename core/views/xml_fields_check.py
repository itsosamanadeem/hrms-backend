import xml.etree.ElementTree as ET

def xml_fields(xml_view):
    root = ET.fromstring(xml_view)

    xml_fields = set()
    for field_tag in root.findall(".//field"):
        name = field_tag.get("name")
        if name:
            xml_fields.add(name)
    IGNORE_FIELDS = {"name", "model", "arch"}
    xml_fields = xml_fields - IGNORE_FIELDS

    return xml_fields
