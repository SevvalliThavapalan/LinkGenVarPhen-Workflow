"""
Analyze aligned files and filter reads based on various criteria.
The script reads a reference FASTA file and an aligned SAM file.
It parses the files, finds mutations and indels in the reads compared to the reference,
and filters reads based on various criteria.
The script writes a summary of the analysis and a new SAM file with filtered reads.
"""
import re
import argparse
import concurrent.futures
import os
from collections import defaultdict
from Bio import SeqIO
import pandas as pd


def parse_arguments():
    """
    Parse command-line arguments for the script.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Analyze aligned files.")
    parser.add_argument("-r", "--reference", required=True, help="Path to the reference FASTA file")
    parser.add_argument("-i", "--input", required=True, help="Path to the aligned SAM file")
    parser.add_argument("-o", "--output", required=True, help= "Path to output directory")
    return parser.parse_args()

def parse_fasta(fasta_file):
    """
    Parse the FASTA file and return a dictionary of reference sequences.
    The dictionary keys are the sequence IDs and the values are the sequences.
    """
    ref_sequences = {}
    reffile = open(fasta_file, 'r', encoding='utf-8')
    for record in SeqIO.parse(reffile, "fasta"):
        ref_sequences[record.id] = str(record.seq)
    return ref_sequences

def parse_cigar(cigar):
    """
    Parse the CIGAR string and return a list of operations.
    Each operation is a tuple (length, operation), where length is an integer
    and operation is one of 'M', 'I', 'D', 'N', 'S', 'H', 'P', '=', or 'X'.
    """
    return [(int(length), op) for length, op in re.findall(r'(\d+)([MIDNSHP=X])', cigar)]

def find_mutations_and_indels(read, ref_sequence, ref_start_pos):
    """
    Find mutations and indels in the read compared to the reference sequence.
    Returns a list of tuples (position, reference base, read base) for each mutation or indel.
    """
    cigar = read[5]
    read_seq = read[9]
    read_pos = 0
    ref_pos = ref_start_pos
    mutations_and_indels = []
    for length, op in parse_cigar(cigar):
        if op == 'M':  # Match or mismatch
            for i in range(length):
                if ref_sequence[ref_pos - 1] != read_seq[read_pos]:
                    mutations_and_indels.append((ref_pos,
                                                 ref_sequence[ref_pos - 1], read_seq[read_pos]))
                ref_pos += 1
                read_pos += 1
        elif op == 'I':  # Insertion to the reference
            mutations_and_indels.append((ref_pos, 'I', read_seq[read_pos:read_pos + length]))
            read_pos += length
        elif op == 'D':  # Deletion from the reference
            mutations_and_indels.append((ref_pos, 'D', '-' * length))
            ref_pos += length
        elif op in 'NSHP=X':  # Skip, soft/hard clipping, padding, sequence match, sequence mismatch
            if op == '=':
                read_pos += length
                ref_pos += length
            elif op == 'X':
                for i in range(length):
                    if ref_sequence[ref_pos - 1] != read_seq[read_pos]:
                        mutations_and_indels.append((ref_pos,
                                                     ref_sequence[ref_pos - 1], read_seq[read_pos]))
                    ref_pos += 1
                    read_pos += 1
            else:
                # Skip these operations
                pass

    return mutations_and_indels

def has_consecutive_mutations_or_indels(mutations_and_indels):
    """
    Check if there are more than two/three consecutive mutations or indels.
    """
    if len(mutations_and_indels) < 2:    #adapt
        return False
    for i in range(1, len(mutations_and_indels)):
        if mutations_and_indels[i][0] == mutations_and_indels[i - 1][0] + 1:
            return True
    return False

def parse_sam(file_path):
    """
    Parse the SAM file and return a dictionary of reads grouped by reference sequence name.
    The dictionary keys are the reference sequence names and the values are lists of reads.
    Each read is a tuple (fields, start_pos), where fields is a list of 
    fields and start_pos is the 1-based start position.
    """
    reads_by_rname = {}
    header_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('@'):
                header_lines.append(line)
                continue
            fields = line.strip().split('\t')
            rname = fields[2]  # Reference sequence name
            pos = int(fields[3])  # 1-based leftmost mapping position
            if rname not in reads_by_rname:
                reads_by_rname[rname] = []
            reads_by_rname[rname].append((fields, pos))
    return reads_by_rname, header_lines


def summarize_mutations_and_indels(grouped_reads, ref_sequences):
    """
    Summarize mutations and indels in the reads compared to the reference sequences.
    Returns a dictionary of dictionaries, where the first key is the reference sequence name,
    the second key is the position, and the value is a set of read identifiers.
    """
    mutation_indel_summary = defaultdict(lambda: defaultdict(set))  # Store sets of read identifiers
    for rname, reads in grouped_reads.items():
        if rname not in ref_sequences:
            print(f"Reference sequence for {rname} not provided.")
            continue
        ref_sequence = ref_sequences[rname]
        for read, start_pos in reads:
            read_id = read[0]  # Assuming the read ID is the first field in SAM format
            mutations_and_indels = find_mutations_and_indels(read, ref_sequence, start_pos)
            for mutation_or_indel in mutations_and_indels:
                position = mutation_or_indel[0]
                mutation_indel_summary[rname][position].add(read_id)  # Store unique read IDs
    return mutation_indel_summary

def filter_reads(grouped_reads, ref_sequences, mutation_indel_summary):
    """
    Filter reads based on various criteria.
    Returns a dictionary of reads grouped by reference sequence name.
    """
    filtered_reads_by_rname = defaultdict(list)
    short = 0
    large_indel = 0
    consecutive_mutation = 0
    cas_proto = 0
    skipped = 0
    other_skipped = 0


    filtered_summary = {
        rname: {pos: reads for pos, reads in positions.items()
                if len(reads) > 3} # remove if Mutation can be found in 3 reads or more
        for rname, positions in mutation_indel_summary.items()
    }

    for rname, reads in grouped_reads.items():
        if rname not in ref_sequences:
            print(f"Reference {rname} missing in FASTA. Skipping {len(reads)} reads.")
            skipped += len(reads)
            continue
        for read, start_pos in reads:
            cigar = read[5]
            read_id = read[0]
            if not cigar or not re.match(r'(\d+[MIDNSHP=X])+$', cigar):
                #print(f"Invalid CIGAR string: {cigar}")
                other_skipped += 1
                continue

            alignment_length = sum(length for length, op in parse_cigar(cigar) if op in 'MD=X')
            if alignment_length < 175:
                short += 1
                continue

            mutations_and_indels = find_mutations_and_indels(read, ref_sequences[rname], start_pos)
            last_58_mutations_indels = [mut for mut in mutations_and_indels
                                        if mut[0] >= start_pos + alignment_length - 58]
            if len(last_58_mutations_indels) >= 5:
                cas_proto += 1
                continue

            if any(op in 'ID' and int(length) > 3 for length, op in parse_cigar(cigar)):
                large_indel += 1
                continue

            if has_consecutive_mutations_or_indels(mutations_and_indels):
                consecutive_mutation += 1
                continue

            if not any(read_id in filtered_summary[rname].get(pos, set())
                       for pos in filtered_summary.get(rname, {})):
                filtered_reads_by_rname[rname].append(read)

    return filtered_reads_by_rname, short, large_indel, consecutive_mutation, cas_proto, skipped

def count_remaining_reads(filtered_reads_by_rname):
    """
    Count the remaining reads after filtering.
    Returns a dictionary of reference sequence names and the number of remaining reads.
    """
    read_counts = {rname: len(reads) for rname, reads in filtered_reads_by_rname.items()}

    return read_counts


def write_filtered_sam(filtered_reads_by_rname, header_lines, output_file):
    """
    Write the filtered reads to a new SAM file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in header_lines:
            f.write(line)
        for reads in filtered_reads_by_rname.values():
            for read in reads:
                f.write('\t'.join(read) + '\n')



def main():
    """
    Main function for the script.
    """
    args = parse_arguments()
    # Clean and convert paths to absolute paths
    fasta_file = os.path.abspath(args.reference.strip())
    input_file = os.path.abspath(args.input.strip())
    output = os.path.abspath(args.output.strip())

    print(f"Using reference FASTA file: {fasta_file}")
    print(f"Using input SAM file: {input_file}")
    print(f"Using prefix for outputs: {output}")

    # Check if both files exist
    if not os.path.isfile(fasta_file):
        raise FileNotFoundError(f"FASTA file not found: {fasta_file}")
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"SAM file not found: {input_file}")

    output_sam_file = output + "_filtered.sam"

    # Parse FASTA in a separate thread (if it's not CPU-heavy)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ref_sequences_future = executor.submit(parse_fasta, fasta_file)
        grouped_reads_future = executor.submit(parse_sam, input_file)
        ref_sequences = ref_sequences_future.result()
        grouped_reads, header_lines = grouped_reads_future.result()
        mutation_indel_summary = summarize_mutations_and_indels(grouped_reads, ref_sequences)
        (filtered_reads_by_rname,short_reads,large_indel,consecutive_mutation,
         cas_proto,skipped) = filter_reads(grouped_reads,ref_sequences,mutation_indel_summary)
        #print(mutation_indel_summary)

    # Count total reads before filtering
    total_reads = sum(len(reads) for reads in grouped_reads.values())

    # Count filtered reads after processing
    filtered_count = sum(len(reads) for reads in filtered_reads_by_rname.values())

    # Calculate total explicitly dropped reads
    dropped_count = short_reads + large_indel + consecutive_mutation + cas_proto + skipped

    # Calculate other dropped reads
    other_dropped = total_reads - (filtered_count + dropped_count)
     # Optionally, write the DataFrame to a CSV file

    log_file = output + "_summary.txt"
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(f"Using reference FASTA file: {fasta_file}\n")
        file.write(f"Using input SAM file: {input_file}\n")
        file.write(f"Using prefix for outputs: {output}\n")
        file.write("Parsing files done\n")
        file.write(f"Aligned reads: {total_reads}\n")
        file.write(f"Final reads after filtering: {filtered_count}\n")
        file.write(f"Dropped reads (short reads): {short_reads}\n")
        file.write(f"Dropped reads (5 or more mutation in sgRNA): {cas_proto}\n")
        file.write(f"Dropped reads (large indels in insert): {large_indel}\n")
        file.write(f"Dropped reads (consecutive mutations in insert): {consecutive_mutation}\n")
        file.write(f"Dropped reads (no reference): {skipped}\n")
        file.write(f"Other dropped reads: {other_dropped}\n")

    print(f"Summary written to {log_file}")

    read_counts = count_remaining_reads(filtered_reads_by_rname)

    df = pd.DataFrame(list(read_counts.items()), columns=['reference', 'Count'])
    df.to_csv(output +'_remaining_reads.csv', index=False)
    write_filtered_sam(filtered_reads_by_rname, header_lines, output_sam_file)




if __name__ == "__main__":
    main()
