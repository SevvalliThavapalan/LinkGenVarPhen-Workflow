# Web Application
Here details about the web application of the workflow can be found. The indivdual scripts which this application is based on can be found in the **sgRNA-insert design* folder.

## Installation

The online version  of the app can be found [here](https://linkgenvarphen-workflow-fmtmodttijhjuucxbvr9z7.streamlit.app/).

#### Local installation
- Clone the repisotory
- Install all packages from the requirements.txt file
```
pip install -r requirements.txt
```
- To start the app locally on your terminal run
```
streamlit run Introduction.py
```
#### Funcions of the web application
| Feature                                             | Input|
|-----------------------------------------------------| --------|
| Design sgRNA-insert pairs for targeted aa mutations | List of aa mutation, genome file (.gb)  |
| Perform mutagenesis on a protein sequence           | Protein sequence, gene name|
| Off-target finder for potential binding sites       | List of base pairing regions, genome file (.gb)|
| Visualization of read count tables                  | Readcount table, list of sgRNA-insert pairs  |

More Details on each function can be found in the web application.

### Designing sgRNA-insert pairs
The design of sgRNA-insert pairs can be performed using the web application or the original python scripts. The web appliation is more user friendly, as no prior bioinformatic knowledge and 
installations are neccessary. This function takes a list of amino acid mutations as well as a genome file in .gb format as input and generates all possible sgRNA-insert pairs. Please refer to the publication to find out more about the design principles. The resulting list of sgRNA-insert pairs can be used to synthesise DNA oligomers. 

### Mutagenesis on a protein sequence
This function allows the mutagenesis of a single protein sequence. Each amino acid in the sequence is mutated to all other amino acids. The output table can 
be used as input for the sgRNA-insert pair design. It takes a gene name and the corresponding protein sequence as input.

### Off-target finder for potential binding sites
We recommend using this function to find the most suited sgRNA-insert pair for specific mutations. Especially if you want only one sgRNA-insert pair per mutation The design tab in the web application provides a table with all protospacers. This table can be used as input to find potentail off-targets. The application finds all regions in the genome with up to four mismatches and provides the original base pairing region, the position in the genome, the off-target sequence, and the number of found mismatches.
#### Note
We recommed to run this only for a few base pairing regions. If you have a lot of them the local python version is more suited, as the computational time can get quite high.

### Visualization of read count tables
The visualization tab allows to gain a first look into the sequenced reads, after experimental procedures and data proccessing is performed. More details to the proccessing of the sequencing data can be found below. 
This interactive tab allows users to choose individual columns to visualize. Summaries, read count distribution, and replicate analysis can be performed. 


#### Note
All relevant python scripts are also available in the **Design sgRNA-insert pairs** folder. You can clone this repisotory if you prefer to run the individual functions locally on you computer.