# CRISPRFlow
This repository contains relevant code and scripts for the publication: **CRISPRFlow A CRISPR-assisted recombineering workFlow for high throughput genome editing in bacteria**. 
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

All relevant python scripts are also available in the **XXX** folder, if you prefer to run all the functions locally on you computer. 
 

