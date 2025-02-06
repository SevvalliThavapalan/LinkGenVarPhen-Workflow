# CRISPRFlow
This repository contains relevant code and scripts for the publication: **CRISPRFlow: A CRISPR-assisted recombineering workFlow for high throughput genome editing in bacteria**. 
The workflow consists of computational and laboratory parts. Here you can find 
all relevant information for the computational parts: 
1. Design of sgRNA-insert pairs
2. Data processing and visualization


## Designing sgRNA-insert pairs
The design of sgRNA-insert pairs can be performed using the CRISPRFlow web application or the original Python scripts. The web appliation is more user firendly, as no prior bioinformatic knowledge and 
installations are neccessary. You can find the web application *here*. All instruction on how to use the individual tabs and functions can be found on the website.

### Overview of the functions in the web application

| Feature                                             | Input|
|-----------------------------------------------------| --------|
| Design sgRNA-insert pairs for targeted aa mutations | List of aa mutation, genome file (.gb)  |
| Perform mutagenesis on a protein sequence           | Protein sequence, gene name|
| Off-target finder for potential binding sites       | List of protospacers, genome file (.gb)|
| Visualization of read count tables                  | Readcount table  |

The following functions are optional features with the intention of improving the workflow.

### Mutagenesis on a protein sequence
This function allows the mutagenesis of a single protein sequence. Each amino acid in the sequence is mutated to all other amino acids. The output table can 
be used as input for the sgRNA-insert pair design.

### Off- target finder for potential binding sites
We recommend using this function to find the most suited sgRNA-insert pair for specific mutations. The design tab in the web application provides a table with all protospacers. This 
table can be used as input to find potentail off-targets. The application finds all regions in the genome with up to four mismatches and results the original base pairing region, the position 
in the genome, the off-target sequence, and the number of found mismatches.

### Visualization of read count tables
The visualization tab allows to gain a first look into the sequenced reads, after experimental procedures and data proccessing is performed. More details to the proccessing of the sequencing data can be found below. 
This interactive tab allows users to choose individual columns to visualize. Summaries, read count distribution, and replicate analysis can be performed. 


#### Note

All relevant python scripts are also available in the **XXX** folder, if you prefer to run the individual functions locally on you computer.

## Data processing
After sequencing is performed, the resulting fastq files should be processed. Here is a recommended workflow we developed. If you prefer other tools and methods you are free to use them.  
 ### 1. Preprocessing and preparations
1. Nanopore sequencing: If nanopore sequencing was used, we recommed concatinating the sequencing files of each barcode into one file. 
2. Illumina sequencing: Here the paired end reads need to be merged. Tools such as *FLASH* can be utilized to perform this.

If you use the web application you will get a file containing all reference sgRNA-insert pairs in a fasta file. This file is important in the later steps of the data processing.

### 2. Trimming and filtering of sequencing reads using cutadapt
During the experimental procedure primers are added before sequencing. These primers need to be removed before the alignment of the reads can be done. If the sub-library spacer is not utilized or needed, we recommend trimming that sequence as well. Cutadapt can also be used to filter short reads for higher quality reads. Detailed commands can be found in the method section of the publication as well as in the Data Processing folder.

### 3. Aligning sequenced reads with minimap2
After trimming and filtering, the sequenced reads are aligned to the earlier mentioned fasta file containing the  refernece sgRNA-insert pairs. We decided to use minimap2, but you are free to use other available tools if you want. The resulting alignment file can be used to create a read count table for downstream data analysis and visualization.

### 4. Mismatch filtering 
Mismatch filtering is recommended so that only high quality reads are retained for the final read count table. The Python script takes the aligned files and the generated sgRNA- insert pair as input and generates a read count table assigned to each sgRNA-insert, a detailed description of the filtered reads as well as a filtered alignment file. Some parameters for the filtering steps can be adjusted in the script if needed. Detailed descriptions can be found in the publication as well as in the Data Proccessing folder.

### Programs and versions
| Name   | Version|
|--------|              |
|Cutadapt|4.9           |
|Minimap2| 2.28-r1209   |
|Python  |3.10.4        |
|Samtools|1.10          |
Streamlit|1.30.0        | 








