#CRIPTION: Extract data from log files and append to csv
import os
import csv
import re
import sys
# Directory containing the output log files in .txt format
#directory = '/home/ubuntu/LOGS_ampere_capture'
if len(sys.argv) != 3:
    print("Usage: python3 csv_gen.py <directory_path_where_txt_files_are_present> <output_file_name.csv>")
    sys.exit(1)
directory = sys.argv[1]
csv_filename = sys.argv[2]
if not os.path.isdir(directory):
    print("Error: Invalid directory path.")
    sys.exit(1)
# List to store data
data = []
# Iterating through the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            if len(lines) >= 4:
                Event_1 = float(lines[2].split(',')[1])
                Event_2 = float(lines[3].split(',')[1])
                Event_1_name = lines[2].split(',')[3]
                Event_2_name = lines[3].split(',')[3]
                #for srs process ID. Not reqd.
               # Event_1 = float(lines[2].split(',')[0])
               # Event_2 = float(lines[3].split(',')[0])
               # Event_1_name = lines[2].split(',')[2]
               # Event_2_name = lines[3].split(',')[2]
                if Event_2==0:
                    Event_1_div_2="NAN"
                else:
                    Event_1_div_2=Event_1/Event_2
                filename_without_extension = os.path.splitext(filename)[0]
                graph_xlabel = f"{filename_without_extension} = {Event_1_name}/{Event_2_name}"
                data.append([filename_without_extension, Event_1_name, Event_1, Event_2_name, Event_2, Event_1_div_2, graph_xlabel])
                
# Write data to CSV file
print(data)

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Metrics', 'Name_1', 'Event_1', 'Name_2', 'Event_2', 'Event_1/Event_2', 'Graph_Xlabel'])
    csv_writer.writerows(data)
print(f'CSV file "{csv_filename}" created successfully!')

