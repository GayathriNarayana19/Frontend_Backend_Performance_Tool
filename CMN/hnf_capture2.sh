#!/bin/bash
# invoke perf to measure CMN PMU
# ensure arm_cmn.ko is loaded
# probably run this as root
# example:
#    ./measure-hnf.sh

#if [ "$#" -ne 4 ]; then                                                                                    
#        echo "Usage: $0 <output_directory> <testcase_name> <core_context> <cores>"                         
#        exit 1
#fi
        
#output_directory="$1"                                                                                      
#testcase_name="$2"
#core_context="$3"
#worker_cores="$4"

HOSTNAME=$(hostname)
# force HNF NodeID mapping based on hostname
if [[ $HOSTNAME == *altra* ]]; then
# Altra
HNF_NODES='{0x01e5,0x01e4,0x01dd,0x01dc,0x01d5,0x01d4,0x01cd,0x01cc,0x0165,0x0164,0x015d,0x015c,0x0155,0x0154,0x014d,0x014c,0x00a5,0x00a4,0x009d,0x009c,0x0095,0x0094,0x008d,0x008c,0x0025,0x0024,0x001d,0x001c,0x0015,0x0014,0x000d,0x000c}'
fi

# Add the events you want to measure in this array
events_to_measure=("sf_hit" "mc_reqs" "brd_snoops_sent" "cache_fill" "cache_miss" "cmp_adq_full" "dir_snoops_sent" "intv_dirty" "ld_st_swp_adq_full" "mc_retries" "pocq_addrhaz" "pocq_atomic_addrhaz" "pocq_reqs_recvd" "pocq_retry" "qos_hh_retry" "qos_pocq_occupancy_all" "qos_pocq_occupancy_atomic" "qos_pocq_occupancy_read" "qos_pocq_occupancy_stash" "qos_pocq_occupancy_write" "seq_full" "seq_hit" "sf_evictions" "sfbi_brd_snp_sent" "sfbi_dir_snp_sent" "slc_eviction" "slc_fill_invalid_way" "slc_sf_cache_access" "snp_fwded" "snp_sent" "snp_sent_untrk" "stash_data_pull" "stash_snp_sent" "txdat_stall" "txrsp_stall")

# Specify the sleep time (e.g., 5 seconds)
sleep_time=5

for a in "${events_to_measure[@]}"; do
    HNF_EVENTS=""
    HNF_EVENTS+=$(eval "echo '-e 'arm_cmn/hnf_$a,nodeid=$HNF_NODES,bynodeid=1/")
    HNF_EVENTS+=" "

    # Create a unique output file for each event
    output_file="$a.txt"

    # Run perf with the specified events and write the output to the corresponding file
    #sudo perf stat -I 1000 -a $HNF_EVENTS > "$output_file" &
    #sudo perf stat -I 1000 -a $HNF_EVENTS > "$output_file" 2>&1 &
    #sudo perf stat -a $HNF_EVENTS -x "," sleep "$sleep_sec"
    perf stat -a $HNF_EVENTS -x "," sleep "$sleep_time" > "$output_file" 2>&1
    #sudo perf stat -a $HNF_EVENTS sleep "$sleep_time" > "$output_file" 2>&1
    # Sleep for the desired duration
    #sleep $sleep_time
    perf_pid=$!
    # Terminate the perf process
    #sudo kill -INT $perf_pid
done



