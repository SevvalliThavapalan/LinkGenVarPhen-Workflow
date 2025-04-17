# Data Processing
Due to the 200 MB upper data limit  of Streamlit, we recommend that the processing of sequencing reads is done locally.
Details can also be found in the method section of the publication.

#### Note

All scripts and tools used here are one possible way to process the data. Feel free to use your own scripts and tools. Here, the most Important
pocessing steps are covered. If you want more details please look into the documentation of each tool.

### 1.  Prepare all relevant files

Besides your sequencing files, the **reference sgRNA-insert pair table and fasta file** is necessary. If you use the web application the fasta file is generated automatically
together with the sgRNA-insert list. Otherwise the python script *generate_reference_file.py* in the sgRNA-insert pairs design directory  can be used. If you used nanopore sequencing to generate your sequencing reads, we recommend that the fastq read files for each barcode are merged into one file and you can skip to step 3. If you have paired reads after illumina sequencing you should continue with step 2.

### 2. Merging paired reads
[FLASh](https://ccb.jhu.edu/software/FLASH/#:~:text=FLASH%20is%20designed%20to%20merge,to%20merge%20RNA%2Dseq%20data.) is a commandline tool to merge paired reads. After installing the software you can use the following command to merge your paired reads.
```
flash Sample_R1.fastq Sample_R2.fastq -o Sample_merged
```
There are also executable versions available if you prefer that over using the commandline.

### 3. Trimming and filtering using cutadapt 
We used cutadapt 4.9 to remove primer sequences at the beginning and end of each sequenced read. The following command was used to trimm the data:

```
cutadapt.exe -e 0.3 -g  Forward primer sequence  -a Reverse primer sequence -O 5 --cores 4 -n 2 --untrimmed-output $path to untrimmed output file -o $path to trimmed output file $path to input file
```
For more details about individual parameters and options check out the documentation of [cutadapt](https://cutadapt.readthedocs.io/en/stable/). After trimming the primer sequences we recommend filtering reads which are too short or too long. This can be done using cutadapt. -m defines the minimal required length and -M defines the maximal length. 
```
cutadapt.exe -m 175 -M 500 -o <path to output file> --cores 4 <path to input file>
```

### 4. Finding perfectly matching reads
Filtered reads are matched against the original list of sgRNA-insert pairs. The previously generated fasta file of the sgRNA-insert pairs is used to find perfect matches in a .fastq file. A read count table is generated mapping each read to a reference. The python script can be used with the following command:
```
py find_perfect_matches.py -f <Input FASTQ file> -s <fasta file with sgRNA-insert sequences> -o <output file with read counts> -mf <output FASTQ file of matched reads> (optional)
```

### 6. Merging read count tables
The generated read count tables can be mapped back to the initial sgRNA - insert table. If you have more than one sample, conditions or replicates you can combine them all together to make the results more concise and clear, as the python script allows multiple input tables. The resulting table can be used to perform data analysis and visualization.
```
py merge_read_count_files.py -r <reference sgRNA-insert table> -o <path to output file> -i <read count table 1> <read count table 2> ...
```
You can reintroduce the final table into the visualization tab of the web application to gain first insight of your data.

### Data availability
As sequencing data files are rather big, we did not include any of the files here in the repository. Fastq and sam files can be found *here*