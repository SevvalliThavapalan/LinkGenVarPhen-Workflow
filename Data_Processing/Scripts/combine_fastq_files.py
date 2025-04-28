"""
Combine all fastq files with the same barcode into a single file
"""
import os
import gzip
import argparse

def get_files():
    """
    Get the input files from the command line
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="Directory containing fastq files",
                        required=True, nargs="+")
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments



def get_input_directory():
    """
    Get the input directory from the user
    """
    input_dir = input("Enter the input directory: ")
    return input_dir


def combine_fastq_files(input_dir):
    """
    Combine all fastq files with the same barcode into a single file
    """
    for root, dirs, files in os.walk(input_dir):
        barcode_to_sequences = {}
        for filename in files:
            if filename.endswith('.fastq') or filename.endswith('.fastq.gz'):
                barcode = os.path.basename(root)  # Use directory name as barcode
                file_path = os.path.join(root, filename)

                # Check if file is gzipped and open accordingly
                if filename.endswith('.gz'):
                    print("Processing file: " + filename)
                    open_func = gzip.open
                    mode = 'rt'  # Text mode for reading gzipped files
                else:
                    open_func = open
                    mode = 'r'

                with open_func(file_path, mode) as f:
                    lines = f.readlines()
                    if barcode not in barcode_to_sequences:
                        barcode_to_sequences[barcode] = []
                    barcode_to_sequences[barcode].extend(lines)

        for barcode, sequences in barcode_to_sequences.items():
            output_file = os.path.join(root, f"{barcode}.fastq")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(sequences)
            print(f"Combined {len(sequences)//4} sequences for barcode {barcode} to {output_file}")

def main():
    """
    Main function
    """
    input_files = get_files()
    input_dir = input_files["input"][0]
    #unzip_fastq_files(input_dir)
    combine_fastq_files(input_dir)

if __name__ == "__main__":
    main()
