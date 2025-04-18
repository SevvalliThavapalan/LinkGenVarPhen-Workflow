"""
Created on Thursday Jan 25 13:25:43 2024

@author: Sevvalli Thavapalan
"""
import math
import argparse
import re
from Bio import SeqIO
import pandas as pd
from write_data_frame import write_df
from important_dictionaries import (three_one, aa_nt, substitution_nng,
                                    substitution_ncc, substitution_nnc,
                                    substitution_cnn, substitution_1)



def get_pams(searchspace):
    """
    Extracts occurrences of patterns '.GG' and 'CC.' from a given search space.

    Parameters:
    - searchspace (str): The input string to search for patterns.

    Returns:
    - ngg_dict (dict): A dictionary containing positions and matched strings for the pattern '.GG'.
    - ccn_dict (dict): A dictionary containing positions and matched strings for the pattern 'CC.'.

    Example:
    >>> searchspace = "ACCGGTAAGGCCCTCGG"
    >>> get_pams(searchspace)
    ({3: 'CGG', 10: 'CGG'}, {2: 'CCG'})
    """
    regex1 = re.compile('.GG')  # Pattern matching for '.GG'
    regex2 = re.compile('CC.')  # Pattern matching for 'CC.'
    ngg_dict = {}
    ccn_dict = {}

    # Iterate over matches for '.GG' and store positions and matched strings in ngg_dict
    for ngg in regex1.finditer(searchspace):
        ngg_dict[ngg.start()] = ngg.group()

    # Iterate over matches for 'CC.' and store positions and matched strings in ccn_dict
    for ccn in regex2.finditer(searchspace):
        ccn_dict[ccn.start()] = ccn.group()

    return ngg_dict, ccn_dict


def get_dist(position_dict):
    """
    Calculates the distance of each position in a dictionary from the reference position 29.
    Because the searchspace is 30 nt before and after the mutation.

    Parameters:
    - position_dict (dict): A dictionary containing positions and matched strings.

    Returns:
    - pam (list): A list of lists, where each inner list contains the matched
    string and its distance from position 29.

    Example:
    >>> position_dict = {3: 'CGG', 10: 'CGG'}
    >>> get_dist(position_dict)
    [['CGG', -26], ['CGG', -19]]
    """
    dist = 0
    pam = []

    # Iterate over the positions and matched strings in the input dictionary
    for key, value in position_dict.items():
        # Calculate the distance from the reference position 29, middle of the oligo
        if key < 29:
            dist = key - 29  # distance from the first nucleotide of PAM
        else:
            dist = key - 29  # distance from the last nucleotide of the mutation

        # Append the matched string and its distance to the pam list
        pam.append([value, dist])

    return pam

def get_homology_arm(example_gene, final_dict):
    """
    Retrieves the homology arms for each position in the final dictionary.

    Parameters:
    - example_gene (str): The reference gene sequence.
    - final_dict (dict): A dictionary containing positions, distances, and partial gene sequences.

    Returns:
    - final_dict (dict): An updated dictionary with homology arms added for each position.

    Example:
    >>> example_gene = "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
    >>> final_dict = {1: [['CGG', -5]], 4: [['TAA', 8], ['GGC', -6]]}
    >>> get_homology_arm(example_gene, final_dict)
    {1: [['CGG', -5, 'GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT'],
      4: [['TAA', 8, 'GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT'], 
      ['GGC', -6, 'GATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT']]}
    """
    for key, value in final_dict.items():
        pos_in_gene = key
        for pam in value:
            center = (math.floor(pos_in_gene +
                                 pam[1] / 2) if pam[1] < 0
                                 else math.ceil(pos_in_gene + pam[1] / 2))
            pam.append(example_gene[center - 42:center + 43].lower())
    return final_dict

def filter_pam(final_dict):
    """
    Filter the pams (after mutation). These ones should not be used.

    """
    reduced_dict =  {}
    exclusion_pams = [
    'AAG','AGA','AGC','AGG','ATG','CAG','CGA','CGC','CGG','CTG','GAG',
    'GCG','GGA','GGC','GGG','GGT','GTG','TAG','TGA','TGC','TGG','CAT']    
    for key, values in final_dict.items():
        for entry in values:
            if len(entry) > 5:
                if entry[7] not in exclusion_pams:
                    if key in reduced_dict.keys():
                        reduced_dict[key].extend([entry])
                    else:
                        reduced_dict[key] = [entry]
                    #if key in reduced_dict.keys():
                    #    reduced_dict[key].extend([entry])
                    #else:
                    #    reduced_dict[key] = [entry]
    return reduced_dict


def insert_target_mutations(final_dict, mut_dict):
    """
    Insert target mutations into the final dictionary.
    """
    adapted_dict = {}
    for key, value in final_dict.items():
        #print(mut_dict)
        #print(final_dict)
        #if (key-1) > 42 and (key-1) < len(example_gene)-42:# take care of the other cases
        for entry in value:
            
            harm = entry[2]
            if key in mut_dict.keys():
                child = mut_dict[key][1:]
                #print(child)
                for child_mut in child:
                    #print(child_mut)
                    if entry[1] < 0: #negative
                        parent_nt = harm[42-math.floor(entry[1]/2):
                                         42-math.floor(entry[1]/2)+3:].upper()
                        #print(parent_nt)
                        if key in adapted_dict.keys():
                            adapted_dict[key].extend([[entry[0],entry[1],
                                                    harm[:42-math.floor(entry[1]/2)].lower()+
                                                    child_mut+
                                                    harm[42-math.floor(entry[1]/2)+3:].lower(),
                                                    parent_nt, child_mut]])
                        else:
                            adapted_dict[key] = [[entry[0],entry[1],
                                                  harm[:42-math.floor(entry[1]/2)].lower()+
                                                  child_mut +
                                                  harm[42-math.floor(entry[1]/2)+3:].lower(),
                                                  parent_nt, child_mut]]
                    else: #positive
                        if key in adapted_dict.keys():
                            if (entry[1] % 2) ==0: #positive
                                parent_nt = (harm[42-math.floor(entry[1]/2):42-
                                                  math.floor(entry[1]/2)+3:].upper())
                                adapted_dict[key].extend([[entry[0],entry[1],
                                                        harm[:42-math.floor(entry[1]/2)].lower()+
                                                        child_mut +
                                                        harm[42-math.floor(entry[1]/2)+3:].lower(),
                                                        parent_nt,child_mut]])
                            else:
                                parent_nt = harm[42-math.floor(entry[1]/2)-1:42-
                                                math.floor(entry[1]/2)+2:].upper()
                                adapted_dict[key].extend([[entry[0],entry[1],
                                                    harm[:42-math.floor(entry[1]/2)-1].lower()+
                                                    child_mut +harm[42-
                                                                math.floor(entry[1]/2)+2:].lower(),
                                                    parent_nt,child_mut]])
                        else:
                            if (entry[1] % 2) ==0:
                                parent_nt = harm[42-
                                                 math.floor(entry[1]/2):42-
                                                 math.floor(entry[1]/2)+3:].upper()
                                adapted_dict[key] = [[entry[0],entry[1],
                                                    harm[:42-math.floor(entry[1]/2)].lower()+
                                                    child_mut +
                                                    harm[42-math.floor(entry[1]/2)+3:].lower(),
                                                    parent_nt,child_mut]]
                            else:
                                parent_nt = harm[42-
                                                 math.floor(entry[1]/2):42-
                                                 math.floor(entry[1]/2)+3:].upper()
                                adapted_dict[key] =[[entry[0],entry[1],
                                                    harm[:42-math.floor(entry[1]/2)-1].lower()+
                                                    child_mut +
                                                    harm[42-math.floor(entry[1]/2)+2:].lower(),
                                                    parent_nt,child_mut]]
    return adapted_dict

def get_files():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help="File with mutations", required=True, nargs="+")
    parser.add_argument('-o', '--output', help='path to outfile', required=True , nargs="+")
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments


def extract_flanking_regions(gene_bank_file, gene_name, positions_to_update, flank_length=60):
    """
    Extracts flanking regions of a gene from a gene bank file, properly handling reverse strands.
    """
    flanking_sequences = []
    merged_sequence = ""
    updated_positions = []
    gene_sequence = ""

    for record in SeqIO.parse(gene_bank_file, "genbank"):
        for feature in record.features:
            if feature.type == "gene" and 'gene' in feature.qualifiers and feature.qualifiers['gene'][0] == gene_name:

                start = feature.location.start
                end = feature.location.end
                strand = feature.strand  # Get strand information (+1 or -1)
                sequence = record.seq
                gene_sequence = sequence[start:end]

                # Extract flanking regions
                upstream_flank = sequence[max(0, start - flank_length):start]
                downstream_flank = sequence[end:min(len(sequence), end + flank_length)]

                # Merge flanking regions with gene sequence
                merged_sequence = upstream_flank + gene_sequence + downstream_flank

                # If the gene is on the reverse strand, reverse complement everything
                if strand == -1:
                    merged_sequence = merged_sequence.reverse_complement()
                    gene_sequence = gene_sequence.reverse_complement()

                    # Update positions accordingly for reverse strand
                    gene_length = len(gene_sequence)
                    updated_positions = [
                        (flank_length + gene_length) - ((pos-1) * 3)
                        for pos in positions_to_update
                    ]
                else:
                    # Update positions normally for forward strand
                    updated_positions = [
                        ((pos-1) * 3) + flank_length
                        for pos in positions_to_update
                    ]

                flanking_sequences.append((merged_sequence, updated_positions, gene_sequence))

    return merged_sequence, updated_positions


def main():
    """
    Main function to design sgRNA and insert pairs for a given list of mutations.
    """
# load genome and mutation list
    infiles = get_files()
    out_path = infiles["output"][0]
    file_path = infiles["input"][0]
    if file_path.endswith(".xlsx"):
        mutation_df = pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        mutation_df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide an Excel or CSV file.")
    oligo_df = []
    nucleotide_sequences = "Example_Data/BW25113.gb" #gene bank file

    pos_lists = mutation_df.groupby("gene")["aa position"].apply(list).to_dict()
    #print(pos_lists)

    mutation_lists = mutation_df.groupby("gene")["mutation"].apply(list).to_dict()

    for key, value in mutation_lists.items(): # gene + list of mutations
        parent_mutation = []
        child_mutation = []

        for mutation in value:
            if mutation[-1] in three_one.keys():
                parent_mutation.append(three_one[mutation[0]])
                child_mutation.append(three_one[mutation[-1]])
        #print(parent_mutation)
        #print(len(child_mutation))
        #print(key)
        merged_sequence, updated_positions = extract_flanking_regions(
            nucleotide_sequences,key,pos_lists[key])
        # Print the flanking sequences and updated positions
        pos_dict = {} # triplets to get exact pos in gene
        for i in range(0, len(merged_sequence), 3):
            pos_dict[i] = (str(merged_sequence[i]) + str(merged_sequence[i + 1])+ str(merged_sequence[i+2]))
        #print(pos_dict)
        #pam = {}
        mut_nt = []
        final_dict = {}

        for i in updated_positions:
            #print(i)
            searchspace=""
            searchspace = str(merged_sequence[(i)-30:(i)+33])
            #print(i)
            #print(pos_dict[i])
            #print(len(searchspace))
            mut_nt.append(pos_dict[(i)])
            #print(mut_nt)
            #print((i-1), pos_dict[(i-1)])
            #mut_pos = (i-1)
            ngg_dict, ccn_dict = get_pams(searchspace)
            ngg = get_dist(ngg_dict)
            ccn = get_dist(ccn_dict)
            final_dict[i] = ngg
            final_dict[i].extend(ccn)
        final_dict = get_homology_arm(str(merged_sequence), final_dict)
        mut_dict = {}

        for k in range(len(pos_lists[key])):
            current_key = (((pos_lists[key][k])-1) * 3) + 60
            #print(pos_dict[current_key])
            # Ensure each key starts with its own fresh value
            if current_key not in mut_dict:
                mut_dict[current_key] = set([mut_nt[k]])  # Start with only mut_nt[k]
                #print(mut_nt[k])
            else:
                mut_dict[current_key] = set(mut_dict[current_key])  # Ensure unique values

            # Now, update with new values that meet the condition
            for j in aa_nt[child_mutation[k]]:
                mismatches = sum(c1 != c2 for c1, c2 in zip(mut_nt[k], j))
                if 1 <= mismatches <= 3:
                    mut_dict[current_key].add(j)

            # Convert back to a list at the end of processing this key
            mut_dict[current_key] = list(mut_dict[current_key])

            #print(mut_dict)  # Debugging
        adapted_dict = insert_target_mutations(final_dict, mut_dict)
        #print(adapted_dict)
         # mutate PAM
        for value2 in adapted_dict.values():
            for entry in value2:
                a = entry[2]
            #print(a)
                pos = 0
                for char in range(len(a)):
                    if a[char].isupper():
                        pos = char
                        break
                ha = entry[2]
                if abs(entry[1]) < 56 :
                    if entry[1] == 3:
                        k = ha[pos + entry[1]:pos + entry[1]+3].upper()
                        if k in substitution_nng.keys():
                            j = ha[pos+entry[1]-3 :pos+entry[1]] + substitution_nng[k]# shift = 1
                            if not "GG" in j:
                                if not "CC" in j:
                                    entry.append((ha[:pos+entry[1]]+
                                                  substitution_nng[k] +ha[pos+entry[1]+3:]))
                                    entry.append(j[2:5])
                                    entry.append(substitution_nng[k])
                        if k in substitution_ncc.keys():
                            j = ha[pos+entry[1]-3 :pos+entry[1]] + substitution_ncc[k]# shift = 1
                            if not "GG" in j:
                                if not "CC" in j:
                                    entry.append((ha[:pos+entry[1]]+
                                                  substitution_ncc[k] +ha[pos+entry[1]+3:]))
                                    entry.append(j[2:5])
                                    entry.append(substitution_ncc[k])
                    elif entry[1] > 2: #positive distances (2oder3)
                        if (entry[1] % 3) == 0: #shift +2 OKAY
                            if entry[0].startswith("CC"):
                                k = ha[pos+entry[1]-3:pos+entry[1]].upper()
                                if k in substitution_nnc.keys():
                                    #print(ha,entry[0],k,entry[1])
                                    entry.append(ha[:pos-3+entry[1]]+
                                                 substitution_nnc[k] +ha[pos+entry[1]:])
                                    #print(len(ha))
                                    entry.append(substitution_nnc[k][-1]+entry[0][1:])
                                    entry.append(substitution_nnc[k])#changed pam
                                # GGN does not work
                            else:
                                #print(entry[1])
                                if entry[1] in [6,9,12,15,18,21,24,27,30]:
                                    #print(entry[1])
                                    k = ha[pos + entry[1]:pos + entry[1]+3].upper()
                                    #print(k)
                                    if k in substitution_ncc.keys():
                                        #print(ha, entry[1])
                                        entry.append(ha[:pos +
                                                    entry[1]-2]+ substitution_ncc[k] +
                                                    ha[pos + entry[1]+1:])
                                        entry.append(substitution_ncc[k][1:]
                                                     +entry[0][-1]) #changed pam
                                        entry.append(substitution_ncc[k])
                                    if k in substitution_nng.keys():
                                        #print(ha, entry[0],k,entry[1])
                                        entry.append(ha[:pos + entry[1]-2]+
                                                     substitution_nng[k] + ha[pos + entry[1]+1:])
                                        entry.append(substitution_nng[k][1:]+entry[0][-1])
                                        entry.append(substitution_nng[k])
                                        #print(dictionaries.substitution_nng[k],entry[0])
                                else:
                                    if entry[0] in substitution_1.keys(): # shift = 0
                                        #print(ha, entry[0],entry[1])
                                        entry.append(ha[:pos+entry[1]-1]+
                                                     substitution_1[entry[0]] +ha[pos+entry[1]+2:])
                                        entry.append(substitution_1[entry[0]])
                                        entry.append(substitution_1[entry[0]])
                    elif entry[1] < 0: # negative distances
                        if (entry[1] % 3) == 0: #shift 2
                            k = ha[pos+entry[1]:pos+entry[1]+3].upper()

                            if entry[0].startswith("CC"):
                                if  k in substitution_cnn.keys():
                                    #print(ha, entry[1],entry[0])
                                    entry.append(ha[:pos+entry[1]]+
                                                 substitution_cnn[k]+ha[pos+entry[1]+3:])
                                    entry.append(entry[0][0]+substitution_cnn[k][:-1]) #changed pam
                                    entry.append(substitution_cnn[k])
                                    #ggn not possible

                        else:
                            if (entry[1] % 2 ) != 0:
                                frame = entry[1]+2 # shift 1
                                if (frame % 3) == 0:
                                    if entry[0] in substitution_1.keys():
                                        #print(ha,entry[1],entry[0])
                                        entry.append(ha[:pos+entry[1]-1]+
                                                     substitution_1[entry[0]] +ha[pos+entry[1]+2:])
                                        entry.append(substitution_1[entry[0]])
                                        entry.append(substitution_1[entry[0]])
                                else:
                                    k = ha[pos + entry[1]-2:pos + entry[1]+1].upper()
                                    if k in substitution_nng.keys(): #shift 1 ungerade
                                          #print(ha, entry[1],entry[0],pos)
                                          #shift 0
                                        entry.append(ha[:pos-2+entry[1]]+
                                                     substitution_nng[k]+ ha[pos+1+entry[1]:])
                                        entry.append(substitution_nng[k][1:]+entry[0][-1])
                                        entry.append(substitution_nng[k])
                                    if k in substitution_ncc.keys(): #shift 1 ungerade
                                        #print(ha, entry[1],entry[0],pos)
                                             # shift 0
                                        entry.append(ha[:pos-2+entry[1]]+
                                                     substitution_ncc[k]+ ha[pos+1+entry[1]:])
                                        entry.append(substitution_ncc[k][1:]+entry[0][-1])
                                        entry.append(substitution_ncc[k])

                            else:
                                frame = entry[1]-2 #shift = 1
                                if (frame % 3) == 0:
                                    #print(k)
                                    k = ha[pos + entry[1]-2:pos + entry[1]+1].upper()
                                    if k in substitution_nng.keys(): #shift 1 ungerade
                                        #print(ha, entry[1],entry[0],pos)
                                        #shift 0
                                        entry.append(ha[:pos-2+entry[1]]+
                                                     substitution_nng[k]+ ha[pos+1+entry[1]:])
                                        entry.append(substitution_nng[k][1:]+entry[0][-1])
                                        entry.append(substitution_nng[k])
                                    if k in substitution_ncc.keys(): #shift 1 ungerade
                                        #print(ha, entry[1],entry[0],pos)
                                        #shift 0
                                        entry.append(ha[:pos-2+entry[1]] +
                                                     substitution_ncc[k] + ha[pos+1+entry[1]:])
                                        entry.append(substitution_ncc[k][1:]+entry[0][-1])
                                        entry.append(substitution_ncc[k])
                                else:
                                    if entry[0] in substitution_1.keys():
                                        #print(ha,entry[1],entry[0])
                                        entry.append(ha[:pos+entry[1]-1]+
                                                     substitution_1[entry[0]] +ha[pos+entry[1]+2:])
                                        entry.append(substitution_1[entry[0]])
                                        entry.append(substitution_1[entry[0]])
                        if not ("gg" or "cc")in ha[pos-2:pos+6]:
                            if not "Gg" in ha[pos-2:pos+6]:
                                if not "Cc" in ha[pos-2:pos+6]:
                                    if not "cC" in ha[pos-2:pos+6]:
                                        if not "gG" in ha[pos-2:pos+6]:
                                            #print(ha)
                                            entry.append(ha)
                                            entry.append("-")
                                            entry.append("-")

        reduced_dict = filter_pam(adapted_dict)
        #print(reduced_dict)
        oligo_df.append(write_df(key,merged_sequence,reduced_dict))
    df = pd.concat(oligo_df, axis = 0)
    df.reset_index(drop=True, inplace=True)
    new_col = df.index.astype(str) + '_' + df['gene']
    df.insert(0, 'reference', new_col)
    out_str = out_path + ".csv"
    df.to_csv(out_str, index=False)
    print("Output saved at: "+ out_str)

if __name__ == "__main__":
    main()
