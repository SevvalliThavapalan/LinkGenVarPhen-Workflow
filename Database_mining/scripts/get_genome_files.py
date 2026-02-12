# -*- coding: utf-8 -*-
""""
Created on Thu Oct 12 14:23:00 2023""
"""
import time
import argparse
from pathlib import Path
import wget
import pandas as pd

parser = argparse.ArgumentParser(description="Download clinical isolate assemblies")

parser.add_argument("--isolates", type=Path, required=True, help="Path to ncbi_dataset.tsv")

parser.add_argument("--assemblies", type=Path, required=True, help="Path to assembly_summary_genbank.txt")

parser.add_argument("--outdir", type=Path, default=Path("clinical"), help="Output directory for downloaded files")

args = parser.parse_args()

isolates = pd.read_csv(args.isolates, sep="\t")
assemblies = pd.read_table( args.assemblies, sep="\t", header=1, low_memory=False)

clinical_df = isolates.loc[isolates["Isolation type"] == "clinical"]

clinical_isolates = clinical_df["Assembly"].tolist()

TIME = 2 # 5 seconds

#clinical isolates
args.outdir.mkdir(parents=True, exist_ok=True)
urls_clinical = []
for i in assemblies["# assembly_accession"]:
    if i in clinical_isolates: # needs to  be adjusted if clinical or environmental
        urls_clinical.append(assemblies.loc[assemblies["# assembly_accession"]==i,
                                            'ftp_path'].values[0])


for url in urls_clinical:
    fragments = url.split("/")
    file_url =  url + "/" + fragments[-1] + "_genomic.gbff.gz"
    print(file_url)
    wget.download(file_url, out=str(args.outdir))
    time.sleep(TIME)
