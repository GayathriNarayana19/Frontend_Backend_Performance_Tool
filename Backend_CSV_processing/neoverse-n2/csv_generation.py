import os
import csv
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
            if row.startswith("#") or not row.strip():
                continue  

            values = row.strip().split(',')

            try:
                if len(values) >= 6 and values[0].startswith("CPU"):
                    # Core-based format
                    core = values[0].strip()
                    event_value = float(values[1].strip())
                    event_name = values[3].strip().split()[0]  # core mode

                elif len(values) >= 4 and values[1].strip() == "":
                    # PID-based format
                    core = f"pid:{filename}"
                    event_value = float(values[0].strip())
                    event_name = values[2].strip()  # pid mode

                else:
                    continue  

                # Build data structure
                if core not in core_data:
                    core_data[core] = {}
                if filename not in core_data[core]:
                    core_data[core][filename] = {}

                core_data[core][filename][event_name] = event_value

            except ValueError:
                continue  # Skip lines where float conversion fails
'''
#  Step 1: Read all log files and store data
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        for row in file:
            values = row.strip().split(',')

            if len(values) < 4:
                continue  # Skip malformed rows

            try:
                event_value = float(values[0].strip())
                event_name = values[2].strip()

                # Use core ID if available, else use pid-based marker
                core = values[1].strip() if values[1].strip() else f"pid:{filename}"

                if core not in core_data:
                    core_data[core] = {}
                if filename not in core_data[core]:
                    core_data[core][filename] = {}

                core_data[core][filename][event_name] = event_value
            except ValueError:
                continue  # Skip rows where event_value isn't a number

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        for row in file:
            values = row.strip().split(',')

            if len(values) >= 6:
                core = values[0]
                event_name = values[3].split()[0]  # Extract first word (event)
                event_value = float(values[1])  # Use second column as value

                if core not in core_data:
                    core_data[core] = {}

                if filename not in core_data[core]:
                    core_data[core][filename] = {}

                core_data[core][filename][event_name] = event_value
'''
#  Step 2: Process Data and Generate CSV
data = []

for core, filenames in core_data.items():
    for filename, values in filenames.items():
        if len(values) >= 2:  # Ensure at least two events exist
            event_names = list(values.keys())
            event_1_name, event_2_name = event_names[0], event_names[1]
            event_1 = values[event_1_name]
            event_2 = values[event_2_name]

            if filename == 'retiring':
                event_3_name, event_4_name = event_names[2], event_names[3]
                event_3 = values[event_3_name]  # OP_SPEC
                event_4 = values[event_4_name]  # STALL_SLOT

                #  Retiring Formula (N2)
                xlabel = f"{filename} = 100 * (({event_names[0]} / {event_names[2]}) * (1 - {event_names[3]} / ({event_names[1]} * 5)))"
                division_result = 100 * ((event_1 / event_3) * (1 - event_4 / (event_2 * 5)))

                data.append((core, filename, event_1_name, event_1, event_2_name, event_2, 
                             division_result, xlabel, event_3_name, event_3, event_4_name, event_4))

            elif filename == 'frontend_bound':
                event_3_name = event_names[2]
                event_3 = values[event_3_name]

                #  Frontend Bound Formula (N2)
                xlabel = f"{filename} = 100 * ({event_names[0]} / ({event_names[1]} * 5) - {event_names[2]} / {event_names[1]})"
                division_result = 100 * (event_1 / (event_2 * 5) - event_3 / event_2)

                data.append((core, filename, event_1_name, event_1, event_2_name, event_2, 
                             division_result, xlabel, event_3_name, event_3))

            elif filename == 'backend_bound':
                event_3_name = event_names[2]
                event_3 = values[event_3_name]

                #  Backend Bound Formula (N2)
                xlabel = f"{filename} = 100 * ({event_names[0]} / ({event_names[1]} * 5) - {event_names[2]} * 3 / {event_names[1]})"
                division_result = 100 * (event_1 / (event_2 * 5) - event_3 * 3 / event_2)

                data.append((core, filename, event_1_name, event_1, event_2_name, event_2, 
                             division_result, xlabel, event_3_name, event_3))

            elif filename == 'bad_speculation':
                event_3_name, event_4_name = event_names[2], event_names[3]
                event_3 = values[event_3_name]  # OP_SPEC
                event_4 = values[event_4_name]  # STALL_SLOT
                event_5_name = event_names[4]
                event_5 = values[event_5_name]  # BR_MIS_PRED

                # Bad Speculation Formula (N2)
                xlabel = f"{filename} = 100 * ((1 - {event_names[0]} / {event_names[2]}) * (1 - {event_names[3]} / ({event_names[1]} * 5)) + {event_names[4]} * 4 / {event_names[1]})"
                division_result = 100 * ((1 - event_1 / event_3) * (1 - event_4 / (event_2 * 5)) + event_5 * 4 / event_2)

                data.append((core, filename, event_1_name, event_1, event_2_name, event_2, 
                             division_result, xlabel, event_3_name, event_3, event_4_name, event_4, event_5_name, event_5))

            else:
                xlabel = f"{filename}={event_1_name}/{event_2_name}"
                division_result = event_1 / event_2 if event_2 != 0 else "NAN"
                data.append((core, filename, event_1_name, event_1, event_2_name, event_2, division_result, xlabel))

#  Step 3: Save Data to CSV
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Ensure all events are captured in CSV header
    csv_writer.writerow(['Core', 'Metrics', 'Name_1', 'Event_1', 'Name_2', 'Event_2', 'Event_1/Event_2', 
                         'Graph_Xlabel', 'Name_3', 'Event_3', 'Name_4', 'Event_4', 'Name_5', 'Event_5'])

    csv_writer.writerows(data)
print(f'CSV file "{csv_filename}" created successfully!')

