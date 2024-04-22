# -*- coding: utf-8 -*-
"""
Created on 26.10.2023

@author: Sevvalli Thavapalan
"""

import pandas as pd

import argparse
from Bio import SeqIO



def get_files():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="fasta file containing the protein sequences", required=True, nargs="+")
    parser.add_argument('-r', '--reference',
                        help='reference accession', required=True)
    parser.add_argument('-p', '--position',required=True, help="Position to check", type=int)
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments

def main():
    infiles = get_files()
   # out_path = infiles['output']
    infile = infiles['input']
    ref = infiles['reference']
    pos = infiles['position']
    pos = int(pos)
    fasta_sequences = SeqIO.parse(open(infile[0]), 'fasta')

    ref_seq = ""

    fasta_dict = {}
    for fasta in fasta_sequences:
        fasta_dict[fasta.description] = str(fasta.seq)
    print(ref)
    for key, values in fasta_dict.items():
        if ref in key:
            ref_seq = values
    print(ref_seq)
    print(ref_seq[pos-1])


if __name__ == "__main__":
    main()
