# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:55:29 2022

@author: Sevvalli Thavapalan
"""
import argparse
from Bio import SeqIO
import pandas as pd


def get_files():
    """
    Parse input files
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="fasta file containing the protein sequences",
                        required=True, nargs="+")
    parser.add_argument('-g', '--gene', help='gene name ', required=True)
    parser.add_argument('-r', '--reference',
                        help='reference accession', required=True)
    parser.add_argument('-m', '--mutations', help = 'excel file containing list of mutations',
                        required =True)
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments

def main():
    """
    Main function
    """
    infiles = get_files()
   # out_path = infiles['output']
    infile = infiles['input']
    ref = infiles['reference']
    gene = infiles["gene"]
    fasta_sequences = SeqIO.parse(open(infile[0], encoding="utf-8"), 'fasta')
    mutations = infiles['mutations']
    mutation_df = pd.read_excel(mutations)
    ref_seq = ""

    fasta_dict = {}
    for fasta in fasta_sequences:
        fasta_dict[fasta.description] = str(fasta.seq)
    print(ref)
    for key, values in fasta_dict.items():
        if ref in key:
            ref_seq = values

    print(ref_seq)

    pos = mutation_df.loc[mutation_df['gene'] == gene, "position"]
    muts = mutation_df.loc[mutation_df['gene'] == gene, "aa mutation"]
    ref_pos = []
    aa_pos = []


    for i in pos:

        if i <= len(ref_seq):
            ref_pos.append(ref_seq[i-1])
            aa_pos.append(int(i))

    mut_pos = []
    for i in muts:
        mut_pos.append(i[0])
    print("Missmatched mutations")
    for i in range(len(mut_pos)):
        if i <= len(ref_seq):
            if ref_pos[i]!= mut_pos[i]:
            
                print(aa_pos[i], ref_pos[i], mut_pos[i])
        else:
            print("remove:"+i)


if __name__ == "__main__":
    main()
