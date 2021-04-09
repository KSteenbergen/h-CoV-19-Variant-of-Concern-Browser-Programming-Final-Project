#!/usr/bin/env python3

import re

snps = 'SNPs.txt'

aa_code = {
    'G':'Glycine', 'P':'Proline', 'A':'Alanine', 'V':'Valine', 'L':'Leucine', 
    'I':'Isoleucine', 'M':'Methionine', 'C':'Cysteine', 'F':'Phenylalanine', 
    'Y':'Tyrosine', 'W':'Tryptophan', 'H':'Histidine', 'K':'Lysine', 'R':'Arginine', 
    'Q':'Glutamine', 'N':'Asparagine', 'E':'Glutamic Acid', 'D':'Aspartic Acid', 
    'S':'Serine', 'T':'Threonine' }
country_code = {'B.1.1.7':'UK', 'B.1.351':'South Africa', 'P.1':'Brazil', 'B.1.525':'Nigeria/Europe', 'A.23.1':'Uganda'}

counter = 0
snp_file = open(snps)
for line in snp_file:
    line = line.rstrip('\n')
    line = line.split('\t')
    counter += 1
    variant = line[0]
    country = country_code.get(variant)
    mt_code = line[1]
    mutation = line[1].split(':')
    mt_type = mutation[0]
    gene = mutation[1].upper()
    if gene == 'S':
        gene = 'Spike'
    elif gene == 'ORF3A':
        gene = 'ORF3'
    
    if mutation[0] == 'del':
        gene = int(gene)
        if gene in range(266, 21555):
            gene = 'ORF1AB'
        elif gene in range(21563, 25384):
            gene = 'Spike'
        elif gene in range(28274, 29533):
            gene  = 'N'
        else:
            print('error on the gene front')
     
    if len(mutation[2]) >= 2:
        m=re.search(r"(\D)([0-9]+)(\D)", mutation[2])
        if m:
            orig_aa = aa_code.get(m[1])
            position = m[2]
            mut_aa = aa_code.get(m[3])
            verbose = "{0} was replaced with {1} at position {2}".format(orig_aa, mut_aa, position)
            concise = "{0} replaced {1}".format(m[3], m[1])
    elif len(mutation[2]) < 2:
        position = mutation[2]
        verbose = "Deleted {0} nucleotides".format(position)
        concise = "{0} nucleotides deleted".format(position)
    #Print variables in format for SQL database entry
    print("({0},'{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}'),".format(counter, variant, country, gene, mt_code, mt_type, verbose, concise))
   