import csv
import os
import sys

def separate_csv(csv_file, output_dir='separate_csv_files'):
    test_data = {}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            test_type = row['Core']
            # Check if the test type already exists in the dictionary
            if test_type not in test_data:
                test_data[test_type] = []
            test_data[test_type].append(row)

    os.makedirs(output_dir, exist_ok=True)

    # Write each set of rows to a separate CSV file
    for test_type, rows in test_data.items():
        output_file = os.path.join(output_dir, f'{test_type}.csv')
        fieldnames = [field for field in reader.fieldnames if field != 'Core']
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows({k: v for k, v in row.items() if k != 'Core'} for row in rows)

    print("Separate CSV files generated successfully.")

if __name__ == "__main__":
    # Check if the '-csv' flag and the CSV file path are provided as arguments
    if '-csv' not in sys.argv or '-dir_name_for_csvs' not in sys.argv:
        print("Usage: python3 csv_split.py -csv <csv_file> -dir_name_for_csvs <output_directory>")
        sys.exit(1)

    csv_flag_index = sys.argv.index('-csv')
    csv_file = sys.argv[csv_flag_index + 1] if len(sys.argv) > csv_flag_index + 1 else None

    dir_flag_index = sys.argv.index('-dir_name_for_csvs')
    output_dir = sys.argv[dir_flag_index + 1] if len(sys.argv) > dir_flag_index + 1 else None

    if csv_file is None or output_dir is None:
        print("Please provide both the CSV file path and the output directory.")
        sys.exit(1)

    separate_csv(csv_file, output_dir)

