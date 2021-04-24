#!/usr/bin/env python3
import os
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO

# get all sequence records for the specified genbank file
recs = [rec for rec in SeqIO.parse("hCoV-19_ReferenceSequence.gb", "genbank")]

# print the number of sequence records that were extracted
print(len(recs))

# print annotations for each sequence record
for rec in recs:
	print(rec.annotations)

# print the CDS sequence feature summary information for each feature in each
# sequence record
for rec in recs:
    feats = [feat for feat in rec.features if feat.type == "CDS"]
    for feat in feats:
        print(feat)