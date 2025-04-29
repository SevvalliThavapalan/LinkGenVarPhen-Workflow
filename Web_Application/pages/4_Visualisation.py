"""
This script is used to visualise the read count data from the merged data file.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO




# Set the page configuration
st.set_page_config(page_title="Read Count Visualisation")

# Function title and description
st.title("Read Count Visualisation")
with st.expander(" :bar_chart: Detailed Description"):
    st.markdown(
        "After constructing your library and amplicon sequencing you can \
        reintroduce your read count tables here. Some basic visualisation and \
        statistical analysis can be performed to get a first overview of your data.\
        We recommend to use the merged data file for this analysis.")



# File uploader for the merged data file
st.subheader(" Upload your merged read count file")
uploaded_file = st.file_uploader(
    "Upload a merged file (Excel, CSV, or TSV format).",
    type=["xlsx", "xls", "csv", "tsv"],
)

# Proceed if a file is uploaded
if uploaded_file:
    # Load the uploaded file
    if uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".tsv"):
        df = pd.read_csv(uploaded_file, sep="\t")
    else:
        st.error("Unsupported file format! Please upload an Excel, CSV, or TSV file.")
        st.stop()

    # Display the uploaded dataframe
    st.write("Here is a preview of your uploaded data:")
    st.dataframe(df.head())


    st.subheader("Select read count columns")
    st.write("Select the columns containing read counts for visualisation:")

    # List all columns for selection
    selected_columns = st.multiselect(
        "Available columns:",
        options=df.columns,
        help="Select one or more columns that contain numeric data for visualisation."
    )


    # Save the figure to an in-memory buffer
    buffer = BytesIO()

    # Proceed if at least one column is selected
    if selected_columns:
        # Display summary statistics for the selected columns
        st.write("Summary statistics of selected columns:")
        st.dataframe(df[selected_columns].describe())

        # Generate a histogram for the selected columns
        st.subheader("Read count histogram")
        st.write("The histogram below shows the distribution of the selected counts.")
        # Use Plotly to create interactive histograms
        melted_df = df.melt(value_vars=selected_columns,
                            var_name="Count Column", value_name="Counts")
        # Calculate optimal number of bins for the histogram
        n_bins = int(np.sqrt(len(melted_df)))
        fig = px.histogram(
            melted_df,
            x="Counts",
            color="Count Column",
            nbins=n_bins,
            title="Histogram of Selected Read counts",
            labels={"Counts": "Read Counts", "Count Column": "Columns"},
            opacity=0.7
        )
        fig.update_layout(
            yaxis_title="Frequency",
            bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)


        # Bar plot with aa position on x-axis
        st.subheader("AA position bar plot")
        st.write("The bar plot below shows the selected columns with respect to the AA position.")

        # Ensure the necessary columns exist before proceeding
        if 'gene' in df.columns and 'aa position' in df.columns and 'reference' in df.columns:
            # User selects a gene
            selected_gene = st.selectbox("Select a gene:", df["gene"].unique())

        # Filter dataframe for the selected gene
            filtered_df = df[df["gene"] == selected_gene]

        # Proceed if data is available for the selected gene
            if not filtered_df.empty:

                tabs = st.tabs(selected_columns)

                for tab,col in zip(tabs,selected_columns):
                # Ensure the selected column exists in the filtered dataframe
                    with tab:
                        st.write(f"### {col} - AA position bar plot")

                    # Create a bar plot for the selected column
                        bar_fig = px.bar(
                            filtered_df,
                            x="aa position",
                            y=col,
                            color="reference",  # Coloring by Reference
                            barmode="stack",  # Stacked bars for better visualisation
                            title=f"AA Position vs {col} for {selected_gene}",
                            labels={"aa position": "AA Position", col: col},
                        )

                        # Hide the legend to avoid clutter
                        bar_fig.update_layout(showlegend=False)

                    # Display the plot
                        st.plotly_chart(bar_fig, use_container_width=True)

            else:
                st.warning(f"No data available for the selected gene: {selected_gene}")

        else:
            st.error("Missing required columns: 'gene',\
                     'aa position', or 'reference' in the dataframe.")
             # Comparison between two selected columns
            st.subheader("Compare two selected columns")
            st.write("Select two columns to compare side by side:")

        # Allow user to select two columns
        column_comparison = st.selectbox(
            "Choose the first column for comparison:",
            options=selected_columns,
            help="Select the first column for comparison."
        )

        # Make sure the second column is different from the first one
        second_column_comparison = st.selectbox(
            "Choose the second column for comparison:",
            options=[col for col in selected_columns if col != column_comparison],
            help="Select the second column for comparison."
        )

        # Display the selected columns for comparison
        if column_comparison and second_column_comparison:
            st.write(f"Comparing **{column_comparison}** with **{second_column_comparison}**:")
            comparison_df = df[['aa position', 'reference',
                                column_comparison, second_column_comparison]]

            # Create a parity plot (scatter plot) comparing the two columns
            st.subheader(f"Parity Plot: {column_comparison} vs {second_column_comparison}")

            # Scatter plot for comparison
            scatter_fig = px.scatter(
                comparison_df,
                x=column_comparison,
                y=second_column_comparison,
                title=f"Parity Plot: {column_comparison} vs {second_column_comparison}",
                labels={column_comparison: column_comparison,
                         second_column_comparison: second_column_comparison},
                hover_data={"reference": True}  # Include the 'Reference' column in the hover data
            )

            # Set log scale for both axes
            scatter_fig.update_layout(
                xaxis_type="log",
                yaxis_type="log"
            )
            st.plotly_chart(scatter_fig, use_container_width=True)

        fig.update_layout(autosize=True)

    else:
        st.warning("Please select at least one column to visualise.")

else:
    st.info("Upload a file to begin.")
