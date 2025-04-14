"""
This file contains dictionaries that are used in the program.
"""

three_one = { "A" : "ALA", "G" : "GLY", "I" : "ILE", "L" : "LEU", "P" : "PRO",
              "V" : "VAL", "F" : "PHE", "W" : "TRP", "Y" : "TYR", "D" : "ASP",
              "E" : "GLU", "R" : "ARG", "H" : "HIS", "K" : "LYS", "S" : "SER",
              "T" : "THR", "C" : "CYS", "M" : "MET", "N" : "ASN", "Q" : "GLN"
    }

aa_nt = { "ALA" : ["GCT","GCC","GCA","GCG"],
         "GLY" : ["GGT","GGC","GGA","GGG"], "ILE" : ["ATT","ATC","ATA"],
          "LEU" : ["CTT","CTC","CTA","CTG","TTG","TTA"], 
          "VAL" : ["GTT","GTC","GTA","GTG"], "PHE" : ["TTT","TTC"],
          "TRP" : ["TGA","TGG"], "TYR" : ["TAT","TAC"],
          "ASP" : ["GAT","GAC"], "GLU" : ["GAA","GAG"],
          "ARG" : ["AGA","AGG", "CGT", "CGC", "CGA", "CGG"], "HIS" : ["CAT", "CAC"],
          "LYS" : ["AAA","AAG"], "SER" : ["AGT","AGC","TCT","TCC", "TCA", "TCG"],
          "THR" : ["ACT","ACC","ACA","ACG"], "CYS" : ["TGT","TGC"], "MET" : ["ATG"], 
          "ASN" : ["AAT", "AAC"], "GLN" : ["CAA","CAG"], "PRO" : ["CCT","CCC","CCA","CCG"]
    }

base_pairs = {"A" : "T",
              "G" : "C",
              "C" : "G",
              "T" : "A"
    }


codon_usage = { "GGG" : 0.13, "GGA" : 0.09,"GGC" : 0.4, "GGT" : 0.38, #Gly
                "AGG" : 0.03, "AGA" : 0.04,  #Arg
                "CGG" : 0.08, "CGA" : 0.05,"CGC" : 0.37, "CGT" : 0.42,
                "CCC" : 0.1,  "CCT" : 0.16,"CCA" : 0.2,"CCG" : 0.55,#Pro
                "TGG" : 1.0,   #Trp
                "ACC" : 0.43, "ACT" : 0.21,"ACA" : 0.3,"ACG" : 0.23, #Thr
                "GCT" : 0.19, "GCC" : 0.25, "GCA" : 0.22, "GCG" : 0.34, #Ala
                "TCT" : 0.19, "TCC" : 0.17, "TCA" : 0.12, "TCG" : 0.13, #Ser
                "AGC" : 0.27, "AGT" : 0.13,
                "CTT" : 0.1,  "CTC": 0.1, "CTA" : 0.3, "CTG" : 0.55, #Leu
                "TTA" : 0.11, "TTG" : 0.11,
                "ATG" : 1, #Met
                "GTT" : 0.29, "GTC" : 0.2, "GTG" : 0.34, "GTA" : 0.17, #Val
                "CAA" : 0.31, "CAG" : 0.69, #Gln
                "AAA" : 0.76, "AAG" : 0.24, #Lys
                "GAA" : 0.7, "GAG": 0.3, #Glu
                "ATT" : 0.47, "ATC": 0.46, "ATA": 0.07, #Ile
                "TAT" : 0.53, "TAC": 0.47, #Tyr
                "CAT" : 0.52, "CAC": 0.48, #His
                "AAT" : 0.39, "AAC" : 0.61, #Asn
                "GAT" : 0.59, "GAC" : 0.41, #Asp
                "TGT" : 0.43, "TGC" : 0.57 # Cys
}


#NGG, CCN shift 0
substitution_1 = {"CGG" : "CGT",
                  "AGG" : "AGA",
                  "GGG" : "GGT"}

# NNG, NCC shift +1
substitution_nng = {"TTG" : "TTA",
                  "CTG" : "CTA",
                  "GTG" : "GTT",
                  "TCG" : "TCA",
                  "ACG" : "ACT",
                  "GCG" : "GCA",
                  "CAG" : "CAA",
                  "AAG" : "AAA",
                  "GAG" : "GAA",
                  "CGG" : "CGA",
                  "AGG" : "AGA",
                  "GGG" : "GGA"}

substitution_ncc = {"TCC" : "TCT",
                    "ACC" : "ACT",
                    "GCC" : "GCA"}

#shift +2
#bei negativen Distanzen
substitution_cnn = {"CTA" : "TTA",
                    "CTG" : "TTG",
                    "CGA" : "AGA",
                    "CGG" : "AGG"}

#bei positiven Distanzen
substitution_nnc = { "TTC" : "TTT",
                     "CTC" : "CTT",
                     "ATC" : "ATT",
                     "GTC" : "GTA",
                     "TCC" : "TCT",
                     "ACC" : "ACA",
                     "GCC" : "GCA",
                     "TAC" : "TAT",
                     "CAC" : "CAT",
                     "AAC" : "AAT",
                     "GAC" : "GAT",
                     "TGC" : "TGT",
                     "CGC" : "CGA",
                     "AGC" : "AGT",
                     "GGC" : "GGT"}

  #shift +2
    #bei negativen Distanzen
substitution_cnn = {"CTA" : "TTA",
                    "CTG" : "TTG",
                    "CGA" : "AGA",
                    "CGG" : "AGG"}

codon_usage = { "GGG" : 0.13, "GGA" : 0.09,"GGC" : 0.4, "GGT" : 0.38, #Gly
                "AGG" : 0.03, "AGA" : 0.04,  #Arg
                "CGG" : 0.08, "CGA" : 0.05,"CGC" : 0.37, "CGT" : 0.42,
                "CCC" : 0.1,  "CCT" : 0.16,"CCA" : 0.2,"CCG" : 0.55,#Pro
                "TGG" : 1.0,   #Trp
                "ACC" : 0.43, "ACT" : 0.21,"ACA" : 0.3,"ACG" : 0.23, #Thr
                "GCT" : 0.19, "GCC" : 0.25, "GCA" : 0.22, "GCG" : 0.34, #Ala
                "TCT" : 0.19, "TCC" : 0.17, "TCA" : 0.12, "TCG" : 0.13, #Ser
                "AGC" : 0.27, "AGT" : 0.13,
                "CTT" : 0.1,  "CTC": 0.1, "CTA" : 0.3, "CTG" : 0.55, #Leu
                "TTA" : 0.11, "TTG" : 0.11,
                "ATG" : 1, #Met
                "GTT" : 0.29, "GTC" : 0.2, "GTG" : 0.34, "GTA" : 0.17, #Val
                "CAA" : 0.31, "CAG" : 0.69, #Gln
                "AAA" : 0.76, "AAG" : 0.24, #Lys
                "GAA" : 0.7, "GAG": 0.3, #Glu
                "ATT" : 0.47, "ATC": 0.46, "ATA": 0.07, #Ile
                "TAT" : 0.53, "TAC": 0.47, #Tyr
                "CAT" : 0.52, "CAC": 0.48, #His
                "AAT" : 0.39, "AAC" : 0.61, #Asn
                "GAT" : 0.59, "GAC" : 0.41, #Asp
                "TGT" : 0.43, "TGC" : 0.57 # Cys
    }
