"""
    Creates a genbank file and a fasta file with the genomes 2610801 to 2873800
"""

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
    for i in xrange (len(tamanho)):
        x=tamanho[i]
        lista.extend(x + '-')  
        i+=1

    contador=0
    for i in xrange (len(lista)):  
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
#features_protein["GeneID"] = []
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
        features_gene["GeneID"].append(feature.qualifiers["db_xref"][0].replace("GeneID:",""))
        features_gene["Locus_tag"].append(feature.qualifiers["locus_tag"][0])
        try:
            features_gene["Gene"].append(feature.qualifiers["gene"][0])
        except:
            features_gene["Gene"].append("") 

    # only CDS for getting the proteins info
    if feature.type == "CDS":
        features_protein["Location"].append(feature.location)
        #features_protein["GeneID"].append(feature.qualifiers["db_xref"][0].replace("GeneID:",""))
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
        #features_protein["GeneID"].append("")
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
ws.write(0,1,'Accession Number',style1)
ws.write(0,2,'Locus Tag',style1)
ws.write(0,3,'Gene Name',style1)
ws.write(0,4,'Strand',style1)
ws.write(0,5,'Uniprot ID',style1)
ws.write(0,6,'Revision Grade',style1)
ws.write(0,7,'Accession Number Protein',style1)
ws.write(0,8,'Protein Name',style1)
ws.write(0,9,'Amino Acids',style1)
ws.write(0,10,'Amino Acids Number',style1)
ws.write(0,11,'Cellular Location',style1)
ws.write(0,12,'GeneOntology',style1)
ws.write(0,13,'EC_Number',style1)
ws.write(0,14,'Description',style1)
ws.write(0,15,'Comments',style1)

"""
    Changing the width of all colunms
"""
for x in xrange(0,15):
        ws.col(x).width = 256 * 50


"""
    Fill the content
"""
for x in xrange(1,len(features_gene["GeneID"]) + 1):
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
    ws.write(x ,1,'NC_002942.5',style2)
    ws.write(x ,2,features_gene["Locus_tag"][aux],style2)
    ws.write(x ,3,features_gene["Gene"][aux],style2)
    if(features_protein["Location"][aux] != ""):
        ws.write(x,4,features_protein["Location"][aux].strand,style2)
    ws.write(x ,5,"",style2)
    ws.write(x ,6,"",style2)
    ws.write(x ,7,features_protein["Protein_id"][aux],style2)
    ws.write(x ,8,features_protein["Name"][aux],style2)
    ws.write(x ,9,features_protein["Sequence"][aux],style2)
    ws.write(x ,10,features_protein["Size"][aux],style2)
    ws.write(x ,11,location,style2)
    ws.write(x ,12,"",style2)
    ws.write(x ,13,features_protein["EC_number"][aux],style2)
    ws.write(x ,14,features_protein["Function"][aux],style2)
    ws.write(x ,15,"",style2)

wb.save('table.xls')






