# Data Processing
Due to the data limit of 200 MB of Streamlit, we recommend that the processing of the sequencing reads is done locally.
This is one possible way to process the data. Feel free to use your own scripts and tools if you prefer.  
Details can also be found in the method section of the publication.

### 1.  Prepare all relevant files

Besides your sequencing files, the **reference sgRNA-insert pair table and fasta file** is necessary. If you use the web application the fasta file is generated automatically
together with the sgRNA-insert list. Otherwise the Python script *generate_reference_file.py* in the sgRNA-insert pairs design directory  can be used. If you used Nanopore sequencing to generate your sequencing reads, we recommend that the fastq read files for each barcode are merged into one file. 

## Trimming and filtering using Cutadapt 