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
import pandas as pd
from Bio import SeqIO
import regex as re


def process_protospacer(protospacer, genome_seq, max_mismatches=4):
    """
    Find potential off-targets in the genome sequence for a given protospacer
    """
    print(f"Checking protospacer: {protospacer}")
    off_targets = []

    # Use regex with fuzzy matching (up to max_mismatches)
    pattern = f"({protospacer}){{e<={max_mismatches}}}"
    for match in re.finditer(pattern, genome_seq, overlapped=True):
        off_targets.append((match.group(), match.start(), match.fuzzy_counts[0]))

    return (protospacer, off_targets)

def highlight_protospacers(df):
    """
    Highlight base regionss with 4 mismatches or more
    """
    def highlight_row(row):
        if row['Mismatches'] == 4 or pd.isnull(row['Mismatches']):
            return ['font-weight: bold; background-color: yellow'] * len(df.columns)
        return [''] * len(df.columns)

    return df.style.apply(highlight_row, axis=1)

def off_target(protospacers_file, genome_file):
    """
    Find potential off-targets in the genome sequence for a given protospacer
    """
    protospacers_file['oligo'] = (protospacers_file.index.astype(str) +
                                   '_' + protospacers_file['gene'])
    protospacers = protospacers_file['base pairing region'].tolist()
    protospacer_dict = dict(zip(protospacers_file['base pairing region'],
                                protospacers_file['oligo']))
    genome = SeqIO.read(genome_file, "genbank")
    genome_seq = str(genome.seq)
    with Pool() as pool:
        results = pool.starmap(process_protospacer, [(p, genome_seq) for p in protospacers])

    off_targets_dict = dict(results)

    # Prepare data for Excel
    data = []
    for protospacer, targets in off_targets_dict.items():
        if targets:
            for target in targets:
                data.append([protospacer_dict[protospacer],
                             protospacer, target[0], target[1], target[2]])
        else:
            data.append([protospacer, "", "", ""])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Oligo no','base pairing region',
                                     'Off-Target Sequence', 'Position', 'Mismatches'])
    styled_df = highlight_protospacers(df)
    return styled_df
