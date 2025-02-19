
## sgRNA-insert pair design

Here all required Python scripts to generate sgRNA-insert pairs for a list of amino acid mutations can be found. The main script for this is *design_sgRNA_insert_pairs.py* By providing a list of mutations you can 
generate all possible sgRNA-insert pairs needed for CRISPR-assisted recombineering. At the moment the script is generating sgRNA-insert pairs for genes of *E. coli*. If you need another organism please download the
.gb (genebank) file for that organisms genome. In line 226 of the python script you than can specify the name of your target organism. The following command will allow you to execute the design process:
```
py design_sgRNA_insert_pairs.py -i <input file containing target amino acid mutation> -o <path to output table>
```
An example table for the input mutation table can be found in the folder Example Data. The *write_data_frame.py* is used by the main script. Make sure it is in the same directory and it should 

## Generate reference files
This script generates two files out of the sgRNA-insert pair table. First, a reference fasta file is generated which is necessary to perform sequence alignment during the data processing step. Second, a list of base piring regions is provided, which can be used to find potential off-targets.
````
py generate_reference_files.py -i <file containing sgRNA-insert pairs in csv> -f <path to output fasta file> -p <path to output base pairing file >
```
## Mutagenesis
This script performs mutagenesis over all amino acids of a provided protein sequence. You need a protein sequence and the gene name and the script will produce a table with all possible amino acid mutations, The resulting file can be used to design sgRNA-insert pairs.
```
py mutagenesis.py <aa_sequence> <gene_name>
```

## Off-target finder