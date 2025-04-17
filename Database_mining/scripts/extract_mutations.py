
import os
import argparse
import pandas as pd
from Bio import SeqIO

def extract_mutations(msa_file, accession):
    """
    extract mutations from a given msa file
    """
    mutations = {}
    reference_seq = None


    # Parse the sequences and find the reference sequence
    for record in SeqIO.parse(msa_file, "fasta"):
        if accession in record.description:
            reference_seq = str(record.seq)
            break

    # Compare all sequences to the reference sequence
    for record in SeqIO.parse(msa_file, "fasta"):
        gap_count = 0  # Counter to track the number of gaps in the reference sequence
        for i, (ref_base, observed_base) in enumerate(zip(reference_seq, record.seq)):
            # Ignore if either reference or observed base is a gap '-'
            if ref_base == '-' :
                gap_count += 1
                continue

            if ref_base != observed_base:
                if observed_base != "-":
                # Adjust positions of mutations considering gaps
                    orig_position = i - gap_count
                    mutation = f"{ref_base}{orig_position+1}{observed_base}"
                    mutations[mutation] = mutations.get(mutation, 0) + 1

    # Sort mutations by frequency in descending order
    sorted_mutations = sorted(mutations.items(), key=lambda x: x[1], reverse=True)

    return sorted_mutations



def process_file(msa_file, accession, gene_name):
    """
    process files, extract mutations and write into a new file
    """
    # Extract mutations from the MSA file
    sorted_mutations = extract_mutations(msa_file, accession)

    # Create a DataFrame
    data = []
    for mutation, frequency in sorted_mutations:
        position = mutation[1:-1]  # Extract position from mutation
        data.append([gene_name, mutation, position, frequency])

    columns = ["gene", "aa mutation", "position", "Frequency"]
    df = pd.DataFrame(data, columns=columns)

    # Determine the output directory
    output_directory = os.path.dirname(msa_file)

    # Write DataFrame to Excel file in the same directory as the input file
    excel_file = os.path.join(output_directory, f"{gene_name}_mutations.xlsx")
    df.to_excel(excel_file, index=False)

    # Count mutations occurring more than 10 times, 10 times or lower, and total mutations
    mutations_gt_10 = sum(1 for freq in df['Frequency'] if freq > 10)
    mutations_10_or_lower = sum(1 for freq in df['Frequency'] if freq <= 10)
    total_mutations = len(df)

    # Print counts to the console
    print(f"Gene Name: {gene_name}")
    print(f"{mutations_gt_10}\t{mutations_10_or_lower}\t {total_mutations}")
    print(f"Total Mutations: {total_mutations}")

def get_files():
    """
    parse files
    """
    parser = argparse.ArgumentParser(
        description='Extract mutations from multiple sequence alignments.')
    parser.add_argument("-i", "--input" ,
                        help='Path(s) to the multiple sequence alignment file(s) (FASTA format)')
    parser.add_argument("-r","--ref", help='Accession of protein')
    parser.add_argument("-g","--gene", help='Gene name')
    args = parser.parse_args()
    arguments = args.__dict__

    return arguments

def main():
    """
    Main function
    """
    infiles = get_files()
    infile = infiles['input']
    ref = infiles['ref']
    gene = infiles['gene']

    process_file(infile,ref,gene)

if __name__ == "__main__":
    main()
