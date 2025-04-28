"""
This script takes a table containing sgRNA-insert pairs
and creates a fasta file containing the insert sequences 
and a csv file containing the protospacer/base pairing regions
"""
def create_fasta_and_protospacer_file(file, fasta_output_file):
    """
    Create a FASTA file and a protospacer file from a table containing sequences.
    """

    # Read Excel file into a pandas DataFrame
    df = file
    protospacer_df = df[['reference','gene', 'aa position', 'mutated aa','child codon',
                          'nt position', 'dist mut pam', 'mutated pam','base pairing region']]

    # Write the FASTA file
    with open(fasta_output_file, 'w', encoding="utf-8") as fasta_file:
        # Iterate over rows in DataFrame
        for index, row in df.iterrows():
            # Extract header information from columns before the sequence column
            #header_info = '_'.join([str(row[col]) for col in df.columns[:2]])
            header_info = f"{row.iloc[0]}"
            # Extract sequence from the 'oligo' column and format it
            sequence = str(row['oligo']).upper()

            # Write header and sequence to FASTA file
            fasta_file.write(f'>{header_info}\n{sequence}\n')

    # Return the file path of the FASTA file and the protospacer DataFrame
    return fasta_output_file, protospacer_df
