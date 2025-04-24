
# Step 2 - sgRNA-insert pair design

Here all required python scripts to generate sgRNA-insert pairs for a list of amino acid mutations can be found. The main script for this is *design_sgRNA_insert_pairs.py* By providing a list of mutations you can 
generate all possible sgRNA-insert pairs needed for CRISPR-assisted recombineering. At the moment the script is generating sgRNA-insert pairs for genes of *E. coli*. If you need another organism please download the
.gb (genebank) file for that organisms genome. In line 226 of the python script you than can specify the name of your target organism. The following command will allow you to execute the design process:
```
py design_sgRNA_insert_pairs.py -i <input file containing target amino acid mutation> -o <path to output table>
```
An example table for the input mutation table can be found in the folder **Example Data**. The *write_data_frame.py* is used by the main script. Make sure it is in the same directory as the main script.

## Generate reference files
This script generates two files out of the sgRNA-insert pair table. First, a reference fasta file, which is necessary to find matching reads during the data processing step. Second, a list of base pairing regions is provided, which can be used to find potential off-targets.
```
py generate_reference_files.py -i <file containing sgRNA-insert pairs in csv> -f <path to output fasta file> -p <path to output base pairing file >
```
## Mutagenesis
This script performs mutagenesis over all amino acids of a provided protein sequence. You need a protein sequence and the gene name and it will produce a table with all possible amino acid mutations, The resulting file can be used to design sgRNA-insert pairs.
```
py mutagenesis.py <"aa_sequence"> <"gene_name">
```

## Off-target finder
The *generate_reference_files.py* script produces as a file containing all base pairing regions. This can be used as input to find potential off targets. This file and a genome file in .gb format are needed to run the script. 
```
py off_target_finder.py -i <input_file> -g <genome_file> -o <output_file>
```
#### Note
As each base pairing region needs to be compared to the whole genome, the script is will have a long computational time based on the size of your list.

## Map Mutations back
To check if the generated sgRNA-insert pairs match to the input mutations we recommend to run the python script *map_mutations_back.py*. This script serves as a control to make sure that there is no issue in the design step and only sgRNA-insert pairs with the right mutations are present in the file.
```
py map_mutations_to_sgRNAs.py -i <List of the original mutations used to generate the sgRNA-insert pairs> -s <List of sgRNA-insert pairs>
```

## Potential issues
We highly recommend that you check some of the generated sgRNA-insert pairs randomly to make sure everything is in order before you purchase the DNA-oligomers. If you encounter any problems feel free to open an issue on our GitHub repository.