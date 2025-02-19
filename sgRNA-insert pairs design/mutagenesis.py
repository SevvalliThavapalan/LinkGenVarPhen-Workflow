import pandas as pd
import sys

def mutate_sequence(seq):
    # Hard-coded aa_code dictionary
    aa_code = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }
  
    tab1 = []
    tab2 = []
    tab3 = []
    
    for i in range(1, len(seq)):
        aa_X = seq[i]
        for key, value in aa_code.items():
            mut_1 = f'{aa_X}{i + 1}{key}'
            tab1.append(mut_1)
            tab2.append(i + 1)
            tab3.append(value)
    
    return tab1, tab2, tab3

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <sequence> <gene_name>")
        sys.exit(1)

    sequence = sys.argv[1]
    gene_name = sys.argv[2]
# Call the function
    tab1, tab2, tab3 = mutate_sequence(sequence)


    gene_tab = [gene_name] * len(tab1)
    positions = [s[1:-1] for s in tab1]


    mutagenesis_df = pd.DataFrame()

    mutagenesis_df["Gene"] = gene_tab
    mutagenesis_df["Mutation"] = tab1
    mutagenesis_df["Position"] = positions

    mutagenesis_df.to_excel("output_mutagenesis.xlsx", index = False)

