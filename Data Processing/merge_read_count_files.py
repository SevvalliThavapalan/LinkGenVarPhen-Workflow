"""
This script merges a primary table with multiple count tables and saves the output.
"""
import os
import argparse
import pandas as pd


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Analyze aligned files.")
    parser.add_argument("-r", "--reference", required=True,
                        help="Path to the reference sgRNA - insert file")
    parser.add_argument("-i", "--input", required=True, help="Path to read count files", nargs="+")
    parser.add_argument("-o", "--output", required=True, help= "Path to output file")
    return parser.parse_args()


def merge_with_multiple_files(table1_path, count_files, output_path):
    """
    Merge a primary table with multiple count tables and save the output.
    
    Parameters:
    - table1_path: str, path to the main table (Table 1).
    - count_files: list, paths to the count files (Table 2, etc.).
    - output_path: str, path to save the merged output.
    """
    # Load Table 1
    table1 = pd.read_excel(table1_path,  engine="openpyxl")
    print(table1.head())
    # Add "Reference" column to Table 1 based on "oligo no." and "gene"
    #table1["Reference"] = table1["oligo no."].astype(str) + "_" + table1["gene"]

    # Reorder columns to place "Reference" at the beginning
    #reordered_columns = ["Reference"] + [col for col in table1.columns if col != "Reference"]
    #table1 = table1[reordered_columns]

    # Initialize merged table with Table 1
    merged_table = table1.copy()

    # Process each count file
    for count_file in count_files:
        # Extract file name (without extension) to use as column name
        file_name = os.path.splitext(os.path.basename(count_file))[0]

        # Load the count file
        count_table = pd.read_csv(count_file,skipfooter=1, engine="python")

        # Rename the "Count" column to only include the file name
        count_table.rename(columns={"Count": file_name}, inplace=True)

        # Merge with the primary table using the "Reference" column
        merged_table = pd.merge(merged_table,
                                count_table[["Reference", file_name]], on="Reference", how="left")

    # Save the final merged table to the specified output path
    merged_table.to_excel(output_path, index=False)

    print(f"Merged table saved to {output_path}")


def abspath(path):
    """
    Custom function to get the absolute path.
    """
    return os.path.abspath(path.strip())


def main():
    """
    Main function.
    """
    # Example Usage
    args = parse_arguments()
    output = abspath(args.output)
    oligo_file = abspath(args.reference.strip())
    input_files = [os.path.abspath(file.strip()) for file in args.input]
    output = os.path.abspath(args.output.strip())

    count_files = input_files  # List of count files

    merge_with_multiple_files(oligo_file, count_files, output)


if __name__ == "__main__":
    main()
