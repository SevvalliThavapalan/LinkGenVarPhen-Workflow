# import fasta file and filter it by length
# Usage: python filter_fasta_file.py <fasta_file> <min_length> <max_length>

#import fasta file
from Bio import SeqIO
import argparse
from pathlib import Path

"""
Takes a fasta file and filters it by length. The resulting file is saved separateley.
"""

def parser():
    parser = argparse.ArgumentParser(description='A given fasta file is filtered by lenght.')
    parser.add_argument('-i', '--input', help="fastafile", required=True) 
    parser.add_argument('-o', '--output', help='path and name to outfile', required=True)
    parser.add_argument('-l', '--length', help=' min length of sequence', required=True)
    
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments


def main():
    infiles = parser()
    out_path = Path(infiles['output'])
    print(out_path)
    filtered_accessions = []
    
    for rec in SeqIO.parse(infiles['input'], 'fasta'):
        name = rec.id
        seq = rec.seq
        seqLen = len(rec)

        if seqLen < int(infiles['length']) -0 or seqLen > int(infiles['length']) +0: 
            #print(seqLen)
            filtered_accessions.append(name)
    print(len(filtered_accessions))
    with open(out_path, 'w') as f:
        for rec in SeqIO.parse(infiles['input'], 'fasta'):
            name = rec.id
            seq = rec.seq
            seqLen = len(rec)
            #check if entry in file is in fasta file
            if name not in filtered_accessions:
                #write whole record to file
                f.write('>' + name + ' ' +rec.description + '\n' + str(seq)+ '\n' )
    f.close()


if __name__ == "__main__":
    main()	

