
from io import BytesIO
import os
import sys
import base64
import streamlit as st
# Insert the parent directory into the system path
sys.path.insert(1, os.path.realpath(os.path.pardir))

# Try to import the mutagenesis module
try:
    from mutagenesis import mutagenesis
except ImportError as e:
    st.error(f"Error importing mutagenesis module: {e}")
    st.stop()

# Streamlit app layout
st.set_page_config(page_title="Mutagenesis")

st.title("Mutagenesis")
with st.expander(" 🗒️ Detailed Description"):
    st.markdown(
        "This section allows you to perform amino acid mutagenesis on a protein of your choosing. \
        You need to provide the gene name and the protein sequence. The function will generate a \
        table which can be used to design sgRNAs and inserts in the Design sgRNAs section."
    )
output = BytesIO()


text = st.text_input("Type the gene name here")

text2 = st.text_input("Paste the protein sequence here", key="sequence")

if st.button('Perform mutagenesis'):
    if not text or not text2:
        st.error("Both gene name and protein sequence are required!")
    else:
        try:
            # Call the mutagenesis function and store the result in session state
            st.session_state.mutagenesis_df = mutagenesis(text, text2)
            # Check if the dataframe is correctly created
            if st.session_state.mutagenesis_df is not None:
                st.write("### First 5 rows of the generated data:")
                st.write(st.session_state.mutagenesis_df.head(5))
            else:
                st.error("No data returned from the mutagenesis function.")
        except ValueError as e:
            st.error(f"ValueError generating mutagenesis: {e}")
        except TypeError as e:
            st.error(f"TypeError generating mutagenesis: {e}")
        except KeyError as e:
            st.error(f"KeyError generating mutagenesis: {e}")
    TEMP_FILE_PATH = "output_mutagenesis.csv"
    st.session_state.mutagenesis_df.to_csv(TEMP_FILE_PATH, index=False)
    # Set up download button
    with open(TEMP_FILE_PATH, "rb") as file:
        file_content = file.read()
        file_encoded = base64.b64encode(file_content).decode('utf-8')
        download_button = f'<a href="data:text/csv;base64,{file_encoded}" \
        download="output_mutagenesis.csv">Download data</a>'
        st.markdown(download_button, unsafe_allow_html=True)
# Add button to clear the generated table
if st.button('Clear Table'):
    st.session_state.mutagenesis_df = None
    st.write("Table cleared.")
