import os

def validate_file_exists(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    return True

def validate_csv_structure(data):
    if not data:
        return False
    if not isinstance(data, list):
        return False
    if not isinstance(data[0], dict):
        return False
    return True

def format_number(num, decimals=2):
    return round(num, decimals)