# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 11:59:58 2014

@author: Nuno
"""

import os
import sys

from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import seq



if not os.path.exists("Blast"):
    os.makedirs("Blast")

print "Deseja fazer blast de todas as proteínas ou só de uma?"
print " 1 -> Uma"
print " 2 -> Todas"

answer = raw_input("Resposta: ")

if answer == "1" or answer == "Uma" or answer == "UMA" or answer == "uma":
    gene = raw_input("Introduza o locus_tag do gene a pesquisar: ")
    error = -1
    aux = 0
    """
        Get Seq
    """
    for x in seq.features_gene["Locus_tag"]:
        if x == gene:
            seq_protein = Seq(str(seq.features_protein["Sequence"][aux]), IUPAC.extended_protein)
            #protein found, no error
            error = 0
            break
        aux += 1
    #protein not found
    if error == -1:
        sys.exit("Locus_tag não encontrado")

    """
        Run blast
    """
    ofile = open('./Blast/blast_%s.xml' %gene, 'w')
    print "A executar o blast"
    handler = NCBIWWW.qblast('blastp','swisprot',seq.features_protein["Sequence"][aux].format('gb'))
    ofile.write(handler.read())
    ofile.write('\n\n')
    ofile.close()
    handler.close()



else:
    indice = 0
    protein_record = {}
    protein_record["Sequence"] = []
    for x in seq.features_gene["Locus_tag"]:
        seq_protein = Seq(str(seq.features_protein["Sequence"][indice]), IUPAC.extended_protein)
        protein_record["Sequence"].append(SeqRecord(seq_protein))
        indice += 1

    indice = 0
    for gene in seq.features_gene["Locus_tag"]:
        print "A executar o blast para: " + seq.features_gene["Locus_tag"][indice]
        save_file = open('./Blast/blast_%s.xml' %gene, 'w')
        handler = NCBIWWW.qblast('blastp','swisprot',protein_record["Sequence"][indice].format('gb'))
        save_file.write(handler.read())
        save_file.write('\n\n')
        save_file.close()
        handler.close()
        indice += 1
"""
verify = open('./Blast/blast_%s_verification.txt' %gene, 'w')
E_VALUE_THRESH = 0.05
result = open('./Blast/blast_%s.xml' %gene, 'r')
records = NCBIXML.parse(result)

for record in records:
    for alignment in record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                verify.write('****Alignment***\n')
                verify.write('sequence: %s' %alignment.title)
                verify.write('length: %i' %alignment.length)
                verify.write('e value: %f' %hsp.expect)
                verify.write(hsp.query[0:75] + '...')
                verify.write(hsp.query[0:75] + '...')
                verify.write(hsp.match[0:75] + '...')
                verify.write(hsp.match[0:75] + '...')
                verify.write(hsp.sbjct[0:75] + '...')
                verify.write('\n')

verify.close()
result.close()
"""
"""
#execução do blast
save_file = open('blast_%s.xml' %gene, 'w')
result_handle = NCBIWWW.qblast('blastp', 'swissprot', protein_record.format('gb'))
save_file.write(result_handle.read())
save_file.write('\n\n')
save_file.close()
result_handle.close()


verify = open('blast_%s_verificacao.txt' %gene, 'w')
E_VALUE_THRESH = 0.05
result = open('blast_%s.xml' %gene,'r')
records = NCBIXML.parse(result)
for record in records:
    for alignment in record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                verify.write('****Alignment****\n')
                verify.write('sequence: %s' %alignment.title)
                verify.write('length: %i' %alignment.length)
                verify.write('e value: %f' %hsp.expect)
                verify.write(hsp.query[0:75] + '...')
                verify.write(hsp.match[0:75] + '...')
                verify.write(hsp.sbjct[0:75] + '...')
                verify.write('\n')
verify.close()
result.close()

"""
