import pandas as pd
import json
import xml.etree.ElementTree as ET

def load_data(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)

    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return pd.DataFrame(json.load(f))

    elif file_path.endswith(".xml"):
        tree = ET.parse(file_path)
        root = tree.getroot()
        rows = []

        for item in root:
            rows.append({child.tag: child.text for child in item})

        return pd.DataFrame(rows)

    else:
        raise ValueError("Unsupported file format")
