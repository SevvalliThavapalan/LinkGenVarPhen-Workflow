# A CRISPR library identifies metabolic mutations in clinical *E. coli* isolates that influence growth and antibiotic action

Here you can find all relevant scripts and information for the computational part of the paper XXX.
This repository contains the original scripts for designing oligos as well as the relevant scripts for a streamlit based webapplication.
This webapplication incorporates the original scripts to design CREATE oligos, allowing useres to upload and design oligos for their own mutations.  

## CREATE oligo design
The original method was developed by [Garst et. al](https://www.nature.com/articles/nbt.3718). The protocols were adapted 
and changed for our requirements. The folder **CREATE oligo Design** contains the scripts and amn example data set. The genome
of *E. coli* BW25113 is incorparated into the scripts. If you want to use a differemt genome you need to change the input in the code of 
the script **CREATE_oligos.py**. We recomend using these scripts if you deal with a huge list of mutations (more than 200MB). Otherwise the webapplication
will work to generate oligos. It is important that the input table containing the mutations has the following format: 

| Gene | Mutation | Position |
|:---------:|:--------:|:--------:|
| aaeA      | T5S      | 5        |
| aaeA      | L102Q    | 102      |
| aaeA      | K189E    | 189      |
