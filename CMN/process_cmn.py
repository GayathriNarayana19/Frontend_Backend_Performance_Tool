#Author: @gayathrinarayana.yegnanarayanan@arm.com
#Description: For every CMN metric, this script helps to add up all the data from 32 nodes and generates a CSV for all 35 hnf metrics with total value calculated using calculate_sum function.

import os
import csv

# Calculate the sum of values in the first column of a file
def calculate_sum(file_path):
    total_sum = 0
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            try:
                value = int(values[0].strip())
                total_sum += value
            except ValueError:
                # Raise error messages for lines having non-numeric values in the first column
                if not line.strip().startswith(('sleep: Interrupt', './hnf_capture2.sh: line')):
                    print(f"Skipping line '{line.strip()}' in file '{file_path}' due to invalid value in the first column.")
    return total_sum

directory = input("Enter the directory containing the hnf text files: ")

output_filename = input("Enter the CSV filename to store the sums: ")

sums = []

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        total_sum = calculate_sum(file_path)
        filename_no_extension = os.path.splitext(filename)[0]
        # Append the filename and sum to the list
        sums.append((filename_no_extension, total_sum))

# Write to CSV 
output_file = output_filename + '.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename', 'Sum'])
    for row in sums:
        writer.writerow(row)

print(f"Sums have been written to '{output_file}'.")



