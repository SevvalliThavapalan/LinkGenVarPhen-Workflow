"""
This script finds potential off-targets in the E. coli genome for a set of base pairing regions.
The list is loaded from a TSV file, and the E. coli genome is loaded from a GenBank file.
The off-target search is performed using regex with fuzzy matching, allowing up to 4 mismatches.
The results are written to an Excel file, which includes the base pairing regions,
the off-target sequence,
the position in the genome, and the number of mismatches.
The off-target search is performed in parallel using the multiprocessing module to improve 
performance.
"""

from multiprocessing import Pool
from collections import defaultdict
import pandas as pd
from Bio import SeqIO

import regex as re


def process_protospacer(reference, protospacer, genome_seq, max_mismatches=4):
    """
    Find potential off-targets in the genome sequence for a given base pairing region.
    Returns the protospacer and a list of tuples: (matched_seq, position, mismatches).
    Includes protospacers with no matches (empty off-target list).
    """
    print(f"Checking base pairing region for {reference}: {protospacer}")
    off_targets = []

    pattern = f"({protospacer}){{s<={max_mismatches}}}"

    for match in re.finditer(pattern, genome_seq, overlapped=True):
        matched_seq = match.group()
        position = match.start()
        mismatches = match.fuzzy_counts[0]
        off_targets.append((matched_seq, position, mismatches))

    return (reference, protospacer, off_targets)

def highlight_protospacers(df):
    """
    Highlight base regionss with 4 mismatches or more
    """
    def highlight_row(row):
        if row['Mismatches'] == 4 or row['Mismatches'] == "None":
            return ['font-weight: bold; background-color: yellow'] * len(df.columns)
        return [''] * len(df.columns)

    return df.style.apply(highlight_row, axis=1)

def off_target(protospacers_file, genome_file):
    """
    Find potential off-targets in the genome sequence for a given protospacer
    """

    protospacers = protospacers_file['base pairing region'].tolist()
    print(len(protospacers), "protospacers loaded")
    protospacer_dict = defaultdict(list)
    for _, row in protospacers_file.iterrows():
        protospacer_dict[row['base pairing region']].append(row['reference'])



    genome = SeqIO.read(genome_file, "genbank")
    genome_seq = str(genome.seq)

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
        if targets and len(targets) > 0:
            for target in targets:
                data.append([reference, protospacer, target[0], target[1], target[2]])
        else:
            data.append([reference, protospacer, "", "", "None"])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['reference','base pairing region',
                                     'Off-Target Sequence', 'Position', 'Mismatches'])
    styled_df = highlight_protospacers(df)
    print(f"Number of unique references processed: {df['reference'].nunique()}")
    return styled_df
