#!/usr/bin/env python3

import re
ref_seq = "hCoV-19_ReferenceSequence.gb"

def genebank_parse(input_file): #Provides an output of gene information from gbk file of reference genome
    
    gene_names = {'NS6':'ORF6', 'NS7A':'ORF7A', 'NS7B':'ORF7B', 'NS3':'ORF3', 
    'E':'E', 'M':'M', 'N':'N', 'NS8':'ORF8', 'S':"Spike", 'ORF1AB':'ORF1AB'}
    aa_len = {'ORF6':'61', 'ORF7A':'121', 'ORF7B':'43', 'ORF3':'various', 
    'E':'75', 'M':'222', 'N':'419', 'ORF8':'121', 'Spike':'1273', 'ORF1AB':'various'}
    
    CDS_count = 0      #Set a count as a reference to each record
    begin = 0
    end = 0
    gene = ''
    product = ''
    product_id = ''

    genbank = open(input_file)
    for line in genbank:
        if line.startswith('     CDS'):
            CDS_count += 1
            coordinates = line.rstrip('\n').split('..')     #parse out coordinates
            m = re.search(r'([0-9]+)', coordinates[0])
            begin = m.group()
            end = coordinates[-1].strip(')')
            length = int(end) - int(begin)
        elif line.startswith('     gene') or line.startswith('ORIGIN'):
            if CDS_count > 0:
                #print("{6}.) Gene: {0}  Coordinates: {1} - {2}, length: {3} \n Product: {4}, Protein_id: {5}\n".format(gene, begin, end, length, product, protein_id, CDS_count))
                #print("alt: {0}, gene: {1},".format(alt_gene, gene))
                #print("coordinates: {0}, {1}, {2}, product: {3}, aa_length: {4}".format(begin, end, length, product, aa_length))
                

                #Print output in format for SQL database values
                print("('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}'),".format(gene, alt_gene, begin, end, length, product, aa_length))
                
        elif line.startswith('                     /'):
            m2 = re.search(r'\s+\/(\w+)="(\w*.*)"', line)
            if m2:
                if m2[1] == 'gene':
                    alt_gene = m2[2].upper()
                    gene = gene_names.get(alt_gene)
                    aa_length = aa_len.get(gene)
                if m2[1] == 'product':
                    product = m2[2]
                if m2[1] == 'protein_id':
                    protein_id = m2[2]
                    

genebank_parse(ref_seq)