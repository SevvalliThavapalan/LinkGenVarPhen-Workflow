# Data Processing
Due to the data limit of 200 MB of Streamlit, we recommend that the processing of the sequencing reads is done locally.
This one possible way to process the data. Details can also be found in the method section of the publication.

1.  Prepare all relevant files

Besides your sequencing files, the **reference sgRNA-insert pair table and fasta file** is necessary. If you use the web application the fasta file is generated automatically
together with the sgRNA-insert list. Otherwise the Python script *generate_reference_fasta.py* can be utilized. If you used Nanopore sequencing to generate your reads, we 
recommend that the fastq read files for each barcode are merged into one file. 