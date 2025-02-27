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

### 4. Aligning reads against reference sgRNA-insert pairs using minimap2
[Minimap2](https://github.com/lh3/minimap2) is a commandline tool to align sequencing reads for various purposes. We used the follwing command to align the sequenced reads to the reference sgRNA-insert pairs:
```
minimap2 -a -x sr -A 2 -B 6 -O 5,56 -E 4,1 -z 400,50 -t 4 <reference fasta file> <input .fastq file> > <path to output .sam file>
```
For more details on the parameters have a look into our publication or the documentation of minimap2. **Important:** You will need a reference fasta file before aligning the reads. Either create your own file or see step 1 for details.

### 5. Filtering reads
Aligned reads can be analyzed and filtered using a custom python script. It will filter out reads following a set of parameters we defined and will return the filtered reads and a read count table. 
Besides a read count table a detailed analysis of the filtered reads is generated and saved to a file. Because of that a path and prefix for the output files in necessary, indicated by the -o option.
Please refer to the method section of the publication for more details about the filtering parameters. 
```
py analyze_aligned_files.py -i <input .sam file> -r <reference fasta file> -o <path to output files>
```

### 6. Merging read count tables
The generated read count tables can be mapped back to the initial sgRNA - insert table. If you have more than one sample, conditions or replicates you can combine them all together to make the results more concise and clear, as the python script allows multiple input tables. The resulting table can be used to perform data analysis and visualization.
```
py merge_read_count_files.py -r <reference sgRNA-insert table> -o <path to output file> -i <read count table 1> <read count table 2> ...
```
You can reintroduce the final table into the visualization tab of the web application to gain first insight of your data.