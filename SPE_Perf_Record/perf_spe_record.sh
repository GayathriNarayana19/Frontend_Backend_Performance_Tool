#!/bin/bash
if [ "$#" -ne 4 ]; then
	echo "Usage: $0 <output_directory> <testcase_name> <core_context> <cores>"
	exit 1
fi

output_directory="$1"
testcase_name="$2"
core_context="$3"
worker_cores="$4"
if [ ! -d "$output_directory" ]; then
	mkdir -p "$output_directory"
fi
filename="$output_directory/${testcase_name}_${core_context}_${worker_cores}.data" 
perf record -e arm_spe/event_filter=2/ -o "$filename" -C $worker_cores --sample-cpu sleep 10 
