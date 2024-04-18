import json
import sys
from datetime import datetime

def parse_value(data):
    key, value_dict = next(iter(data.items()))
    value_type, value = next(iter(value_dict.items()))
    
    if value_type.strip() == "N":
        return parse_number(value)
    elif value_type.strip() == "S":
        return parse_string(value)
    elif value_type.strip() == "BOOL":
        return parse_boolean(value)
    elif value_type.strip() == "NULL":
        return parse_null(value)
    elif value_type.strip() == "L":
        return parse_list(value)
    elif value_type.strip() == "M":
        return parse_map(value)
    return None

def parse_number(value):
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return None

def parse_string(value):
    value = value.strip()
    try:
        return int(datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').timestamp())
    except ValueError:
        return value if value else None

def parse_boolean(value):
    true_values = {"1", "t", "T", "TRUE", "true", "True"}
    false_values = {"0", "f", "F", "FALSE", "false", "False"}
    value = value.strip()
    if value in true_values:
        return True
    elif value in false_values:
        return False
    return None

def parse_null(value):
    true_values = {"1", "t", "T", "TRUE", "true", "True"}
    value = value.strip()
    return None if value in true_values else False

def parse_list(value):
    if not isinstance(value, list):
        return None
    result = []
    for item in value:
        parsed_item = parse_value(item)
        if parsed_item is not None:
            result.append(parsed_item)
    return result if result else None

def parse_map(value):
    if not isinstance(value, dict):
        return None
    result = {}
    for key, val in value.items():
        parsed_val = parse_value({key: val})
        if parsed_val is not None:
            result[key] = parsed_val
    return result if result else None

def transform_json(input_json):
    transformed_data = parse_map(input_json)
    print(json.dumps(transformed_data, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transform_json.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    with open(input_file, 'r') as file:
        input_json = json.load(file)
        transform_json(input_json)
