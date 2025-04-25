"""
File to design sgRNAs and inserts based on a list of mutations and a genome file.
"""
import zipfile
import os
import base64
import sys
import io
from io import BytesIO
import streamlit as st
import pandas as pd
from Bio import SeqIO
sys.path.insert(1, os.path.realpath(os.path.pardir))
from src.oligos import *
from src.filter_by_pam import *
from src.filter_by_codon import *
from src.generate_reference_files import *




# Function to read Excel file
def read_excel_file(uploaded_file):
    """Reads an Excel file and returns a DataFrame."""

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, sep="[,;]", engine="python")
        else:
            df = pd.read_excel(uploaded_file)
        return df
    else:
        st.write("Upload an Excel file containing the mutations to get started.")
        return None


EXAMPLE_TABLE = """
| gene | mutation | position |
|:---------:|:--------:|:--------:|
| aaeA      | T5S      | 5        |
| aaeA      | L102Q    | 102      |
| aaeA      | K189E    | 189      |\
"""

# Streamlit app layout
st.set_page_config(page_title="Design sgRNAs and Inserts")
output = BytesIO()
st.title("sgRNA and Insert Design")
with st.expander(" 🧬 Detailed Description"):
    st.markdown(
        "This is the main function of the web application. By providing a \
        list of potential amino acid mutations as well as a genome you can generate "
        "a list of sgRNA -insert pairs. If you do not want to use all sgRNAs and "
        "inserts you can filter the generated table by PAMs or codons. The generated "
        "files can be downloaded for further use."
    )
st.markdown(
    " #### Example Input")
st.markdown("The following table shows an example input table. The table should  "
            "contain three columns named : gene, mutation and position.\
            It is important that the input table includes these three columns in this exact format.\
            **Otherwise the function will not work properly.** \
            Also make sure that the genes in the input table are present \
            in the target genome file.")
st.markdown(EXAMPLE_TABLE,unsafe_allow_html=True)
st.subheader("Choose your input genome:")

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'oligos_df' not in st.session_state:
    st.session_state.oligos_df = None



genome_choice = st.radio("Choose an option:",
                         ("Upload your own genome file", "Select from provided genomes"))

if genome_choice == "Upload your own genome file":
    genome_file = st.file_uploader("Upload genome", type=["gb"])
    if genome_file is not None:
        st.write("Genome file uploaded successfully!")
        # Parse the uploaded genome file
        try:
            record = SeqIO.read(genome_file, "genbank")
            st.write("Genome Information:")
            st.write(f"Name: {record.name}")
            st.write(f"Description: {record.description}")
        except (ValueError, IOError) as e:
            st.error(f"An error occurred while parsing the genome file: {e}")
else:
    selected_genome = st.selectbox("Select a provided genome:",
                                   ["E. coli BW25113", "E. coli K-12 substr. MG1655",
                                    "S. aureus USA 300",
                                    "P. aeruginosa PA01", "P. aeruginosa PA14"])
    # Load the selected provided genome
    if selected_genome == "E. coli BW25113":
        genome_file = "Web_Application/data/BW25113.gb"
    elif selected_genome == "E. coli K-12 substr. MG1655":
        genome_file = "Web_Application/data/MG1655.gb"
    elif selected_genome == "S. aureus USA 300":
        genome_file= "Web_Application/data/saureus_USA300_FPR3757.gb"
    elif selected_genome == "P. aeruginosa PA01":
        genome_file= "Web_Application/data/pa01.gb"
    elif selected_genome == "P. aeruginosa PA14":
        genome_file= "Web_Application/data/pa14.gb"
    # Parse the uploaded genome file
    try:
        record = SeqIO.read(genome_file, "genbank")
        st.write("Genome information:")
        st.write(f"Name: {record.name}")
        st.write(f"Description: {record.description}")

    except (ValueError, IOError) as e:
        st.error(f"An error occurred while parsing the genome file: {e}")

st.subheader("Please upload your list of mutations:")
st.write("Upload your file below:")
uploaded_file = st.file_uploader("Upload your file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    st.session_state.df = read_excel_file(uploaded_file)
    # Read the uploaded file directly into DataFrame

# Display the first 5 rows of the uploaded Excel file
if st.session_state.get('df') is not None:
    st.write("### First 5 rows of the uploaded file:")
    st.write(st.session_state.df.head(5))

    # Generate oligos if the button is clicked
    if st.button('Generate oligos'):
        st.write('Processing...')
        st.session_state.oligos_df, st.session_state.missing_genes = generate_oligos(
            st.session_state.df, genome_file)
        st.write("Done")
        if len(st.session_state.missing_genes) > 0 :
            st.write("These genes could not be found in the genome file:")
            for value in st.session_state.missing_genes:
                st.write(value)
            #st.write(st.session_state.missing_genes)
        st.write("### Results:")
        st.write(st.session_state.oligos_df)
        st.write("Please check double check the resulting table for any errors before ordering the DNA oligomers. If you encounter any errors please contact us.")

        #set up fasta file and protospacer list
        fasta_output_path = "reference_file.fasta"

        # Create the FASTA file and protospacer DataFrame
        (st.session_state.reference_file,
         st.session_state.proto_file) = create_fasta_and_protospacer_file(
            st.session_state.oligos_df,fasta_output_path)

        # Write DataFrame to temporary Excel file
        temp_file_path = "sgRNA_insert_list.csv"
        st.session_state.oligos_df.to_csv(temp_file_path, index=False)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Save DataFrame to Excel in memory
            csv_buffer = io.BytesIO()
            st.session_state.oligos_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            zip_file.writestr("sgRNA_insert_list.csv", csv_buffer.read())
       # Add reference file to the ZIP
            with open(st.session_state.reference_file, "rb") as ref_file:
                zip_file.writestr("reference_file.fasta", ref_file.read())
        # Add protospacer DataFrame to the ZIP
            proto_buffer = io.BytesIO()
            st.session_state.proto_file.to_csv(proto_buffer, index=False)
            proto_buffer.seek(0)
            zip_file.writestr("bpregion_file.csv", proto_buffer.read())
        # Reset buffer position to the beginning
        zip_buffer.seek(0)

        # Encode ZIP file for download
        zip_file_content = zip_buffer.read()
        zip_file_encoded = base64.b64encode(zip_file_content).decode('utf-8')
        download_button = f'<a href="data:application/zip;base64,{zip_file_encoded}" download="results.zip">Download Results as ZIP</a>'
        st.markdown(download_button, unsafe_allow_html=True)

# Show filtering options only after oligos are generated
    if st.session_state.get('oligos_df') is not None:
    # Initialize session state for filtered data and thresholds
        if 'filtered_df' not in st.session_state:
            st.session_state.filtered_df = st.session_state.oligos_df
        if 'filtered_df_codon' not in st.session_state:
            st.session_state.filtered_df_codon = st.session_state.oligos_df
        if 'filter_threshold_pam' not in st.session_state:
            st.session_state.filter_threshold_pam = 1
        if 'filter_threshold_codon' not in st.session_state:
            st.session_state.filter_threshold_codon = 1

    # Display tabs for filtering options
        tabs = st.tabs(['Filter by PAMs', 'Filter by Codons'])

    # Tab for filtering by PAMs
        with tabs[0]:
            st.header('Filter by PAMs')

        # Get user input for PAM threshold
            filter_threshold_pam = st.number_input(
                'Enter a numeric threshold for filtering PAMs:',
                min_value=1,
                max_value=100,
                value=st.session_state.filter_threshold_pam,  # Load previous value
                step=1,
                key= "pam"
            )

        # Apply filter only if threshold changes
            if st.button('Filter by PAM'):
                if filter_threshold_pam != st.session_state.filter_threshold_pam:
                    st.session_state.filter_threshold_pam = filter_threshold_pam
                    st.session_state.filtered_df = filter_pam(st.session_state.oligos_df,
                                                              filter_threshold_pam)

        # Display filtered data
                if st.session_state.filtered_df.empty:
                    st.write("No rows match the filter criteria.")
                else:
                    st.write("First five rows of the filtered table:")
                    st.write(st.session_state.filtered_df.head(5))
                    temp_file_path = "output_filtered_by_pam.csv"
                    st.session_state.filtered_df.to_csv(temp_file_path, index=False)
            # Set up download button
                    with open(temp_file_path, "rb") as file:
                        file_content = file.read()
                        file_encoded = base64.b64encode(file_content).decode('utf-8')
                        download_button = f'<a href="data:text/csv;base64,{file_encoded}" download="output_filtered_by_pam.csv">Download data</a>'
                        st.markdown(download_button, unsafe_allow_html=True)

    # Tab for filtering by Codons
        with tabs[1]:
            st.header('Filter by Codons')

        # Get user input for Codon threshold
            filter_threshold_codon = st.number_input(
                'Enter a numeric threshold for filtering by Codons:',
                min_value=1,
                max_value=100,
                value=st.session_state.filter_threshold_codon,  # Load previous value
                step=1,
                key = "codon"
            )

        # Apply filter only if threshold changes
            if st.button('Filter by Codon'):
                if filter_threshold_codon != st.session_state.filter_threshold_codon:
                    st.session_state.filter_threshold_codon = filter_threshold_codon
                    st.session_state.filtered_df_codon = filter_codon(st.session_state.oligos_df,
                                                                      filter_threshold_codon)

        # Display filtered data
                if st.session_state.filtered_df_codon.empty:
                    st.write("No rows match the filter criteria.")
                else:
                    st.write("First five rows of the filtered table:")
                    st.write(st.session_state.filtered_df_codon.head(5))
                    temp_file_path = "output_filtered_by_codon.csv"
                    st.session_state.filtered_df_codon.to_csv(temp_file_path, index=False)
                # Set up download button
                    with open(temp_file_path, "rb") as file:
                        file_content = file.read()
                        file_encoded = base64.b64encode(file_content).decode('utf-8')
                        download_button = f'<a href="data:text/csv;base64,{file_encoded}" download="output_filtered_by_codon.csv">Download data</a>'
                        st.markdown(download_button, unsafe_allow_html=True)
# Add button to clear the generated table
    if st.button('Clear Tables'):
        st.session_state.df = None
        st.session_state.oligos_df = None
        st.write("Tables cleared.")
# Add button to clear the filtered tables
    if st.button('Clear Filtered Tables'):
        st.session_state.filtered_df = st.session_state.oligos_df
        st.session_state.filtered_df_codon = st.session_state.oligos_df
        st.write("Filtered tables cleared.")
