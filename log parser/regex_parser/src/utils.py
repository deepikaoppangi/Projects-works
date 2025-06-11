import os

def read_log_file(file_path):
    """Read log file and return lines."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file {file_path} not found")
    with open(file_path, 'r') as f:
        return f.readlines()

def write_json_file(data, output_path):
    """Write data to JSON file."""
    import json
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
