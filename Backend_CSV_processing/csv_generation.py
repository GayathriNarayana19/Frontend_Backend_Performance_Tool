#DESCRIPTION: Extract data from log files and append to csv
import os
import csv
import re
import sys

if len(sys.argv) != 3:
    print("Usage: python3 csv_generation.py <directory_path_where_txt_files_are_present> <output_file_name.csv>")
    sys.exit(1)

directory = sys.argv[1]
csv_filename = sys.argv[2]
if not os.path.isdir(directory):
    print("Error: Invalid directory path.")
    sys.exit(1)

core_data = {}
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        for row in file:
            # Split the row into values
            values = row.strip().split(',')
            
            # Check if the row contains valid data
            if len(values) >= 6:
                core = values[0]
                event_name = values[3]
                event_value = float(values[1])  # Use the 2nd value (index 1) for event_value
                
                # Check if the core entry is present in the dictionary
                if core not in core_data:
                    core_data[core] = {}
                
                if filename not in core_data[core]:
                    core_data[core][filename] = {}
                core_data[core][filename][event_name] = event_value

# List to store data for creating csv
data = []

for core, filenames in core_data.items():
    for filename, values in filenames.items():
        if len(values) >= 2:  # Ensure both combinations exist
            event_names = list(values.keys())
            event_1_name, event_2_name = event_names[0], event_names[1]
            event_1 = values[event_1_name]
            event_2 = values[event_2_name]
            xlabel = f"{filename}={event_1_name}/{event_2_name}"
            if event_2 != 0:
                division_result = event_1 / event_2
            else:
                division_result = "NAN"
            data.append((core, filename, event_1_name, event_1, event_2_name, event_2, division_result, xlabel))

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Core','Metrics', 'Name_1', 'Event_1', 'Name_2', 'Event_2', 'Event_1/Event_2', 'Graph_Xlabel'])
    csv_writer.writerows(data)
print(f'CSV file "{csv_filename}" created successfully!')

