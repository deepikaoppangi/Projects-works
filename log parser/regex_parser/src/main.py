import os
from utils import read_log_file, write_json_file
from parser import parse_logs

def main():
    log_file = input("Enter path to log file (e.g., data/mock_logs.txt): ")
    output_file = r"C:\Users\deepi\Downloads\HCL_work\log_parser\regex_parser\data\output.json"
    
    try:
        log_lines = read_log_file(log_file)
        parsed_logs = parse_logs(log_lines)
        write_json_file(parsed_logs, output_file)
        print(f"Parsed logs written to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
