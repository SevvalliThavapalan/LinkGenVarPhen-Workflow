import pandas as pd
import glob
import os

def merge_mutation_files(folder_path, file_pattern="*.xlsx", output_path="merged_mutations.csv"):
    all_dfs = []

    # Collect all matching files (TSV or CSV depending on your data)
    for filepath in glob.glob(os.path.join(folder_path, file_pattern)):
        print(f"Reading: {filepath}")
        df = pd.read_excel(filepath)  # Assuming the files are in Excel format

        # Keep only relevant columns
        filtered_df = df.loc[:, ['gene', 'aa mutation', 'position', 'Frequency']]

        all_dfs.append(filtered_df)

    # Concatenate all filtered DataFrames
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # Save to CSV
    merged_df.to_csv(output_path, index=False)
    print(f"Merged file saved to: {output_path}")

    return merged_df

# Example usage
if __name__ == "__main__":
    folder = "mutation_tables"  # Replace with your actual folder
    merged = merge_mutation_files(folder)
    print(merged.head())