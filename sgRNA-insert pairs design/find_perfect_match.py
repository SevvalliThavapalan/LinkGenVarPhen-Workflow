from Bio import SeqIO
import pandas as pd
import parasail
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to read sequences from a FASTQ file
def read_fastq(file_path):
    sequences = []
    with open(file_path, "r") as file:
        for record in SeqIO.parse(file, "fastq"):
            sequences.append(str(record.seq))
    return sequences

# Function to calculate mismatches and gaps from an alignment
def calculate_mismatches_and_gaps(align1, align2):
    mismatches = sum(1 for a, b in zip(align1, align2) if a != b and a != '-' and b != '-')
    gaps = align1.count('-') + align2.count('-')
    return mismatches, gaps

# Function to align a single read to all sequences
def align_read_to_sequences(read, sequences, alignment_threshold, gap_open_penalty, gap_extend_penalty):
    temp_counts = {seq: {'count': 0, 'mismatches': 0, 'gaps': 0, 'perfect_matches': 0, 'alignments': []} for seq in sequences}
    align_count = 0
    for seq in sequences:
        align_count += 1
        print("Aligning read: "+ str(align_count))
        # Count perfect matches
        perfect_matches = read.count(seq)
        temp_counts[seq]['perfect_matches'] += perfect_matches
        
        if perfect_matches > 0:
            temp_counts[seq]['count'] += perfect_matches
        else:
            # Perform local alignment using Parasail with custom gap penalties
            result = parasail.sw_trace_striped_16(read, seq, gap_open_penalty, gap_extend_penalty, parasail.blosum62)
            if result.score >= alignment_threshold:
                align1, align2 = result.traceback.query, result.traceback.ref
                mismatches, gaps = calculate_mismatches_and_gaps(align1, align2)
                if mismatches <= 20 and gaps <= 5:  # Filter out alignments with more than 20 mismatches or more than 5 gaps
                    temp_counts[seq]['count'] += 1
                    temp_counts[seq]['mismatches'] += mismatches
                    temp_counts[seq]['gaps'] += gaps
                    temp_counts[seq]['alignments'].append((align1, align2, result.score))
    return temp_counts

# Function to count occurrences of each sequence from the DataFrame in read_list
def count_occurrences(df, read_list, alignment_threshold=20, gap_open_penalty=10, gap_extend_penalty=1, num_threads=4):
    df['Processed_oligo'] = df['oligo'].str.upper().str[18:]
    df['Count'] = 0
    df['Mismatches'] = 0
    df['Gaps'] = 0
    df['Perfect_Matches'] = 0  # Add a new column for perfect matches

    sequences = df['Processed_oligo'].tolist()
    temp_counts = {seq: {'count': 0, 'mismatches': 0, 'gaps': 0, 'perfect_matches': 0, 'alignments': []} for seq in sequences}

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_read = {executor.submit(align_read_to_sequences, read, sequences, alignment_threshold, gap_open_penalty, gap_extend_penalty): read for read in read_list}
        for future in as_completed(future_to_read):
            result = future.result()
            for seq in result:
                temp_counts[seq]['count'] += result[seq]['count']
                temp_counts[seq]['mismatches'] += result[seq]['mismatches']
                temp_counts[seq]['gaps'] += result[seq]['gaps']
                temp_counts[seq]['perfect_matches'] += result[seq]['perfect_matches']
                temp_counts[seq]['alignments'].extend(result[seq]['alignments'])

    alignments_data = []
    read_count = 0
    for seq, stats in temp_counts.items():
        read_count += 1
        print("Read no: " + str(read_count))
        count = stats['count']
        if count > 0:
            mismatches = stats['mismatches'] // count  # average mismatches
            gaps = stats['gaps'] // count  # average gaps
            df.loc[df['Processed_oligo'] == seq, ['Count', 'Mismatches', 'Gaps', 'Perfect_Matches']] = [count, mismatches, gaps, stats['perfect_matches']]
            for alignment in stats['alignments']:
                align1, align2, score = alignment
                alignments_data.append([seq, align1, align2, score])

    df_filtered = df[df['Count'] > 1][['Processed_oligo', 'Count', 'Mismatches', 'Gaps', 'Perfect_Matches']]
    df_filtered.rename(columns={'Processed_oligo': 'Sequence'}, inplace=True)

    # Create a DataFrame for alignments
    alignments_df = pd.DataFrame(alignments_data, columns=['Sequence', 'Alignment1', 'Alignment2', 'Score'])

    return df_filtered, alignments_df

# Function to write alignment details to a text file
def write_alignments_to_text(file_path, alignments_df):
    with open(file_path, 'w') as file:
        for index, row in alignments_df.iterrows():
            file.write(f"Sequence: {row['Sequence']}\n")
            file.write(f"Alignment1: {row['Alignment1']}\n")
            file.write(f"Alignment2: {row['Alignment2']}\n")
            file.write(f"Score: {row['Score']}\n")
            # If mismatches and gaps were calculated, include them
            mismatches, gaps = calculate_mismatches_and_gaps(row['Alignment1'], row['Alignment2'])
            file.write(f"Mismatches: {mismatches}\n")
            file.write(f"Gaps: {gaps}\n")
            file.write("\n")

# Read the oligo sequences from the Excel file
excel_file = '../oligo_excel_files/final_ts-library_02062020.xlsx'
df = pd.read_excel(excel_file)

# Read reads from the second file (nanopore reads in FASTQ format)
read_file = "argR/arg_test_new_kit/pass/barcode01/barcode01.fastq"
reads = read_fastq(read_file)

# Count occurrences
counts_df, alignments_df = count_occurrences(df, reads, alignment_threshold=20, gap_open_penalty=20, gap_extend_penalty=5, num_threads=8)

# Print the results
print(counts_df)
print(alignments_df)

# Save the results to Excel and text files
output_counts_file = "sequence_counts_barcode1.xlsx"
output_alignments_file = "sequence_alignments_barcode1.txt"
counts_df.to_excel(output_counts_file, index=False)
write_alignments_to_text(output_alignments_file, alignments_df)
