# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 10:48:10 2022

@author: Sevvalli Thavapalan
"""

import cobra
import pandas as pd



model =  cobra.io.read_sbml_model('iML1515.mat')
xl_file = pd.read_excel("gene_bnum.xlsx", dtype='str')
all_rxns = model.reactions


genes_subsystem = {}

for i in all_rxns:
    genes = i.genes
    for j in genes:
        if i.subsystem not in genes_subsystem.keys():
            genes_subsystem[i.subsystem] = set([j.id])
        else:
            genes_subsystem[i.subsystem].add(j.id)

for key, value in genes_subsystem.items():
    print(key, value)



bnum = {}
for row in range(len(xl_file["Gene Name"])):
    bnum[xl_file["Accession"][row]] = xl_file["Gene Name"][row]

final_dict = {}
for key, value in genes_subsystem.items():
    for i in value:
        if i in bnum.keys():
            if key not in final_dict.keys():
                final_dict[key] = set([bnum[i]])
            else:
                final_dict[key].add(bnum[i])

for key, value in final_dict.items():
    for j in value:

        print(key,"/",j)

pathways_model = pd.DataFrame()
pathways_model["Pathways"] = final_dict.keys()
pathways_model["Genes"] = list(final_dict.values())


pathways_model.to_excel("iML1515_all_genes_pathways.xlsx")