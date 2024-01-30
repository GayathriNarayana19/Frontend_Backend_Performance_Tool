#DESCRIPTION: Extract data from log files and append to csv
import os
import csv
import re
import sys
if len(sys.argv) != 3:
    print("Usage: python3 csv_gen.py <directory_path_where_txt_files_are_present> <output_file_name.csv>")
    sys.exit(1)


directory = sys.argv[1]
csv_filename = sys.argv[2]
if not os.path.isdir(directory):
    print("Error: Invalid directory path.")
    sys.exit(1)
# List to store data for creating csv
data = []
# Iterating through the files in the directory specified by user in cmdline
for filename in os.listdir(directory):
        core_data = {}
#    if filename.endswith('.txt'):
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
                    
                    # Store the event value for the specific event type
                    core_data[core].setdefault(event_name, []).append(event_value)
                    #print(core_data)
                    #print(core)
        
        # Extract the event names in accordance with the cores which are dynamic according to the user input. 
        event_names = list(set(event_name for events in core_data.values() for event_name in events.keys()))
        
        # Iterate by core  and perform Event_1/Event_2 
        for core in core_data.keys():
            for i in range(len(event_names)):
                for j in range(i + 1, len(event_names)):
                    Event_1_name = event_names[i]
                    Event_2_name = event_names[j]
                    Event_1 = core_data[core][Event_1_name][0] 
                    Event_2 = core_data[core][Event_2_name][0] 
                    if Event_1_name in core_data[core] and Event_2_name in core_data[core]:
                        if core_data[core][Event_2_name][0] != 0:
                            result = core_data[core][Event_1_name][0] / core_data[core][Event_2_name][0]
                        else:
                            result = "NAN"
                    else:
                        print(f"Not enough data for division with {core}, {Event_1}, or {Event_2}")
                    
                    filename_without_extension = os.path.splitext(filename)[0]
                    graph_xlabel = f"{filename_without_extension} = {Event_1_name}/{Event_2_name}"
                    data.append([core,filename_without_extension, Event_1_name, Event_1, Event_2_name, Event_2, result, graph_xlabel])
                    
    # Write data to CSV file
#print(data)

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Core','Metrics', 'Name_1', 'Event_1', 'Name_2', 'Event_2', 'Event_1/Event_2', 'Graph_Xlabel'])
    csv_writer.writerows(data)
print(f'CSV file "{csv_filename}" created successfully!')
