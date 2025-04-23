"""
This script finds potential off-targets for a set of base pairing regions.
The base pairing regions are loaded from a TSV file, and the genome is loaded from 
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
from collections import defaultdict
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




def process_protospacer(reference,protospacer, genome_seq, max_mismatches=4):
    """
    Find potential off-targets in the genome sequence for a given base pairing region.
    Returns the protospacer and a list of tuples: (matched_seq, position, mismatches).
    Includes protospacers with no matches (empty off-target list).
    """
    print(f"Checking base pairing region for {reference}: {protospacer}")
    off_targets = []

    pattern = f"({protospacer}){{e<={max_mismatches}}}"

    for match in re.finditer(pattern, genome_seq, overlapped=True):
        matched_seq = match.group()
        position = match.start()
        mismatches = match.fuzzy_counts[0]
        off_targets.append((matched_seq, position, mismatches))

    return (reference, protospacer, off_targets)


def highlight_protospacers(df):
    """
    Highlight base pairing regions with 4 mismatches or less
    """
    def highlight_row(row):
        if row['Mismatches'] == 4 or row['Mismatches'] == 0:
            return ['font-weight: bold; background-color: yellow'] * len(df.columns)
        return [''] * len(df.columns)

    return df.style.apply(highlight_row, axis=1)

def main():
    """
    Main function to find off-targets for all protospacers
    """
    # Load the base pairing regions from a TSV file
    args = get_files()
    protospacers_df = pd.read_csv(args['input'], engine='python')
    print("Loaded protospacers:")
    print(protospacers_df[['reference', 'base pairing region']].head(12))
    protospacers = protospacers_df['base pairing region'].tolist()
    print(len(protospacers), "protospacers loaded")
    protospacer_dict = defaultdict(list)
    for _, row in protospacers_df.iterrows():
        protospacer_dict[row['base pairing region']].append(row['reference'])


    # Load the E. coli genome from a GenBank file
    ecoli_genome = SeqIO.read(args['genome'], "genbank")

    # Convert genome sequence to a string (for performance)
    genome_seq = str(ecoli_genome.seq)

# Run the off-target search in parallel

    with Pool() as pool:
        tasks = []
        for protospacer, refs in protospacer_dict.items():
            for ref in refs:
                tasks.append((ref, protospacer, genome_seq))
        results = pool.starmap(process_protospacer, tasks)




    # Prepare data for Excel
    data = []
    for reference, protospacer, targets in results:
        if targets:
            for target in targets:
                data.append([reference, protospacer, target[0], target[1], target[2]])
        else:
            data.append([reference, protospacer, "", "", ""])


    # Create DataFrame
    df = pd.DataFrame(data, columns=['reference','base pairing region',
                                     'Off-Target Sequence', 'aa position', 'Mismatches'])
    styled_df = highlight_protospacers(df)
    print(f"Number of unique references processed: {df['reference'].nunique()}")
    print(f"Number of total rows: {len(df)}")
    print(df['reference'].value_counts())


    # Write DataFrame to Excel
    output_file = args['output']
    styled_df.to_excel(output_file, index=False)

    print(f"Results have been written to {output_file}")


if __name__ == "__main__":
    main()
