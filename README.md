# A repository-scale workflow for linking bacterial genetic variation to phenotypes
This repository contains relevant code and scripts for the publication: **A repository-scale workflow for linking bacterial genetic variation to phenotypes**. 
The workflow consists of computational and laboratory parts. In this repisotory we provide
all relevant information for the computational parts:
1. Database mining for amino acid mutations
2. Design of sgRNA-insert pairs
3. Data processing and visualisation

More details for each step can be found in the indivdual folders.

## Database mining for amino acid mutations
The first step of this workflow is to mine genomes from databases for amino acid mutations. In this study we used the [NCBI Pathogen Detection database](https://www.ncbi.nlm.nih.gov/pathogens/). If you want to use other databases it is important that you obtain genome assembly files (.gbff) in the end. All the downstream steps are based on these files.

### Retrieve genome assembly files
A file containing target isolates is retrieved from the database. Using identifiers from this file and the information from the NCBI ftp site, gene assembly files are downloaded.

### Protein accessions and sequences
Here, protein accessions for target genes are retrieved from the genome assembly files and saved into one file. In the next step these accessions are used to download protein fasta sequences and are saved into a file. For each gene one file is generated containing the available protein sequences from the previously obtained genome assembly files.

### Sequence filtering
As most database are not curated we recommend a filtering step to remove unwanted protein sequences. This can be done by taking the length of a reference protein so that sequences which are too long or too short are removed.

### Multiple sequence alignment
After adding the sequence of a reference protein of your choosing, multiple sequence alignment (MSA) using muscle can be performed. The resulting file can be used to retrieve amino acid mutations compared to the reference and their frequency.

### Extract list of mutations
After generating the MSA, mutations can be extracted by providing the accession of the reference protein. We recommend checking the generated list of mutations. If there are too many gaps in the alignment, this indicates that there is still a wrong protein sequence in the protein fasta file. Another option is to inspect the MSA by using for example the [Alignmentviewer](https://alignmentviewer.org/).



## Designing sgRNA-insert pairs
The design of sgRNA-insert pairs can be performed using the web application or the original python scripts. The web appliation is more user friendly, as no prior bioinformatic knowledge and 
installations are neccessary. You can find the web application [here](https://linkgenvarphen-workflow-fmtmodttijhjuucxbvr9z7.streamlit.app/). All instruction on how to use the individual tabs and functions can be found on the website.

### Overview of the functions in the web application

| Feature                                             | Input|
|-----------------------------------------------------| --------|
| Design sgRNA-insert pairs for targeted aa mutations | List of aa mutation, genome file (.gb)  |
| Perform mutagenesis on a protein sequence           | Protein sequence, gene name|
| Off-target finder for potential binding sites       | List of base pairing regions, genome file (.gb)|
| Visualisation of read count tables                  | Readcount table, list of sgRNA-insert pairs  |

The following functions are optional features with the intention of improving the workflow.

### Mutagenesis on a protein sequence
This function allows the mutagenesis of a single protein sequence. Each amino acid in the sequence is mutated to all other amino acids. The output table can 
be used as input for the sgRNA-insert pair design.

### Off-target finder for potential binding sites
We recommend using this function to find the most suited sgRNA-insert pair for specific mutations. Especially if you want only one sgRNA-insert pair per mutation The design tab in the web application provides a table with all protospacers. This table can be used as input to find potentail off-targets. The application finds all regions in the genome with up to four mismatches and provides the original base pairing region, the position in the genome, the off-target sequence, and the number of found mismatches.
#### Note
We recommed to run this only for a few base pairing regions. If you have a lot of them the local python version is more suited, as the computational time can get quite high.

### Visualisation of read count tables
The visualisation tab allows to gain a first look into the sequenced reads, after experimental procedures and data proccessing is performed. More details to the proccessing of the sequencing data can be found below. 
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
During the experimental procedure primers are added before sequencing. These primers need to be removed before the alignment of the reads can be performed. If the sub-library spacer is not utilized or needed, we recommend trimming that sequence as well. Cutadapt can also be used to filter reads to get a high quality data set. Detailed commands can be found in the method section of the publication as well as in the **Data Processing** folder.

### 3. Finding perfect matches
After trimming and filtering is performed, reads are matched against the initial list of sgRNA-insert pairs to find perfect matches. A read count table is generated counting the number of matches for each reference.
The previously generated reference file is taken as input to run the  python script.

### Feedback
We appreciate any feedback or suggestions you can provide. The initial versions of the computational workflows was developed by one person. and even though we tried to think of every potential issue and bug there
is always the possibility that we missed something. If you have any feedback or run into any issues, feel free to open an issue on our GitHub repository.








