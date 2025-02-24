"""
This script generates a list of all possible single amino acid mutations 
for a given protein sequence.
The script takes two arguments: the protein sequence and the gene name.
The script generates a list of all possible single amino acid mutations
for the given protein sequence.
The output is saved as an Excel file with the gene name and the list of mutations.
"""
import sys
import pandas as pd

def mutate_sequence(seq):
    """
    Hard-coded aa_code dictionary
    """
    aa_code = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }
    mutations_1 = []
    positions_1 = []
    aa_values_1 = []
    for i in range(1, len(seq)):
        aa_x = seq[i]
        for key, value in aa_code.items():
            mut_1 = f'{aa_x}{i + 1}{key}'
            mutations_1.append(mut_1)
            positions_1.append(i + 1)
            aa_values_1.append(value)
    return mutations_1, positions_1, aa_values_1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <sequence> <gene_name>")
        sys.exit(1)

    sequence = sys.argv[1]
    gene_name = sys.argv[2]
# Call the function
    mutations, positions, aa_values = mutate_sequence(sequence)


    gene_tab = [gene_name] * len(mutations)
    pos_values = [s[1:-1] for s in mutations]


    mutagenesis_df = pd.DataFrame()

    mutagenesis_df["Gene"] = gene_tab
    mutagenesis_df["Mutation"] = mutations
    mutagenesis_df["Position"] = pos_values

    mutagenesis_df.to_excel("output_mutagenesis.xlsx", index = False)
