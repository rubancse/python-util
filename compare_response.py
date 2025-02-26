import xml.etree.ElementTree as ET
import json

def consolidate_xml_json(xml_response, json_response, matching_field="ipaddress"):
    """
    Consolidates XML and JSON API responses based on a matching field (default: ipaddress).

    Args:
        xml_response: The XML API response as a string.
        json_response: The JSON API response as a string.
        matching_field: The field to use for matching (default: "ipaddress").

    Returns:
        A list of dictionaries, where each dictionary represents a consolidated entry.
        Returns an empty list if there are errors.
    """

    try:
        # Parse XML
        root = ET.fromstring(xml_response)
        xml_data = []
        for element in root:  # Iterate through the elements under the root
            item = {}
            for child in element:
                item[child.tag] = child.text
            xml_data.append(item)

        # Parse JSON
        json_data = json.loads(json_response)
        if isinstance(json_data, dict) and "data" in json_data: # If the json has a "data" key
            json_data = json_data["data"]
        elif not isinstance(json_data, list):
            raise ValueError("JSON data must be a list of dictionaries or contain a 'data' key with a list.")

        consolidated_data = []

        # Consolidation logic (similar to previous example, but handles XML)
        for xml_item in xml_data:
            match_found = False
            for json_item in json_data:
                if xml_item.get(matching_field) == json_item.get(matching_field):
                    match_found = True
                    consolidated_item = xml_item.copy()
                    consolidated_item.update(json_item)  # Merge JSON data
                    consolidated_data.append(consolidated_item)
                    break
            if not match_found:
                consolidated_data.append(xml_item)

        for json_item in json_data:
            match_found = False
            for xml_item in xml_data:
                if xml_item.get(matching_field) == json_item.get(matching_field):
                    match_found = True
                    break
            if not match_found:
                consolidated_data.append(json_item)
        return consolidated_data

    except (ET.ParseError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Error processing responses: {e}")
        return []


# Sample XML and JSON responses (replace with your actual data)
xml_response = """
<data>
    <item>
        <ipaddress>192.168.1.1</ipaddress>
        <name>Server A</name>
        <os>Linux</os>
    </item>
    <item>
        <ipaddress>10.0.0.1</ipaddress>
        <name>Workstation B</name>
        <os>Windows</os>
    </item>
</data>
"""

json_response = """
{
    "data": [
        {"ipaddress": "192.168.1.1", "location": "NYC", "vendor": "Dell"},
        {"ipaddress": "172.16.0.1", "location": "LA", "vendor": "HP"},
        {"ipaddress": "10.0.0.1", "location": "London", "vendor": "Lenovo"}
    ]
}
"""

consolidated_result = consolidate_xml_json(xml_response, json_response)
print(json.dumps(consolidated_result, indent=2))


#Example with JSON without "data" key
json_response2 = """
[
        {"ipaddress": "192.168.1.1", "location": "NYC", "vendor": "Dell"},
        {"ipaddress": "172.16.0.1", "location": "LA", "vendor": "HP"},
        {"ipaddress": "10.0.0.1", "location": "London", "vendor": "Lenovo"}
]
"""
consolidated_result2 = consolidate_xml_json(xml_response, json_response2)
print(json.dumps(consolidated_result2, indent=2))
