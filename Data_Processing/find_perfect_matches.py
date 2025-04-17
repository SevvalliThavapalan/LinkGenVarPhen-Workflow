from collections import defaultdict
import argparse
import os

def parse_fasta(fasta_file):
    ref_dict = {}
    prefix_to_trim = "TCCTCTGGCGGAAAGCCT"
    with open(fasta_file, encoding="utf-8") as f:
        name = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if name:
                    full_seq = ''.join(seq_lines)
                    if full_seq.startswith(prefix_to_trim):
                        full_seq = full_seq[len(prefix_to_trim):]
                    ref_dict[name] = full_seq
                name = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line)
        if name:
            full_seq = ''.join(seq_lines)
            if full_seq.startswith(prefix_to_trim):
                full_seq = full_seq[len(prefix_to_trim):]
            ref_dict[name] = full_seq
    return ref_dict


def count_reference_matches_from_fasta(fastq_file, reference_fasta, out_file, matched_fastq=None):
    # Load references from FASTA
    ref_seqs = parse_fasta(reference_fasta)

    # Init match counts
    match_counts = defaultdict(int)
    matched_reads = []

    with open(fastq_file, encoding="utf-8") as fq, \
         open(matched_fastq, 'w', encoding="utf-8") if matched_fastq else open(os.devnull, 'w', encoding="utf-8") as matched_out:

        while True:
            header = fq.readline()
            if not header:
                break
            seq = fq.readline()
            plus = fq.readline()
            qual = fq.readline()

            matched = False
            for ref_name, ref_seq in ref_seqs.items():
                if ref_seq in seq:
                    match_counts[ref_name] += 1
                    matched = True
                    print(f"Matched {ref_seq} in read: {header.strip()}")

            if matched:
                matched_out.write(f"{header}{seq}{plus}{qual}")

    # Write counts to CSV
    with open(out_file, 'w', encoding="utf-8") as out:
        out.write("reference,count\n")
        for ref_name in sorted(ref_seqs):
            out.write(f"{ref_name},{match_counts.get(ref_name, 0)}\n")


def get_files():
    parser = argparse.ArgumentParser(description='Count reference matches in a FASTQ file.')
    parser.add_argument('-f', '--fastq_file', help='Input FASTQ file')
    parser.add_argument('-s','--sgRNAs_fasta_file', help='fasta file with sgRNA-insert sequences')
    parser.add_argument('-o', '--output', help='Output CSV file for match counts')
    parser.add_argument('-mf', '--matched_fastq', help='Optional: output FASTQ file of matched reads', default=None)
    return parser.parse_args()

def main():
    infiles = get_files()
    count_reference_matches_from_fasta(
        fastq_file=infiles.fastq_file,
        reference_fasta=infiles.sgRNAs_fasta_file,
        out_file=infiles.output,
        matched_fastq=infiles.matched_fastq
    )

if __name__ == "__main__":
    main()
