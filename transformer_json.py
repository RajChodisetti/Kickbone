  import json
  import sys
  from datetime import datetime


  def parse_number(value):
    """Converts string to a float or int, removing leading zeros."""
    try:
      if '.' in value:
        return float(value)
      return int(value.lstrip('0'))
    except ValueError:
      return None


  def parse_string(value):
    """Trims whitespace and converts RFC3339 timestamps to Unix epoch."""
    value = value.strip()
    if value == "":
      return None
    try:
      return int(datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').timestamp())
    except ValueError:
      return value


  def parse_boolean(value):
    """Standardizes boolean values."""
    truthy = {"1", "t", "T", "TRUE", "true", "True"}
    falsey = {"0", "f", "F", "FALSE", "false", "False"}
    value = value.strip()
    if value in truthy:
      return True
    elif value in falsey:
      return False
    return None


  def parse_null(value):
    """Converts specific strings to None, ignoring invalid values."""
    value = value.strip().lower()
    return None if value == "true" else False


  def parse_list(items):
    """Processes list items based on their data types, ignoring invalid entries."""
    result = []
    for item in items:
      if isinstance(item, dict):
        for key, val in item.items():
          if key.strip() in value_parsers:
            parsed = value_parsers[key.strip()](val)
            if parsed is not None:
              result.append(parsed)
    return result


  def parse_map(value_map):
    """Recursively processes map items, handling nested structures."""
    result = {}
    for key, val in value_map.items():
      key = key.strip()
      if key and val:
        for type_key, content in val.items():
          type_key = type_key.strip()
          if type_key in value_parsers:
            parsed = value_parsers[type_key](content)
            if parsed is not None:
              result[key] = parsed
    return result


  value_parsers = {
      'N': parse_number,
      'S': parse_string,
      'BOOL': parse_boolean,
      'NULL': parse_null,
      'L': parse_list,
      'M': parse_map
  }


  def transform_json(input_json):
    """Main function to handle JSON transformation."""
    transformed_data = parse_map(input_json)
    return transformed_data


  if __name__ == "  main  ":
    if len(sys.argv) != 2:
      print("Usage: python transform_json.py <input_file>")
      sys.exit(1)
    input_file = sys.argv[1]
    with open(input_file, "r") as f:
      input_json = json.load(f)
      transform_json(input_json)
