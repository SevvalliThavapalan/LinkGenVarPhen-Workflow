import argparse
from Bio import AlignIO
import pandas as pd


def get_files():
    """
    Parse input files
    """
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-a', '--alignment file', help='', required=True)
    parser.add_argument('-r', '--reference',
                        help='reference accession', required=True)
    parser.add_argument('-m', '--mutations', help = 'excel file containing list of mutations',
                        required =True)
    parser.add_argument('-o', '--output', help='output file name')
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments


def map_mutations_with_alignment(mutation_df, msa_file, ref_id, gene_column="gene", mutation_column="aa mutation", pos_column="position"):
    """
    Adjust mutations based on multiple sequence alignment gaps in the reference sequence.
    
    mutation_df: DataFrame with mutation data
    msa_file: FASTA alignment file
    ref_id: identifier for the reference sequence in the alignment
    """
    # Load alignment
    alignment = AlignIO.read(msa_file, "fasta")
    ref_seq = None

    # Find the reference sequence in the alignment
    for record in alignment:
        if ref_id in record.id or ref_id in record.description:
            ref_seq = record.seq
            break

    if ref_seq is None:
        raise ValueError(f"Reference ID '{ref_id}' not found in alignment.")

    print(f"Found reference sequence in alignment: {ref_id}")
    
    # Map from ungapped ref positions → alignment indices
    ungapped_pos = 0
    ungapped_to_aligned = {}
    for i, aa in enumerate(ref_seq):
        if aa != "-":
            ungapped_pos += 1
            ungapped_to_aligned[ungapped_pos] = i  # 1-based positions

    updated_rows = []

    for _, row in mutation_df.iterrows():
        gene = row[gene_column]
        mut = row[mutation_column]
        try:
            pos = int(row[pos_column])
        except ValueError:
            continue

        if pos not in ungapped_to_aligned:
            print(f"Position {pos} not in reference sequence (may be beyond length or in a gap). Skipping.")
            continue

        align_idx = ungapped_to_aligned[pos]
        ref_aa = ref_seq[align_idx]
        expected_ref_aa = mut[0]  # e.g., F from F123L

        if ref_aa != expected_ref_aa:
            print(f" Mismatch at position {pos}: expected {expected_ref_aa}, found {ref_aa}. Updating.")
            mut = f"{ref_aa}{pos}{mut[-1]}"  # rewrite mutation with actual ref AA

        # Update row
        row["Corrected Mutation"] = mut
        row["Aligned Position"] = align_idx + 1  # 1-based
        row["Aligned Ref AA"] = ref_aa
        updated_rows.append(row)

    corrected_df = pd.DataFrame(updated_rows)
    return corrected_df



def main():
    infiles = get_files()
    ref_accession = infiles['reference']
    alignment = infiles["alignment file"]
    mutation_file = infiles['mutations']
    output_file = infiles['output']

    mutation_df = pd.read_excel(mutation_file)
    corrected_df = map_mutations_with_alignment(
        mutation_df,
        msa_file=alignment,
        ref_id=ref_accession,
    )
    out_path = output_file+".xlsx"
    corrected_df.to_excel(out_path, index=False)



if __name__ == "__main__":
    main()
