# A repository-scale workflow for linking bacterial genetic variation to phenotypes
This repository contains relevant code and scripts for the publication: **A repository-scale workflow for linking bacterial genetic variation to phenotypes**. 
The workflow consists of computational and laboratory parts. In this repisotory we provide
all relevant information for the computational parts:
1. Database mining for amino acid mutations
2. Design of sgRNA-insert pairs
3. Data processing and visualization

## Database mining for amino acid mutations
The first step of this workflow is to mine genomes from databases for amino acid mutations. In this study we used the [NCBI Pathogen Detection database](https://www.ncbi.nlm.nih.gov/pathogens/). If you want to use other databases it is important that you obtain genome assembly files (.gbff) in the end. All the downstream steps are based on these files.

### Retrieve genome assembly files
A file containing target isolates is retrieved from the database. Using identifiers from this file and the information from the NCBI ftp site, gene assembly files are downloaded.

### Protein accessions and sequences
Here, protein accessions for target genes are retrieved from the genome assembly files and saved into one file. In the next step these accessions are used to download protein fasta sequences and are saved into a file. For each gene one file is generated containing the available protein sequences from the previously obtained genome assembly files.

### Sequence filtering
As most database are not curated we recommend a filtering step to remove unwanted protein sequences. This can be done by taking the length of a reference protein so that sequences which are too long or too short are removed.

###


## Designing sgRNA-insert pairs
The design of sgRNA-insert pairs can be performed using the web application or the original python scripts. The web appliation is more user friendly, as no prior bioinformatic knowledge and 
installations are neccessary. You can find the web application *here*. All instruction on how to use the individual tabs and functions can be found on the website.

### Overview of the functions in the web application

| Feature                                             | Input|
|-----------------------------------------------------| --------|
| Design sgRNA-insert pairs for targeted aa mutations | List of aa mutation, genome file (.gb)  |
| Perform mutagenesis on a protein sequence           | Protein sequence, gene name|
| Off-target finder for potential binding sites       | List of base pairing regions, genome file (.gb)|
| Visualization of read count tables                  | Readcount table, list of sgRNA-insert pairs  |

The following functions are optional features with the intention of improving the workflow.

### Mutagenesis on a protein sequence
This function allows the mutagenesis of a single protein sequence. Each amino acid in the sequence is mutated to all other amino acids. The output table can 
be used as input for the sgRNA-insert pair design.

### Off-target finder for potential binding sites
We recommend using this function to find the most suited sgRNA-insert pair for specific mutations. Especially if you want only one sgRNA-insert pair per mutation The design tab in the web application provides a table with all protospacers. This table can be used as input to find potentail off-targets. The application finds all regions in the genome with up to four mismatches and provides the original base pairing region, the position in the genome, the off-target sequence, and the number of found mismatches.
#### Note
We recommed to run this only for a few base pairing regions. If you have a lot of them the local python version is more suited, as the computational time can get quite high.

### Visualization of read count tables
The visualization tab allows to gain a first look into the sequenced reads, after experimental procedures and data proccessing is performed. More details to the proccessing of the sequencing data can be found below. 
This interactive tab allows users to choose individual columns to visualize. Summaries, read count distribution, and replicate analysis can be performed. 


#### Note
All relevant python scripts are also available in the **Design sgRNA-insert pairs** folder. You can clone this repisotory if you prefer to run the individual functions locally on you computer.

## Data processing
After sequencing is performed, the resulting fastq files should be processed. Here is a recommended workflow we developed. If you prefer other tools and methods you are free to use them. This part needs to be done locally as Stremlits data limit of 200 MB will not be enough to process large sets of sequencing data.
 ### 1. Preprocessing and preparations
1. Nanopore sequencing: If nanopore sequencing was used, we recommed concatinating the sequencing files of each barcode into one file. 
2. Illumina sequencing: Here the paired end reads need to be merged. Tools such as *FLASh* can be utilized to perform this.

If you use the web application you will get a file containing all reference sgRNA-insert pairs in a fasta file. This file is important in the later steps of the data processing.

### 2. Trimming and filtering of sequencing reads using cutadapt
During the experimental procedure primers are added before sequencing. These primers need to be removed before the alignment of the reads can be performed. If the sub-library spacer is not utilized or needed, we recommend trimming that sequence as well. Cutadapt can also be used to filter short reads for higher quality reads. Detailed commands can be found in the method section of the publication as well as in the **Data Processing** folder.

### 3. Aligning sequenced reads with minimap2
After trimming and filtering, the sequenced reads are aligned to the earlier mentioned fasta file containing the  refernece sgRNA-insert pairs. We decided to use minimap2, but you are free to use other available tools if you want. The resulting alignment file can be used to create a read count table for downstream data analysis and visualization.

### 4. Mismatch filtering 
Mismatch filtering is recommended so that only high quality reads are retained for the final read count table. The python script takes the aligned files and the generated sgRNA- insert pairs as input and generates a read count table assigned to each sgRNA-insert, a detailed description of the filtered reads as well as a filtered alignment file. Some parameters for the filtering steps can be adjusted in the script if needed. Detailed descriptions can be found in the publication as well as in the Data Proccessing folder.

### Most important programs and versions

| Name   | Version      |
|--------|------------  |
|Cutadapt|4.9           |
|Minimap2| 2.28-r1209   |
|Python  |3.10.4        |
|Streamlit|1.30.0       | 








