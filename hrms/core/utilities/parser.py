ALLOWED_ATTRS = {
    "name",
    "string",
    "action",
    "class",
    "style",
    "domain",
    "widget",
    "invisible",
    "readonly",
    "required",
    "colspan",
}
BOOLEAN_ATTRS = {"invisible", "readonly", "required"}

import xml.etree.ElementTree as ET


class XMLViewParser:
    def parse(self, xml_string: str) -> dict:
        """
        Entry point: full XML (record-based)
        """
        root = ET.fromstring(xml_string)

        arch_field = root.find(".//field[@name='arch']")
        if arch_field is None:
            raise ValueError("No <field name='arch'> found")

        # arch must contain exactly one root view tag
        for child in arch_field:
            return self._parse_node(child)

        raise ValueError("Empty arch field")

    def _parse_node(self, node: ET.Element) -> dict:
        """
        Recursive XML → JSON node
        """
        json_node = {
            "type": node.tag,
            "props": self._parse_attributes(node),
        }

        children = []
        for child in node:
            children.append(self._parse_node(child))

        if children:
            json_node["children"] = children

        return json_node

    def _parse_attributes(self, node: ET.Element) -> dict:
        props = {}

        for key, value in node.attrib.items():
            if key not in ALLOWED_ATTRS:
                continue

            if key in BOOLEAN_ATTRS:
                value = value in ("1", "true", "True")

            props[key] = value

        return props
