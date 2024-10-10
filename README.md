# A CRISPR library identifies metabolic mutations in clinical *E. coli* isolates that influence growth and antibiotic action

Here you can find all relevant scripts and information for the computational part of the paper XXX.
This repository contains the original scripts for designing sgRNAs and repair templates as well as the relevant scripts for a streamlit based web application.
This web application incorporates the original scripts to design CREATE sgRNAs and repair templates, allowing useres to upload and design sgRNAs and repair templates for their own mutations.  

## CREATE sgRNAs and repair templates design
The original method was developed by [Garst et. al](https://www.nature.com/articles/nbt.3718). Protocols were adapted 
and changed for our requirements and another study was published by our group and can be found [here](https://www.embopress.org/doi/full/10.15252/msb.202311596).
The folder **CREATE sgRNAs and repair templates Design** contains the scripts and amn example data set. The genome
of *E. coli* BW25113 is incorparated into the scripts. If you want to use a different genome you need to change the input in the code of 
the script **CREATE_sgRNAs.py**. We recommend using these scripts if you deal with a huge list of mutations (more than 200 MB). Otherwise the web application
will suffice to generate sgRNAs and repair templatess. It is important that the input Excel table containing the mutations has the following format: 

| Gene | Mutation | Position |
|:---------:|:--------:|:--------:|
| aaeA      | T5S      | 5        |
| aaeA      | L102Q    | 102      |
| aaeA      | K189E    | 189      |

## Streamlit based webapplication
The web app implementation using Streamlit allows the sgRNAs and repair templates design without installation (recommended for datasets smaller than 200 MB).
As above the input table has to have the same format as shown above. You can choose between different provided genomes as well as upload 
your own genomes. The genomes need to be gene bank files (.gb). For more deatils visit the web application (LINK).

## Clinical *E. coli* isolates and metabolic mutations
The dataset used in this study was obtained from the NCBI Pathogens Database. The name of the gene assembly files utilized to find metabolic mutations can
be found in the **Clinical isolates** folder. 