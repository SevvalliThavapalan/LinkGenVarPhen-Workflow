import pandas as pd
import os
import wget
import time

isolates = pd.read_csv("isolates.tsv", sep='\t')
assemblies = pd.read_table("assembly_summary_genbank.txt", sep='\t', header=1, low_memory=False)

clinical_df = isolates.loc[isolates["Isolation type"] == "clinical"]
environmental_df = isolates.loc[isolates["Isolation type"] == "environmental/other"]

clinical_isolates = clinical_df["Assembly"].tolist()
environmental_isolates = environmental_df["Assembly"].tolist()

t = 5 # 5 seconds
urls = []
for i in assemblies["# assembly_accession"]:
    if i in clinical_isolates:
        urls.append(assemblies.loc[assemblies["# assembly_accession"]==i, 'ftp_path'].values[0])

output_directory = "gbff_files"
for i in urls:
    fragments = i.split("/")
    file_url = i + "/" + fragments[-1] + "_genomic.gbff.gz"
    print(file_url)
    wget.download(file_url, out=output_directory)
    time.sleep(t)
