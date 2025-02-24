# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:37:26 2022

@author: Sevvalli Thavapalan
"""
import pandas as pd
from important_dictionaries import aa_nt


def get_keys_by_value(my_dict, search_value):
    """
    Get the keys by value
    """
    keys_with_value = []
    for key, values_list in my_dict.items():
        if search_value in values_list:
            keys_with_value.append(key)
    return keys_with_value

# Function to clean the values in the specified columns
def clean_values(cell_value):
    """
    Clean the values in the specified columns
    """
    if pd.notna(cell_value):
        return str(cell_value).strip("[]").replace("'", "")
    return cell_value

def process_gene(gene, dictionary_values):
    """
    Process the gene
    """
    if gene:
        return gene[0]
    print(gene, dictionary_values)
    for key, values in aa_nt.items():
        if dictionary_values in values:
            return key
    return None


def write_df(name,example_gene, reduced_dict):
    """
    Write the dataframe to a csv file
    """
    base_pairs = {"A" : "T",
                  "G" : "C",
                  "C" : "G",
                  "T" : "A"
        }
    sub_library_spacer = "TCCTCTGGCGGAAAGCCT"
    spacer = "GATC"
    pj23119 = "ttgacagctagctcagtcctaggtataatactagt"
    cas_handle = "gttttagagctagaaatagcaagttaaaataaggctag"
    oligo_df = pd.DataFrame()
    position_aa = []
    position_nt = []
    homology_arm = []
    protospacer = []
    distance = []
    pam_mutation = []
    mutated_pam = []
    parent_codon = []
    child_codon = []
    oligo = []
    mutated_codon = []
    target_strand = []
    for key, value in reduced_dict.items():
        #print(key, value)
        position = key -60
        for entry in value:
            if len(entry) > 5:
                position_aa.append(position/3+1)
                parent_codon.append(entry[3])
                child_codon.append(entry[4])
                position_nt.append(position+1)
                distance.append(entry[1])
                homology_arm.append(entry[5])
                pam_mutation.append(entry[0])
                mutated_pam.append(entry[6])
                mutated_codon.append(entry[7])
                if entry[0].startswith("CC"): #non template coding strand
                    if entry[1] >=0:  # positive distances
                        pos = (key-1) + (entry[1])
                        complement= ""
                        if (entry[1]%3) ==0: #
                            complement = example_gene[pos+3:pos+23]
                        elif (entry[1]%2) ==0:
                            complement = example_gene[pos+2:pos+22]
                        else:
                            complement = example_gene[pos+3:pos+23]
                        rev_complement = ""
                        for char in complement:
                            rev_complement += base_pairs[char]
                        protospacer.append(rev_complement[::-1])
                        oligo.append(sub_library_spacer + entry[5]
                                     + spacer + pj23119 + rev_complement[::-1] + cas_handle)
                        #print(rev_complement[::-1])
                        target_strand.append("non template / coding strand")
                    else: # negative distances
                        pos = (key) + (entry[1])
                        complement= ""
                        if (entry[1]%3) == 0:
                            complement = example_gene[pos+2:pos+22]
                            #print(len(entry[5]))
                        elif(entry[1]%2)==0:
                            complement = example_gene[pos+2:pos+22]
                        else:
                            complement = example_gene[pos+2:pos+22]
                            #print(entry[1])
                            #print(entry[5])
                            #print(complement)
                        rev_complement = ""
                        for char in complement:
                            rev_complement += base_pairs[char]
                        protospacer.append(rev_complement[::-1])
                        oligo.append(sub_library_spacer + entry[5] + spacer +
                                    pj23119 + rev_complement[::-1] + cas_handle)
                        #print(rev_complement[::-1])
                        target_strand.append("non template / coding strand")
                else: #template coding strand
                    pos = (key-1) + (entry[1])
                    if entry[1] >=0:  # positive distances
                        complement=""
                        if (entry[1]%3) ==0: #
                            complement = example_gene[pos-20:pos]
                        elif (entry[1]%2) ==0:
                            complement = example_gene[pos-20:pos]
                        else:
                            complement = example_gene[pos-20:pos]
                        protospacer.append(complement)
                        #print(len(complement))
                        target_strand.append("template / non coding strand")
                        oligo.append(sub_library_spacer + entry[5] +
                                    spacer + pj23119 + complement + cas_handle)
                    else:
                         # negative distances
                        pos = (key) + (entry[1])
                        complement= ""
                        if (entry[1]%3) == 0:
                            complement = example_gene[pos-20:pos]
                        elif(entry[1]%2)==0:
                            complement = example_gene[pos-21:pos-1]
                        else:
                            complement = example_gene[pos-21:pos-1]
                        protospacer.append(complement)
                        #print(len(complement))
                        target_strand.append("template / non coding strand")
                        oligo.append(sub_library_spacer + entry[5] +
                                     spacer + pj23119 + complement + cas_handle)
    mutated_aa = []
    for i in child_codon:
        keys_for_codon = get_keys_by_value(aa_nt, i)
        mutated_aa.append(keys_for_codon)
    parent_aa = []
    for j in parent_codon:
        keys_for_codon = get_keys_by_value(aa_nt, j)
        parent_aa.append(keys_for_codon)
    gene_name = []
    for i in range(len(parent_aa)):
        gene_name.append(name)
    oligo_df["gene"] = gene_name
    oligo_df["parent aa"] = parent_aa
    oligo_df["parent codon"] = parent_codon
    oligo_df["aa position"] = position_aa
    oligo_df["mutated aa"]  = mutated_aa
    oligo_df["child codon"] = child_codon
    oligo_df["nt position"] = position_nt
    oligo_df["dist mut pam"] = distance
    oligo_df["pam"] = pam_mutation
    oligo_df["mutated pam"] = mutated_pam
    oligo_df["homology arm"] = homology_arm
    oligo_df["target strand of protospacer"] = target_strand
    oligo_df["protospacer"] = protospacer
    oligo_df["oligo"] = oligo

    oligo_df = oligo_df.drop(oligo_df[oligo_df['protospacer'].map(len) < 20].index)
    oligo_df = oligo_df.drop(oligo_df[oligo_df['oligo'].map(len) < 150].index)
    columns_to_clean = ["parent aa", "mutated aa"]
    # Check if values in Column_A and Column_B are the same
    mask = oligo_df['parent aa'] == oligo_df['mutated aa']

    # Remove rows where values in Column_A and Column_B are the same
    oligo_df = oligo_df[~mask]
    oligo_df[columns_to_clean] = oligo_df[columns_to_clean].applymap(clean_values)
    oligo_df = oligo_df[~oligo_df['parent codon'].isin(['TAA', 'TAG'])]
    return oligo_df
