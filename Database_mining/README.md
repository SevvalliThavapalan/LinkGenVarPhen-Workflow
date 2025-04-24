# Step 1 - Database Mining



### 1. Retrieve genome assembly files
The first step is to retrieve genome assembly files from a database of your choosing. Here, we used the NCBI Pathogen Detection DB to retrieve clinical *E. coli* genomes.
The python script *get_genome_files.py* uses the information about the clinical isolates together with the information about the assembly files from NCBI to retrieve genome 
assembly files.

#### Note
The first step to retrieve the genome assembly files will vary depending on the database you want to use. But all other steps can be performed using the retrieved genome assembly files. 

### 2. Extract gene list
The final list of genes was extracted from the genome-scale model iML1515 of *E. coli*. The script *get_all_genes.py* generates a table with genes, their b number, and the pathway.
Genome scale model can be downloaded [here](http://bigg.ucsd.edu/models/iML1515).
### 3. Protein accessions and sequences
Protein accessions are collected using the bash script called *filter_assembly_files.sh*. The first argument is the directory containing gene assembly files and the second argument 
is the name of the target gene. The output is redirected into a .txt file:
```
filter_assembly_files.sh <path_to_directory> <gene name> > output_file.txt
```
The output file is taken as input for the next step to retrieve the protein sequences. *fetch_fasta.py* downloads the protein sequences for the accessions in a given file. 

```
py fetch_fasta.py -i <.txt file containing protein accessions> -o <path to output .fasta file>
```
Make sure that every accession is in a new line.
### 4. Sequence filtering
We recommend a filtering step to remove unwanted and faulty protein sequences, especially when using uncurated databases. The script *filter_fasta_file.py* takes a fasta file and filters protein sequences by length.
By choosing the length of a reference protein users filter out sequences which are longer or shorter than the specified length. The parameter can be adjusted inside the script.
```
py filter_fasta_file.py -i <input fasta file> -o <path to output fasta file> -l <length of reference protein>
```
### 5. Multiple sequence alignment
Before a multiple sequence alignment can be performed. The reference protein sequence needs to be added into the fasta file. Using the tool muscle the alignment can be performed using the following command:
```
muscle -super5 <path to input fasta file> -output <path to aligned afa file>
```
The super5 option is used for files containing more than 1000 sequences. More details can be found in the documentation of the alignment tool. 
### 6. Extract list of mutations
Before mutations can be extracted new lines in the aligned fasta file need to be removed. This is performed using the following command:
```
seqtk seq <path to input .afa file> > <$path to output .afa file>
```
#### Note 
We recommend to check the MSA latest at this stage to make sure that no faulty sequence remains in the file. For that the [Alignmentviewer](https://alignmentviewer.org/) can be used. This is an fast way to chek your alignment.
In the next step amino acid mutations can be extracted using the script *extract_mutations.py*. The script takes the aligned afa file and the accession of the reference protein file to extract mutations and their frequencies.
The outpufile is saved in the same direction as the multiple sequence alignment file.
```
py extract_mutations.py -i <path to input afa file> -r <reference protein accession> -g <gene name>
```
### 7. Check list of mutations
We recommend checking if the list of mutations matches the reference files. In some instances gaps in the alignment can lead to shifted positions from the reference. The script *check_mutations.py* offers an option to find potential issues and correct them. The output file will generate a corrected list with the right positions in the reference sequence.
```
py check_mutations.py -a <alignment file> -r <reference accession> -m <list of mutations in excel format from extract mutations> -o <path to output excel file>
```
### 8. Merge multiple list of mutations
If you have more than one list of mutation you can use the *merge_mutations_files.py* to combine them into one single file. The resulting table can be used to design sgRNA-insert pairs. The files should be in the same folder and end with .xlsx. The script will take all files that are present in the directory and merge them, so make sure that no other files with the .xlsx extension are present.
```
py merge_mutations_files.py -i <path to input  folder> -o <path to output file>
```