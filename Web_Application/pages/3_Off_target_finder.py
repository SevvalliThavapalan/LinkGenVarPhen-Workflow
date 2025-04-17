"""
This script is used to find potential off targets for designed base pairing regions.
They are checked against the whole genome of your target organism
and all sequences with upto 4 mismatches are reported back.
"""
import os
import sys
import base64
import io
from io import BytesIO
from Bio import SeqIO
import pandas as pd
import streamlit as st

from src.off_target_finder import off_target

def read_file(input_file):
    """
    Read the uploaded file and return a DataFrame
    :param file: Uploaded file
    :return: DataFrame
    """
    if input_file is not None:
        file_extension = input_file.name.split('.')[-1].lower()
        if file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(io.BytesIO(input_file.read()))
        elif file_extension == 'csv':
            df = pd.read_csv(io.StringIO(input_file.getvalue().decode("utf-8")))
        elif file_extension == 'tsv':
            df = pd.read_csv(io.StringIO(input_file.getvalue().decode("utf-8")), sep='\t')
        else:
            st.write("Unsupported file type. Please upload an Excel, CSV, or TSV file.")
            return None
        return df
    else:
        st.write("Upload an Excel, CSV, or TSV file containing the protospacers to get started.")
        return None

# Streamlit app layout
st.set_page_config(page_title="Off targets")
output = BytesIO()

st.title("Off target finder")
with st.expander(" 🔍 Detailed Description"):
    st.markdown(
        "This function can be used to find potential off targets for designed base \
        pairing regions. \
        they are checked against the whole genome of your target organism and all\
        sequences with upto 4 mismatches are reported back. As each base pairing region is \
        checked against the whole genome, this function can take a while to run. We recommend \
        to run this function with a small number of base pairing regions at a time."
    )


st.subheader("Choose your input genome:")

genome_choice = st.radio("Choose an option:",
                         ("Upload your own genome file", "Select from provided genomes"))

if genome_choice == "Upload your own genome file":
    GENOME_FILE = st.file_uploader("Upload genome", type=["gb"])
    if GENOME_FILE is not None:
        st.write("Genome file uploaded successfully!")

        # Parse the uploaded genome file
        try:
            record = SeqIO.read(GENOME_FILE, "genbank")
            st.write("Genome Information:")
            st.write(f"Name: {record.name}")
            st.write(f"Description: {record.description}")
        except (ValueError, IOError) as e:
            st.error(f"An error occurred while parsing the genome file: {e}")
else:
    selected_genome = st.selectbox("Select a provided genome:",
                                   ["E. coli BW25113", "E. coli K-12 substr. MG1655",
                                    "S. aureus USA 300", "P. aeruginosa PA01",
                                    "P. aeruginosa PA14"])
    # Load the selected provided genome
    if selected_genome == "E. coli BW25113":
        GENOME_FILE = "./Web_Application/data/BW25113.gb'"

    elif selected_genome == "E. coli K-12 substr. MG1655":
        GENOME_FILE = "data/MG1655.gb"

    elif selected_genome == "S. aureus USA 300":
        GENOME_FILE= "data/saureus_USA300_FPR3757.gb"

    elif selected_genome == "P. aeruginosa PA01":
        GENOME_FILE= "data/pa01.gb"

    elif selected_genome == "P. aeruginosa PA14":
        GENOME_FILE= "data/pa14.gb"


    # Parse the uploaded genome file
    try:
        record = SeqIO.read(GENOME_FILE, "genbank")
        st.write("Genome information:")
        st.write(f"Name: {record.name}")
        st.write(f"Description: {record.description}")

    except (ValueError, IOError) as e:
        st.error(f"An error occurred while parsing the genome file: {e}")

    st.subheader("Please upload your list of protospacers:")
    st.write("Upload your file containing the base pairing regions file below:")
    uploaded_file = st.file_uploader("Upload Excel, CSV, or TSV File",
                                     type=["xlsx", "xls", "csv", "tsv"])
    if uploaded_file is not None:
        st.session_state.df = read_file(uploaded_file)
        if st.session_state.df is not None:
            st.write("File uploaded successfully!")
            st.write(st.session_state.df.head())
    else:
        st.write("Please upload a file to get started.")

    if st.button('Find off targets:'):
        if st.session_state.df is not None:
            st.write('Processing...')

         # Generate oligos
            st.session_state.offtargets_df = off_target(st.session_state.df, GENOME_FILE)
            st.write("Done")
            st.write("### Results:")
            st.write(st.session_state.offtargets_df)
            # Write DataFrame to temporary Excel file
            TEMP_FILE_PATH = "output_offtargets.xlsx"
            st.session_state.offtargets_df.to_excel(TEMP_FILE_PATH, index=False)
         # Set up download button
            with open(TEMP_FILE_PATH, "rb") as file:
                file_content = file.read()
                file_encoded = base64.b64encode(file_content).decode('utf-8')
                download_button = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,\
                {file_encoded}" download="output_offtargets.xlsx">Download data</a>'
                st.markdown(download_button, unsafe_allow_html=True)
