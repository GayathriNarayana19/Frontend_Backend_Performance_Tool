#File to sort SPE-LDST CSV DATA to analyse based on columns pc and latency

import sys
import pandas as pd

def count_and_sort_csv(input_file):
    df = pd.read_csv(input_file)
    pc_counts = df['pc'].value_counts()

    counts_df = pd.DataFrame({'pc': pc_counts.index, 'frequency': pc_counts.values})

    merged_df = pd.merge(df, counts_df, on='pc')

    sorted_df = merged_df.sort_values(by='frequency', ascending=False)

    sorted_df = sorted_df.drop(columns=['frequency'])

    sorted_file_freq_pc = 'sorted_file_freq_pc.csv'
    sorted_df.to_csv(sorted_file_freq_pc, index=False)

    grouped_df = merged_df.groupby('pc').agg({'total_lat': 'sum', 'frequency': 'first'}).reset_index()

    sorted_df_by_frequency = grouped_df.sort_values(by='frequency', ascending=False)

    total_latency = 'total_latency.csv'
    sorted_df_by_frequency.to_csv(total_latency, index=False)

    sorted_df_by_latency = sorted_df_by_frequency.sort_values(by='total_lat', ascending=False)

    sorted_file_by_latency = 'sorted_file_by_latency.csv'
    sorted_df_by_latency[['pc', 'frequency', 'total_lat']].to_csv(sorted_file_by_latency, index=False)

    print(f"Files saved:\n- {sorted_file_freq_pc}\n- {total_latency}\n- {sorted_file_by_latency}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    count_and_sort_csv(input_file)
