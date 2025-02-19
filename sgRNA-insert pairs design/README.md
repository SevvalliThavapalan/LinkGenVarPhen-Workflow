
## sgRNA-insert pair design

Here all required Python scripts to generate sgRNA-insert pairs for a list of amino acid mutations can be found. The main script for this is *design_sgRNA_insert_pairs.py* By providing a list of mutations you can 
generate all possible sgRNA-insert pairs needed for CRISPR-assisted recombineering. At the moment the script is generating sgRNA-insert pairs for genes of **E. coli**. If you need another organism please download the
.gb (genebank) file for that organisms genome. In line 226 of the python script you than can specify the name of your target organism. The following command will allow you to execute the design process:
```
py design_sgRNA_insert_pairs.py -i <input file containing target amino acid mutation> -o <path to output table>
```
An example table for the input mutation table can be found in the folder Example Data. The *write_data_frame.py* is used by the main script. Make sure it is in the same directory and it should 