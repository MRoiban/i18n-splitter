import json
import sys
import argparse

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
            file.seek(0)
            return json.load(file), lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File '{file_path}' is not a valid JSON file. JSONDecodeError: {e}")
        sys.exit(1)

def find_key_line(key, lines):
    for i, line in enumerate(lines):
        if f'"{key}"' in line or f"'{key}'" in line:
            return i + 1
    return "(not found in the original lines)"

def compare_keys(json1, json2, lines1, lines2, write_missing=False, verbose=False):
    keys1 = set(json1.keys())
    keys2 = set(json2.keys())

    only_in_file1 = keys1 - keys2
    only_in_file2 = keys2 - keys1

    # Dictionary to hold missing key-value pairs from file1
    missing_in_file2 = {key: json1[key] for key in only_in_file1}

    # Display count of missing keys
    print(f"Number of keys only in the first JSON file: {len(only_in_file1)}")
    print(f"Number of keys only in the second JSON file: {len(only_in_file2)}")

    # Display keys and line numbers if verbose mode is enabled
    if verbose:
        if only_in_file1:
            print("\nKeys only in the first JSON file:")
            for key in only_in_file1:
                line_number = find_key_line(key, lines1)
                print(f"  - {key} (line {line_number})")

        if only_in_file2:
            print("\nKeys only in the second JSON file:")
            for key in only_in_file2:
                line_number = find_key_line(key, lines2)
                print(f"  - {key} (line {line_number})")

    # Write missing keys and values to "missing.json" if requested
    if write_missing and missing_in_file2:
        with open("missing.json", "w", encoding='utf-8') as outfile:
            json.dump(missing_in_file2, outfile, indent=4)
        print("\nMissing keys and values written to 'missing.json'.")

    # If no keys are missing
    if not only_in_file1 and not only_in_file2:
        print("\nBoth JSON files have identical keys.")

def main():
    parser = argparse.ArgumentParser(description="Compare keys between two JSON files.")
    parser.add_argument("file1", help="Path to the first JSON file")
    parser.add_argument("file2", help="Path to the second JSON file")
    parser.add_argument("--write-missing", action="store_true", help="Write missing keys from file1 to 'missing.json'")
    parser.add_argument("--verbose", action="store_true", help="Display detailed list of missing keys and their line numbers")
    args = parser.parse_args()

    json1, lines1 = load_json(args.file1)
    json2, lines2 = load_json(args.file2)

    compare_keys(json1, json2, lines1, lines2, write_missing=args.write_missing, verbose=args.verbose)

if __name__ == "__main__":
    main()
