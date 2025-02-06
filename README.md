# CRISPRFlow
This repository contains relevant code and scripts for the publication: **CRISPRFlow A CRISPR-assisted recombineering workFlow for high throughput genome editing in bacteria**. 
The workflow consists of computational and laboratory parts. Here you can find 
all relevant information for the computational parts: 
1. Design of sgRNA-insert pairs
2. Data processing and visualization


## Designing sgRNA-insert pairs
The design of sgRNA-insert pairs can be performed using the CRISPRFlow web application or the original Python scripts. The web appliation is more user firendly, as no prior bioinformatic knowledge and 
installations are neccessary.  You can find the web apllication *here*. All instruction on how to use the individual tabs and functions can be found on the website.

### Overview of the functions in the web application

| Feature                                             | Input|
|-----------------------------------------------------| --------|
| Design sgRNA-insert pairs for targeted aa mutations | List of aa mutation, genome file (.gb)  |
| Perform mutagenesis on a protein sequence           | Protein sequence, gene name|
| Off-target finder for potential binding sites       | List of protospacers, genome file (.gb)|
| Visualization for read count tables                 | Readcount table  |



