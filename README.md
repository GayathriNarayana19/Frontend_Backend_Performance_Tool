# Frontend_Backend_Performance_Tool
This performance tool is designed to monitor the performance of PMU events, SPE, CMN-hnf events and does post processing in the form of CSV generation to visualise the results better. 
## Features

- Perf Stats -
A key advantage of the arm_pmu_collection.sh script is its ability to execute on multiple cores in parallel, significantly reducing the execution time. For optimal performance in 5G/ Networking workloads, it is recommended to set a sleep interval between 5 to 10 seconds, depending on the workload and user preferences. Given that there are approximately 70 KPIs to monitor, setting the sleep interval to 10 seconds, for instance, results in a total runtime of 70 * 10 = 700 seconds, or about 12 minutes approximately.

## Perf Collection

**Script:** `Perf_Stats/neoverse-n2-v2/arm_pmu_collection.sh`

### Core-based
```bash
sudo ./arm_pmu_collection.sh /home/ubuntu/test_collect 15,16,17,18 3
```

### PID-based
```bash
sudo ./arm_pmu_collection.sh /home/ubuntu/test_collect pid:92921 2
```

**Arguments:** `<output_directory> <core(s)|pid> <sleep_seconds>`

## CSV Generation

**Script:** `Backend_CSV_processing/neoverse-v2/csv_generation.py`

```bash
python3 csv_generation.py ./perf_data/output_dir test1.csv
```

## CSV Splitting (multiple cores)

**Script:** `Backend_CSV_processing/neoverse-v2/csv_split.py`

```bash
python3 csv_split.py -csv test1.csv -dir_name_for_csvs /home/ubuntu/split-csvs-test1
```

## Plotting

**Repo:** [Performance_Analysis_Backend](https://github.com/GayathriNarayana19/Performance_Analysis_Backend/tree/main/Perf_Stats_Backend)

**Script:** `Perf_Stats_Backend/plotting_perf_stat_v2.py`

```bash
python3 plotting_perf_stat_v2.py \
  --csv /path/to/scenario1.csv /path/to/scenario2.csv \
  -o /home/ubuntu/output_plots \
  -s 4K-baseline 64k_llc_stash_disable \
  -c "4K vs 64K cases Comparison"
```

- CMN -
The CMN directory has hnf_capture2.sh and process_cmn.py which help in monitoring the N1 hnf-CMN events and post process the results. 

- Consolidates the data into one CSV which can be fed into Backend_plotting tool for analysis.

## Documentation

For detailed documentation, please refer to the following PDFs:

- Perf Stats & Backend_CSV_processing combined [Perf Stats Usage](Documentation-perf_stat.pdf)
- CMN [PDF 2: CMN Usage](Documentation-CMN-hnf.pdf)
- SPE Parser Post Processing - Sorting based on Latency & Program Counter [SPE_parser_sort_script-Usage](Documentation - SPE_parser_post_processing.docx)
- SPE_Perf_Record: Official Documentation - 
[PDF 3: SPE Usage](Documentation-SPE_tool_script_version.pdf) 


## Installation

```bash
git clone https://github.com/GayathriNarayana19/Frontend_Backend_Performance_Tool/
cd Frontend_Backend_Performance_Tool
```
## License
This project is licensed under the GNU General Public license v3.0 - see the LICENSE file for details.
