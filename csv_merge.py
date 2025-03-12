import pandas as pd
import glob

# List of CSV files to merge
csv_files = glob.glob("apt_data_500_batch*.csv")

# Read and concatenate all CSV files
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("merged_apt_data.csv", index=False)

print("CSV files merged successfully into 'merged_apt_data.csv'")