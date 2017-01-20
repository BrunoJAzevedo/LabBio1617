"""
    Cria os ficheiros Blast numa directoria de nome Blast
    Permite que o utilizador coloque o locus tag que pretende fazer blast 
    Ou então correr o blast para todos os locus tag no ficheiro genbank.gb
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
    handler = NCBIWWW.qblast('blastp','nr',seq.features_protein["Sequence"][aux])
    ofile.write(handler.read())
    ofile.close()
    handler.close()


    resultxml = open('./Blast/blast_%s.xml' %gene, 'r')
    blast= NCBIXML.parse(resultxml)

    idsGoodBlast = []

    E_VALUE_THRESH = 0.5
    SCORE = 95
    for blast_record in blast:
        print blast_record.alignments
        for alignment in blast_record.alignments:
            print alignment
            for hsp in alignment.hsps:
                print(str(hsp))
                if hsp.expect < E_VALUE_THRESH and hsp.score> SCORE:
                    print("NICE\n\tE_VALUE_THRESH: " + str(hsp.expect) + " SCORE: " + str(hsp.score))
                    data = (alignment.title.split("|")[3],hsp.expect,hsp.score)
                    idsGoodBlast.append(data)
                    matches +=1
                    
    print idsGoodBlast


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
        handler = NCBIWWW.qblast('blastp','nr',protein_record["Sequence"][indice])
        save_file.write(handler.read())
        save_file.close()
        handler.close()
        indice += 1
