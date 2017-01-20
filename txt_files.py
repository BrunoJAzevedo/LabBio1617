"""
    Percorre todos os ficheiros blast, pega nas informações do primeiro alignment e cria 
    um txt juntamente com as informações obtidas no seq.py
"""

import os
import sys

from Bio.Blast import NCBIXML
import seq



if not os.path.exists("TXT_FILES"):
        os.makedirs("TXT_FILES")

titulo = {}
length = {}
e_value = {}
aux = 0

for gene in seq.features_gene["Locus_tag"]:
    """
        Parsing aos blast_*.xml
    """
    result = open('./Blast/blast_%s.xml' %gene, 'r')
    records = NCBIXML.parse(result)
    for record in records:
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                length[gene] = alignment.length
                e_value[gene] = hsp.expect
                barra = 0
                titulo_ = ""
                parentesis = 0
                for char in  str(alignment.title):
                    if barra == 4 and parentesis == 0:
                        titulo_ += char
                    if char == "|":
                        barra +=1
                    if char == "]":
                        parentesis = 1
                    if barra == 4 and parentesis == 1:
                        titulo[gene] = titulo_
                        break
            break
        break
    """
        Criar ficheiro
    """
    txt = open('./TXT_FILES/%s.txt' %gene, 'w')

    txt.write("*********** " + seq.features_gene["GeneID"][aux] + " ***********" )
    txt.write("\n")
    txt.write("Locus Tag: " + seq.features_gene["Locus_tag"][aux])
    txt.write("\n")
    txt.write("Gene Name: " + seq.features_gene["Gene"][aux])
    txt.write("\n")
    if(seq.features_protein["Location"][aux] != ""):
        txt.write("Strand: " + str(seq.features_protein["Location"][aux].strand))
        txt.write("\n")
    txt.write("Protein ID: " + seq.features_protein["Protein_id"][aux])
    txt.write("\n")
    txt.write("Protein Name: " +seq.features_protein["Name"][aux])
    txt.write("\n")
    txt.write("Protein Size: " + seq.features_protein["Size"][aux])
    txt.write("\n")
    txt.write("EC Number: " + seq.features_protein["EC_number"][aux])
    txt.write("\n")
    txt.write("Function: " + seq.features_protein["Function"][aux])
    txt.write("\n\n")
    txt.write("***********  Blast Results  ***********")
    txt.write("\n")
    txt.write("Name:"+titulo[gene])
    txt.write("\n")
    txt.write("Size: "+str(length[gene]))
    txt.write("\n")
    txt.write("E Value: "+str(e_value[gene]))
    txt.write("\n\n")
    txt.write("***********  Sequence  ***********")
    txt.write("\n")
    txt.write(seq.features_protein["Sequence"][aux])

    aux += 1
                