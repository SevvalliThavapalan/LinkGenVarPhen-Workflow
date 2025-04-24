"""
Introduction page 
"""
import streamlit as st


st.set_page_config(
    page_title="Introduction"
)

st.sidebar.image(
    "https://raw.githubusercontent.com/SevvalliThavapalan/LinkGenVarPhen-Workflow/main/logo/LinkMetabolism_logo.png",use_column_width=True)
st.title("Introduction")

st.markdown("""

This web application was developed to translate a list of amino acid mutations into DNA oligomers with sgRNA-insert pairs for CRISPR assisted recombineering. It is part of the project *"A repository-scale workflow for linking bacterial 
            genetic variation to phenotypes"*. The aim of the workflow is to systematically identify, introduce and analyse effects of individual mutations. Purpose of this web application is the second step of the workflow, enabling the 
            automated design of sgRNA-insert pairs. The design principles are based on [Garst et al.](https://www.nature.com/articles/nbt.3718) and the adapted version of another study by our [group](https://www.embopress.org/doi/full/10.15252/msb.202311596).
""")

st.markdown("## Functions of the web application")
st.markdown(
    """
    - **Design sgRNA-insert pair sequences** for a list of amino acid mutations.
    - **Mutagenesis** of a single protein sequence. The resulting table \
    can be used to design sgRNA-insert pairs.
    - **Off target finder** for a list of base pairing regions. \
    They are compared to the target genome to find potential binding sites.
    - The **Visualisation** tab can be used to reintroduce read counting tables. \
    The purpose is to provide a first insight into the results after performing experiments. 
""")

st.markdown("## Example data")
st.markdown(
"""
You can find example data in the GitHub repository:\
    - For the design, mutagenesis and off target finder, you can use the example data provided in \
    the [example data](https://github.com/SevvalliThavapalan/LinkGenVarPhen-Workflow/tree/main/sgRNA-insert%20pairs%20design/Example_Data).
""")
st.markdown("### Limitations")
st.markdown(
    """
    - The web application has a 200 MB data limit. Larger datasets might lead to \
    issues.
    - This part of the workflow only allows to generate and design sgRNA-insert \
    pools. Sequenced data to investigate the library composition can not be processed here. \
    But there are scripts available on GitHub and can be cloned to perform the processing.
    """
)

st.markdown("### Feedback")
st.markdown("""

We appreciate any feedback or suggestions you can provide. The initial versions of this website was developed by one person, and even though we tried to think of every potential issue and bug there
is always the possibility that we missed something. If you have any feedback or run into any issues, feel free to open an issue on our [GitHub repository](https://github.com/SevvalliThavapalan/LinkGenVarPhen-Workflow/tree/main).
            """
)

st.markdown("### Link Metabolism")
st.markdown("""
- For more about our work, visit our [homepage](https://www.linkmetabolism.com/).
- Our Github [page](https://github.com/LinkMetabolism)
- Follow us on [X](https://twitter.com/LinkLabs).
""")
