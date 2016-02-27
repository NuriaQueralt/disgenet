#!/usr/bin/python
'''
main_owlParserEFO.py

Version: 1.0
Date: 2015-09-17
Author: Nuria Queralt Rosinach
Description: Script to parse the efo ontology file in OWL (efo.owl) to extract the direct relation: efo-umls-name. 
'''
import sys,re

def parsingOWL(path,in_OWL_file):
    '''Function to parse the efo ontology (efo.owl) to extract the efo-umls mappings.'''
    
    # INPUTS
    input_file = "%s%s" % (path,in_OWL_file)
        
    # OUTPUTS    
    out_file = "efo_umls2efo2name.tab"
    umls2id2name_file = open("%s%s" % (path,out_file), 'w')
    umls2id2name_file.write("umls\tefo\tname\n")
    out_file2 = "efo_umls2efo.tab"
    umls2id2name_file2 = open("%s%s" % (path,out_file2), 'w')
    umls2id2name_file2.write("umls\tefo\tname\n")
    
    # ALGORITHM
    # READ XML INPUT FILE
    owlText = open(input_file).read()
    owlText_list = owlText.split('<!-- http://www.')
    #owlText_list = owlText.split('<!-- http://www.ebi.ac.uk/efo/EFO_')
    #owlText_list = owlText.split('<owl:Class rdf:about="&ORDO;Orphanet_')
    #owlText_list = owlText.split("</owl:Class>")[1:-1]
    
    # RE PATTERN DEFINITIONS
    id_pattern = re.compile(r'<owl:Class rdf:about="&efo;EFO_(\d+)">')
    name_pattern = re.compile(r'<rdfs:label.*?>(.+)</rdfs:label>')
    umls_pattern = re.compile(r'<efo:UMLS.*?([C]{1}\d{7})</efo:UMLS')
    obsolete_pattern = re.compile(r'<rdfs:subClassOf rdf:resource="&oboInOwl;ObsoleteClass"/>')
    
    # LOOP ONTO THE OWL FILE
    numFragments = 0
    dis = 0
    disObsoleteCount = 0
    disActiveCount = 0
    nameCount = 0
    id_withcui = 0
    id_withoutcui = 0
    cuis = 0
    id = 'NA'
    name = 'NA'
    umls = 'NA'
    for owlClass_0 in owlText_list:
        owlClass = owlClass_0.strip().replace("\n", "")
        numFragments += 1
#        print owlClass
        print " FRAGMEEEEEEEEEEEENT\n"
        
        # Regular Expression MATCHINGS
        id_match = id_pattern.search(owlClass)
        if id_match:
            id = id_match.group(1)
            dis += 1
            print id
            
            name_match = name_pattern.search(owlClass)
            if name_match:
                name = name_match.group(1)
                nameCount += 1
            print name
        
            obsolete_match = obsolete_pattern.search(owlClass)
            if obsolete_match:
                disObsoleteCount += 1
                print id, name, 'OBSOLETE TERM'
            else:
                disActiveCount += 1  

                umls_matches = umls_pattern.finditer(owlClass)
                if umls_matches:
#                    print umls_matches
                    for umls_match in umls_matches:
#                        print umls_match.group(0), " ", umls_match.group(1)
                        cuis += 1
                        umls = umls_match.group(1)
                        umls2id2name_file.write("%s\t%s\t%s\n" % (umls,id,name))
                        umls2id2name_file2.write("%s\t%s\t%s\n" % (umls,id,name))
                        print "MAPPING: ",umls, " ", id, " ", name
                if umls == 'NA':
                    id_withoutcui += 1
                    print "NO MAPPING: ",umls, " ", id, " ", name
                    umls = ''
                    umls2id2name_file.write("%s\t%s\t%s\n" % (umls,id,name)) 
                else:
                    id_withcui += 1
                      
           
        id = 'NA'
        name = 'NA'
        umls = 'NA'
        umls_matches = []
            
    print "Script has ended correctly. Please, find output at: %s%s. Remember to remove manually the last entry label." % (path,out_file)   
    print ""
    print ""
    print "Number of fragments :", numFragments     
    print "Number of IDs: ", dis
    print "Number of ID Names: ", nameCount
    print "Number of Obsolete IDs: ", disObsoleteCount
    print "Number of Active IDs: ", disActiveCount
    print "Number of EFO2UMLS mappings: ",cuis
    print "Number of id with umls mapping: ", id_withcui 
    print "Number of id without umls mapping: ", id_withoutcui




    
    umls2id2name_file.close()
    
    return



if __name__ == "__main__":


    try:
        path = "/home/nqueralt/workspace/disgenet2rdf_2015/in/"
        in_OWL_file = "efo.owl"

        parsingOWL(path,in_OWL_file)

    except OSError:
        print "Some problem occurred....T_T"
        sys.exit() 
