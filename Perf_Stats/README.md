# Neoverse N2/V2 PMU Collection & Analysis

## Perf Collection

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

```bash
python3 csv_generation.py ./perf_data/output_dir test1.csv
```

## CSV Splitting (multiple cores)

```bash
python3 csv_split.py -csv test1.csv -dir_name_for_csvs /home/ubuntu/split-csvs-test1
```

## Plotting 

Go to https://github.com/GayathriNarayana19/Performance_Analysis_Backend/tree/main/Perf_Stats_Backend repo to execute the below for rendering plots. 

```bash
python3 plotting_perf_stat_v2.py \
  --csv /path/to/scenario1.csv /path/to/scenario2.csv \
  -o /home/ubuntu/output_plots \
  -s 4K-baseline 64k_llc_stash_disable \
  -c "4K vs 64K cases Comparison"
```
