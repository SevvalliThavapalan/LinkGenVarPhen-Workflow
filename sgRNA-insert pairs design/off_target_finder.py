"""
This script finds potential off-targets in the E. coli genome for a set of base pairing regions.
The base pairing regions are loaded from a TSV file, and the E. coli genome is loaded from 
a GenBank file.
The off-target search is performed using regex with fuzzy matching, allowing up to 4 mismatches.
The results are written to an Excel file, which includes the base pairing regions, 
the off-target sequence,
the position in the genome, and the number of mismatches.
The off-target search is performed in parallel using the multiprocessing module to improve 
performance.
"""
from multiprocessing import Pool
import argparse
import regex as re
import pandas as pd
from Bio import SeqIO


def get_files():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input',
                        help="csv file containig base pairing regions ", required=True)
    parser.add_argument('-g', '--genome', help='path to genome in gb format', required=True)
    parser.add_argument('-o', '--output', help='path to out file in xlsx format', required=True)

    args = parser.parse_args()
    arguments = args.__dict__

    return arguments


# Function to find potential off-targets for a single base pairing region
def process_protospacer(protospacer, genome_seq, max_mismatches=4):
    """
    Find potential off-targets in the genome sequence for a given base pairing region
    """
    print(f"Checking base pairing region: {protospacer}")
    off_targets = []

    # Use regex with fuzzy matching (up to max_mismatches)
    pattern = f"({protospacer}){{e<={max_mismatches}}}"
    for match in re.finditer(pattern, genome_seq, overlapped=True):
        off_targets.append((match.group(), match.start(), match.fuzzy_counts[0]))

    return (protospacer, off_targets)

def highlight_protospacers(df):
    """
    Highlight base pairing regions with 4 mismatches or less
    """
    def highlight_row(row):
        if row['Mismatches'] == 4 or pd.isnull(row['Mismatches']):
            return ['font-weight: bold; background-color: yellow'] * len(df.columns)
        return [''] * len(df.columns)

    return df.style.apply(highlight_row, axis=1)

def main():
    """
    Main function to find off-targets for all protospacers
    """
    # Load the base pairing regions from a TSV file
    args = get_files()
    protospacers_df = pd.read_csv(args['input'], sep='[,;]', engine='python')
    protospacers_df['oligo'] = protospacers_df.index.astype(str) + '_' + protospacers_df['gene']
    protospacers = protospacers_df['base pairing region'].tolist()
    protospacer_dict = dict(zip(protospacers_df['base pairing region'], protospacers_df['oligo']))


    # Load the E. coli genome from a GenBank file
    ecoli_genome = SeqIO.read(args['genome'], "genbank")

    # Convert genome sequence to a string (for performance)
    genome_seq = str(ecoli_genome.seq)

# Run the off-target search in parallel

    with Pool() as pool:
        results = pool.starmap(process_protospacer, [(p, genome_seq) for p in protospacers])

    # Convert results into a dictionary
    off_targets_dict = dict(results)

    # Prepare data for Excel
    data = []
    for protospacer, targets in off_targets_dict.items():
        if targets:
            for target in targets:
                data.append([protospacer_dict[protospacer],protospacer, target[0],
                             target[1], target[2]])
        else:
            data.append([protospacer_dict[protospacer],protospacer, "", "", ""])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Oligo no','base pairing region',
                                     'Off-Target Sequence', 'Position', 'Mismatches'])
    styled_df = highlight_protospacers(df)

    # Write DataFrame to Excel
    output_file = args['output']
    styled_df.to_excel(output_file, index=False)

    print(f"Results have been written to {output_file}")


if __name__ == "__main__":
    main()
