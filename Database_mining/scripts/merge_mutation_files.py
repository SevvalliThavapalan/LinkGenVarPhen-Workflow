import pandas as pd
import glob
import os
import argparse

def get_files():
    """
    Parse input files
    """
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--input folder', help='input directory', required=True)
    parser.add_argument('-o', '--output', help='output file name')
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments

def merge_mutation_files(folder_path, output_path,file_pattern="*.xlsx"):
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
    merged_df.to_excel(output_path, index=False)
    print(f"Merged file saved to: {output_path}")

    return merged_df

def main():
    args = get_files()
    folder_path = args['input folder']
    output_path = args['output'] if args['output'] else "merged_mutations.xlsx"

    merged_df = merge_mutation_files(folder_path, output_path)
    print(merged_df.head())

# Example usage
if __name__ == "__main__":
    main()