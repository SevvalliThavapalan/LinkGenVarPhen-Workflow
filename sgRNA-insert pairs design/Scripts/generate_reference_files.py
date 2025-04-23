"""
This script reads a csv file containing sgRNA-insert pairs 
and creates a fasta file containing the insert sequences 
and a csv file containing the protospacer sequences.
"""
import argparse
import pandas as pd

def create_fasta_from_table(csv_file, output_file, protospacer_file):
    """
    Create a FASTA and base pairing file from a table containing sequences.
    """
    # Read file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    protospacer_df = df[['reference', 'aa position', 'mutated aa','child codon',
                          'nt position', 'dist mut pam', 'mutated pam','base pairing region']]

    with open(output_file, 'w', encoding='utf-8') as fasta_file:
        # Iterate over rows in DataFrame
        for index, row in df.iterrows():
            # Extract header information from columns before the sequence column
            header_info = f"{row.iloc[0]}"
            # Extract sequence from the 'oligo column and remove the first part
            sequence = str(row['oligo']).upper()

            # Write header and sequence to FASTA file
            fasta_file.write(f'>{header_info}\n{sequence}\n')
    protospacer_df.to_csv(protospacer_file, index=False)

def get_files():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input',
                        help="csv file containing sgRNA-insert pairs ", required=True)
    parser.add_argument('-f', '--fasta', help='path to fasta out file', required=True)
    parser.add_argument('-b', '--basepairing', help='path to base pairing region out file', required=True)

    args = parser.parse_args()
    arguments = args.__dict__

    return arguments

def main():
    """
    Main function.
    """
    args = get_files()
    create_fasta_from_table(args['input'], args['fasta'], args['basepairing'])

if __name__ == "__main__":
    main()
