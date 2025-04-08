# -*- coding: utf-8 -*-
""""
Created on Thu Oct 12 14:23:00 2023""
"""
import time
import wget
import pandas as pd

isolates = pd.read_csv("ncbi_dataset.tsv", sep='\t')
assemblies = pd.read_table("assembly_summary_genbank.txt", sep='\t', header=1, low_memory=False)

clinical_df = isolates.loc[isolates["Isolation type"] == "clinical"]

clinical_isolates = clinical_df["Assembly"].tolist()

TIME = 2 # 5 seconds

#clinical isolates

urls_clinical = []
for i in assemblies["# assembly_accession"]:
    if i in clinical_isolates: # needs to  be adjusted if clinical or environmental
        urls_clinical.append(assemblies.loc[assemblies["# assembly_accession"]==i,
                                            'ftp_path'].values[0])

OUTPUT_DIR = "clinical"
for i in urls_clinical:
    fragments = i.split("/")
    file_url =  i + "/" + fragments[-1] + "_genomic.gbff.gz"
    print(file_url)
    wget.download(file_url, out=OUTPUT_DIR)
    time.sleep(TIME)
