#Cria um ficheiro genbank para os genomas de 2610801 ate 2873800

"""
    Imports
"""
import os

"""
    BioPython
"""
from Bio import SeqIO
from Bio import Entrez

"""
    xls file
"""
import xlwt

"""
    Create directory
"""
if not os.path.exists("GenBank"):
        os.makedirs("GenBank")


"""
    Create genbank file
    File will be saved in the genbank directory
"""
Entrez.email = "history.a70500@alunos.uminho.pt"
handler = Entrez.efetch(db="nucleotide",rettype="gbwithparts",retmode="text",id="NC_002942.5",seq_start=2610801 ,seq_stop=2873800)
record = SeqIO.read(handler,"gb")

SeqIO.write(record,"./GenBank/genbank.gb","genbank")

file = SeqIO.read("./GenBank/genbank.gb", "genbank")


"""
    Auxiliar function
"""
def sizeSequence(tamanho):
    i=0
    lista=[]
    x=[]
    resultado=[]
    for i in range (len(tamanho)):
        x=tamanho[i]
        lista.extend(x + '-')
        i+=1

    contador=0
    for i in range (len(lista)):
        if (lista[i]!='-'):
            contador+=1

        else:
            resultado.append(str(contador))
            contador=0

    return resultado



"""
    Dictionary with features for the gene and proteins
"""
features_gene = {}
features_gene["GeneID"] = []
features_gene["Locus_tag"] = []
features_gene["Gene"] = []

features_protein = {}
features_protein["Name"] = []
features_protein["Protein_id"] = []
features_protein["Size"] = []
features_protein["Function"] = []
features_protein["EC_number"] = []
features_protein["Location"] = []
features_protein["Sequence"] = []
features_protein["Note"] = []

"""
    Adds the features
"""
for feature in file.features:
    # Gene info
    if feature.type == "gene":
        features_gene["GeneID"].append(feature.qualifiers["db_xref"][0])
        features_gene["Locus_tag"].append(feature.qualifiers["locus_tag"][0])
        try:
            features_gene["Gene"].append(feature.qualifiers["gene"][0])
        except:
            features_gene["Gene"].append("")

    # only CDS for getting the proteins info
    if feature.type == "CDS":
        features_protein["Location"].append(feature.location)
        features_protein["Protein_id"].append(feature.qualifiers["protein_id"][0])
        features_protein["Sequence"].append(feature.qualifiers["translation"][0])
        features_protein["Size"] = sizeSequence(features_protein["Sequence"])
        features_protein["Name"].append(feature.qualifiers["product"][0])
        try:
            features_protein["Function"].append(feature.qualifiers["function"][0])
        except:
            features_protein["Function"].append("Function unknown")

        try:
            features_protein["EC_number"].append(feature.qualifiers["EC_number"][0])
        except:
            features_protein["EC_number"].append("")

        try:
            features_protein["Note"].append(feature.qualifiers["note"][0])
        except:
            features_protein["Note"].append("")

    if feature.type == "tRNA" or feature.type == "misc_feature":
        features_protein["Location"].append("")
        features_protein["Protein_id"].append("")
        features_protein["Sequence"].append("")
        features_protein["Size"] = 0
        features_protein["Name"].append("")
        features_protein["Function"].append("Function unknown")
        features_protein["EC_number"].append("")
        features_protein["Note"].append("")



"""
    Creating table
"""
wb = xlwt.Workbook()
ws = wb.add_sheet('Table')


"""
    Style for the first line of the table
"""
style1 = xlwt.easyxf("font: name Times New Roman, color-index red, bold on; align: wrap on, vert centre, horiz center")


"""
    Style for the second line of the table
"""
style2 = xlwt.easyxf("font: name Cambria; align: wrap on, vert centre, horiz center")
"""
    first line
    (line, column, data, style)
"""
ws.write(0,0,'GeneID',style1)
ws.write(0,1,'Locus Tag',style1)
ws.write(0,2,'Gene Name',style1)
ws.write(0,3,'Strand',style1)
ws.write(0,4,'Uniprot ID',style1)
ws.write(0,5,'Revision Grade',style1)
ws.write(0,6,'Accession Number Protein',style1)
ws.write(0,7,'Protein Name',style1)
ws.write(0,8,'Amino Acids Number',style1)
ws.write(0,9,'EC_Number',style1)
ws.write(0,10,'Description',style1)

"""
    Unkown functions table
"""
uf = xlwt.Workbook()
us = uf.add_sheet('Unkown Functions')

us.write(0,0,'GeneID',style1)
us.write(0,1,'Locus Tag',style1)
us.write(0,2,'Gene Name',style1)
us.write(0,3,'Strand',style1)
us.write(0,4,'Uniprot ID',style1)
us.write(0,5,'Revision Grade',style1)
us.write(0,6,'Accession Number Protein',style1)
us.write(0,7,'Protein Name',style1)
us.write(0,8,'Amino Acids Number',style1)
us.write(0,9,'EC_Number',style1)
us.write(0,10,'Description',style1)



"""
    Changing the width of all colunms
"""
for x in range(0,15):
        ws.col(x).width = 256 * 50
        us.col(x).width = 256 * 50


"""
    Fill the content
"""


unknown_functions_counter = 1 #counter to know what line to insere in the unknown functions table

for x in range(1,len(features_gene["GeneID"]) + 1):
    aux = x - 1
    """
        Deleting the (+) or (-) in the location

        else -> For those that doesn't have location
    """
    if(features_protein["Location"][aux] != ""):
        start = features_protein["Location"][aux].start + 1
        location = "[" + str( start ) + ":" + str( features_protein["Location"][aux].end ) + "]"
    else :
        location = ""

    """
        Fill the content
    """
    ws.write(x,0,features_gene["GeneID"][aux],style2)
    #ws.write(x ,1,'NC_002942.5',style2)
    ws.write(x ,1,features_gene["Locus_tag"][aux],style2)
    ws.write(x ,2,features_gene["Gene"][aux],style2)
    if(features_protein["Location"][aux] != ""):
        ws.write(x,3,features_protein["Location"][aux].strand,style2)
    ws.write(x ,4,"",style2)
    ws.write(x ,5,"",style2)
    ws.write(x ,6,features_protein["Protein_id"][aux],style2)
    ws.write(x ,7,features_protein["Name"][aux],style2)
    #ws.write(x ,8,features_protein["Sequence"][aux],style2)
    ws.write(x ,8,features_protein["Size"][aux],style2)
    #ws.write(x ,10,location,style2)
    #ws.write(x ,11,"",style2)
    ws.write(x ,9,features_protein["EC_number"][aux],style2)
    ws.write(x ,10,features_protein["Function"][aux],style2)
    #ws.write(x ,14,"",style2)

    """
        Only unknown functions
    """
    if features_protein["Function"][aux] == "Function unknown":
        us.write(unknown_functions_counter,0,features_gene["GeneID"][aux],style2)
        #us.write(unknown_functions_counter ,1,'NC_002942.5',style2)
        us.write(unknown_functions_counter ,1,features_gene["Locus_tag"][aux],style2)
        us.write(unknown_functions_counter ,2,features_gene["Gene"][aux],style2)
        if(features_protein["Location"][aux] != ""):
            us.write(unknown_functions_counter,3,features_protein["Location"][aux].strand,style2)
        us.write(unknown_functions_counter ,4,"",style2)
        us.write(unknown_functions_counter ,5,"",style2)
        us.write(unknown_functions_counter ,6,features_protein["Protein_id"][aux],style2)
        us.write(unknown_functions_counter ,7,features_protein["Name"][aux],style2)
        #us.write(unknown_functions_counter ,8,features_protein["Sequence"][aux],style2)
        us.write(unknown_functions_counter ,8,features_protein["Size"][aux],style2)
        #us.write(unknown_functions_counter ,10,location,style2)
        #us.write(unknown_functions_counter ,11,"",style2)
        us.write(unknown_functions_counter ,9,features_protein["EC_number"][aux],style2)
        us.write(unknown_functions_counter ,10,features_protein["Function"][aux],style2)
        #us.write(unknown_functions_counter ,14,"",style2)
        unknown_functions_counter = unknown_functions_counter + 1

"""
    Saving xls files
"""
wb.save('table.xls')
uf.save('unknown_functions.xls')





