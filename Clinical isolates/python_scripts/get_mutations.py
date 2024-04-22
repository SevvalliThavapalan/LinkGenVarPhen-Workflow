from Bio import SeqIO
import os
import argparse
import pandas as pd

def extract_mutations(msa_file):
    mutations = {}
    reference_seq = None

    # Parse the sequences and find the reference sequence
    for record in SeqIO.parse(msa_file, "fasta"):
        if "Escherichia coli BW25113" in record.description:
            reference_seq = str(record.seq)
            break

    # Compare all sequences to the reference sequence
    for record in SeqIO.parse(msa_file, "fasta"):
        for i, (ref_base, observed_base) in enumerate(zip(reference_seq, record.seq)):
            if ref_base != observed_base and ref_base != '-' and observed_base != '-':
                mutation = f"{ref_base}{i+1}{observed_base}"
                mutations[mutation] = mutations.get(mutation, 0) + 1

    # Sort mutations by frequency in descending order
    sorted_mutations = sorted(mutations.items(), key=lambda x: x[1], reverse=True)

    return sorted_mutations

def get_gene_name(file_name):
    # Extract gene name from the file name
    parts = file_name.split("_")
    if len(parts) >= 2:
        return parts[0]
    return "Unknown"

def process_file(msa_file):
    gene_name = get_gene_name(os.path.basename(msa_file))
    sorted_mutations = extract_mutations(msa_file)

    # Create a DataFrame
    data = []
    for mutation, frequency in sorted_mutations:
        position = mutation[1:-1]  # Extract position from mutation
        data.append([gene_name, mutation, position, frequency])

    columns = ["Gene Name", "Mutation", "Position", "Frequency"]
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

def main():
    parser = argparse.ArgumentParser(description='Extract mutations from multiple sequence alignments.')
    parser.add_argument('msa_files', nargs='+', help='Path(s) to the multiple sequence alignment file(s) (FASTA format)')
    args = parser.parse_args()

    for msa_file in args.msa_files:
        process_file(msa_file)

if __name__ == "__main__":
    main()
