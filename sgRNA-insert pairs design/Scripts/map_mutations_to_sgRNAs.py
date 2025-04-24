import pandas as pd
import argparse


def get_files():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="File with mutations", required=True, nargs="+")
    parser.add_argument('-s','--sgRNA', help="File with sgRNA sequences", required=True, nargs="+")
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments

def main():
    """
    Main function to read in the sgRNA and mutations files, map the mutations 
    to sgRNAs, and check if all sgRNAs are present in the mutations file.
    """
    infiles = get_files()
    mutations = infiles["input"][0]
    sgRNA = infiles["sgRNA"][0]
    
    # Read in the sgRNA sequences and mutations
    sgRNA_df = pd.read_csv(sgRNA, sep=",", header=0)
    mutations_df = pd.read_excel(mutations, header=0)

    # Map mutation to amino acid using three_one dictionary
    three_one = { "A" : "ALA", "G" : "GLY", "I" : "ILE", "L" : "LEU", "P" : "PRO",
                  "V" : "VAL", "F" : "PHE", "W" : "TRP", "Y" : "TYR", "D" : "ASP",
                  "E" : "GLU", "R" : "ARG", "H" : "HIS", "K" : "LYS", "S" : "SER",
                  "T" : "THR", "C" : "CYS", "M" : "MET", "N" : "ASN", "Q" : "GLN"
    }
    mutations_df['parent aa'] = mutations_df['mutation'].str[0].map(three_one)
    mutations_df['mutated aa'] = mutations_df['mutation'].str[-1].map(three_one)

    # Merge mutations with sgRNA data
    merged_oligos = pd.merge(sgRNA_df, mutations_df,
                             on=['gene', 'aa position', 'parent aa', 'mutated aa'], how='left')
    merged_oligos = merged_oligos.drop_duplicates(subset=['reference'])

    # Identify mutations not present in sgRNA file
    missing_mutations = mutations_df[~mutations_df['mutation'].isin(merged_oligos['mutation'])]

    # Check if all sgRNAs are present
    if len(merged_oligos) == len(sgRNA_df):
        print("All sgRNAs are present in the mutations file.")
    else:
        print("Not all sgRNAs are present in the mutations file. The design needs to be adjusted. Please contact us for help.")
        
    # Print mutations that are missing from the sgRNA file
    print("\nThe following mutations are not present in the sgRNA file:")
    print(missing_mutations[['gene', 'aa position', 'mutation']])


if __name__ == "__main__":
    main()
    