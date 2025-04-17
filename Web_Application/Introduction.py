"""
Introduction page 
"""
import streamlit as st


st.set_page_config(
    page_title="Introduction"
)

st.title("Introduction")
st.sidebar.success("Menu")

st.markdown("""

This web application was developed to translate a list of amino acid mutations into DNA oligomers with sgRNA-insert pairs for CRISPR assisited recombineering. It is part of the project "A repository-scale workflow for linking bacterial 
            genetic variation to phenotypes". The aim of the workflow is to systematically identify, introduce and analyse effects of individual mutations. Purpose of this application is the second step of the workflow, enabling the 
            automated design of sgRNA-insert pairs. The design principles are based on [Garst et al.](https://www.nature.com/articles/nbt.3718) and the adapted version of another study by our [group](https://www.embopress.org/doi/full/10.15252/msb.202311596).
""")

st.markdown("## Functions of the web application")
st.markdown(
    """
    - **Design sgRNA and insert sequences** for a list of amino acid mutations.
    - **Mutagenesis** of a single protein sequence. The resulting table \
    can be used to design sgRNAs and inserts.
    - **Off-target finder** for a list of base pairing regions. \
    They are compared to the target genome to find potential binding sites.
    - The **Visualization** tab can be used to reintroduce read counting tables. \
    The purpose is to provide a first insight into the results after performing experiments. 
""")


st.markdown("### Limitations")
st.markdown(
    """
    - The web application has a 200 MB data limit. Larger datasets might lead to \
    issues such as long runtimes or crushing the server.
    - This part of CRISPRFlow only allows to generate and design sgRNA and insert \
    pools. Sequenced data to investigate the library composition can not be processed here. \
    But there are scripts available on Github, which are easy to follow.
    """
)

st.markdown("### Contribute and Follow Us")

st.markdown("""
- Interested in contributing? Check out our [GitHub personal page](https://github.com/SevvalliThavapalan/LinkGenVarPhen-Workflow/tree/main).
- For more about our work, visit our [homepage](https://www.linkmetabolism.com/).
- Follow us on [X](https://twitter.com/LinkLabs) for the latest updates.
""")
