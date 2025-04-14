"""
Perform mutagenesis on a given protein sequence.
"""
import pandas as pd




def mutate_sequence(seq):
    """
    Function to generate all possible amino acid mutations for a given protein sequence.
    """
    # Hard-coded aa_code dictionary
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

def mutagenesis(gene_name, sequence):
    """
    Function to generate a table of all possible 
    amino acid mutations for a given protein sequence.
    """
    # Call the function
    mutations, positions, aa_values = mutate_sequence(sequence)


    gene_tab = [gene_name] * len(mutations)
    positions = [s[1:-1] for s in mutations]


    mutagenesis_df = pd.DataFrame()

    mutagenesis_df["gene"] = gene_tab
    mutagenesis_df["aa mutation"] = mutations
    mutagenesis_df["position"] = positions

    return mutagenesis_df
