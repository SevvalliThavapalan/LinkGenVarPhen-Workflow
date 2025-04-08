# Step 1 - Database Mining



### 1. Retrieve genome assembly files
The first step is to retrieve genome assembly files from a database of your choosing. Here, we used the NCBI Pathogen Detection DB to retrieve clinical *E. coli* genomes.
The python script get_genome_files.py uses the information about the clinical isolates together with the information about the assembly files from NCBI to retrieve genome 
assembly files.

#### Note
The first step to retrieve the genome assembly files will vary depending on the database you want to use. But all other steps can be performed using the retrieved genome assembly files. 


### 2. Extract gene list
The final list of genes was extracted from the genome-scale model iML1515 of *E. coli*. The script *get_all_genes.py* generates a table with genes, their b number, and the pathway.

### 3. Protein Accessions and Sequences
Protein accessions are collected using the bash script called *filter_assembly_files.sh*. The first argument is the directory containing gene assembly files and the second argument 
is the name of the target gene. The output is redirected into a .txt file:
```
filter_assembly_files.sh <path_to_directory> <gene name> > output_file.txt
```
The output file is than taken as input for the next step to retrieve the protein sequences. *fetch_fasta.py* downloads the protein sequences for the accessions in a given file. 

```
py fetch_fasta.py -i <.txt file containing protein accessions> -o <path to output .fasta file>
```
### 4. Sequence Filtering
We recommend a filtering step to remove unwanted and faulty protein sequences, especially when using uncurated databases. The script *filter_fasta_file.py* takes a fasta file and filters protein sequences by length.
By choosing the length of a reference protein users filter out sequences which are longer or shorter than the specified length. The parameter can be adjusted inside the script.
```
py filter_fasta_file.py -i <input fasta file> -o <path to output fasta file> -l <length of reference protein>
```

### 5. Multiple Sequence Alignment
Before a multiple sequence alignment can be performed. The reference protein sequence needs to be added into the fasta file. Using the tool muscle the alignment can be performed using the following command:
```
muscle -super5 <path to input fasta file> -output <path to aligned afa file>
```
The super5 option is used for files containing more than 1000 sequences. More details can be found in the documentation of the alignment tool

### 6. Extract List of mutations
Amino acid mutations can be extracted using the script *extract_mutations.py*. The script takes the aligned afa file and the accession of the reference protein file to extract mutations and their frequencies.
The outpufile is saced in the same direction as the multiple sequence alignment file.
```
py extract_mutations.py -i <path to input afa file> -r <reference protein accession>
```

### 7. Check list of mutations
We recommend checking if the list of mutations matches the reference files. In some instances faulty sequences can lead to wrong positions of mutations. The script *check_mutations.py* offers an option to find potential issues.
```
py check_mutations.py -i <fasta file containing protein sequences> -g <gene name> -r <reference protein accession> -m <list of mutations in excel format>
```
This script reports back if there are mismatched mutations, meaning if the parent aa in the mutation list is different than the one in the reference sequence. This is an indication that you should have a closer look ino the MSA again.