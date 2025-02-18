import pandas as pd
import argparse

def create_fasta_from_table(csv_file, output_file, protospacer_file):
    # Read Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    protospacer_df = df[['gene', 'aa position', 'mutated aa', 'protospacer']]

    with open(output_file, 'w') as fasta_file:
        # Iterate over rows in DataFrame
        for index, row in df.iterrows():
            # Extract header information from columns before the sequence column
            header_info = f"{index}_{row.iloc[0]}"
            # Extract sequence from the 'oligo column and remove the first part
            sequence = str(row['oligo']).upper()

            # Write header and sequence to FASTA file
            fasta_file.write(f'>{header_info}\n{sequence}\n')
    
    protospacer_df.to_csv(protospacer_file, index=True)
   
def get_files():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="csv file containing sgRNA-insert pairs ", required=True)
    parser.add_argument('-f', '--fasta', help='path to fasta out file', required=True)
    parser.add_argument('-p', '--protospacer', help='path to protospacer out file', required=True)
   
    args = parser.parse_args()
    arguments = args.__dict__

    return arguments

def main():
    args = get_files()
    create_fasta_from_table(args['input'], args['output'], args['protospacer'])

if __name__ == "__main__":
    main()