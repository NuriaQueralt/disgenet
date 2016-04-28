#!/usr/bin/python
'''
main_owlParserEFO.py

Version: 2.0
Date: 2016-03-23
Author: Nuria Queralt Rosinach
Description: Script to parse the efo ontology file in OWL (efo.owl) to extract the direct relation: efo-umls-name. 
'''
import sys,re
from lib import abravo_lib as utils

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
    umls2id2name_file2.write("umls\tefo\n")
    
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
                        umls2id2name_file2.write("%s\t%s\n" % (umls,id))
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
    umls2id2name_file2.close()
    
    return

def parsingXrefOWL(path,in_OWL_file):
    '''Function to parse the efo ontology (efo.owl) to extract the efo-umls mappings.'''
    
    # INPUTS
    input_file = "%s%s" % (path,in_OWL_file)
        
    # OUTPUTS    
    out_file = "efo_umls2efo2name.tab"
    umls2efo2name_file = open("%s%s" % (path,out_file), 'w')
    umls2efo2name_file.write("umls\tefo\tname\n")
    out_file2 = "efo_umls2id2name.tab"
    umls2id2name_file = open("%s%s" % (path,out_file2), 'w')
    umls2id2name_file.write("umls\tvocabulary\tname\n")
    
    # VARIABLE
    vocabs_dict = {}
    efo2umls_dict = {}
    vocab2umls_dict = {}
    
    # ALGORITHM
    # READ XML INPUT FILE
    owlText = open(input_file).read()
    owlText_list = owlText.split('    // Classes\n')[1].split('    // Annotations\n')[0].split('    <!-- http://')
    i = 0
    for fragment in owlText_list:
        i += 1
        #print "start fragment:\n", fragment,"\nfinal fragment\n" 
    print "Number of classes: ", i
    #owlText_list = owlText.split('<!-- http://www.')
    #owlText_list = owlText.split('<!-- http://www.ebi.ac.uk/efo/EFO_')
    #owlText_list = owlText.split('<owl:Class rdf:about="&ORDO;Orphanet_')
    #owlText_list = owlText.split("</owl:Class>")[1:-1]
    
    # RE PATTERN DEFINITIONS
    id_pattern = re.compile(r'<owl:Class rdf:about="(.+)">\n')
    name_pattern = re.compile(r'<rdfs:label.*?>(.+)</rdfs:label>')
    citation_pattern = re.compile(r'<efo:(.+)_definition_citation.*?>(.+):(.+)</efo:')
    xref_pattern = re.compile(r'<oboInOwl:hasDbXref.*?>(.+):(.+)</oboInOwl:hasDbXref>')
    obsolete_pattern = re.compile(r'<rdfs:subClassOf rdf:resource="&oboInOwl;ObsoleteClass"/>')
     
    # LOOP ONTO THE OWL FILE
    numFragments = 0
    dis = 0
    disObsoleteCount = 0
    disActiveCount = 0
    nameCount = 0
    id_withcui = 0
    id_withoutcui = 0
    citations = 0
    xrefs = 0
    id = 'NA'
    name = 'NA'
    citation = 'NA'
    xref = 'NA'
    for owlClass_0 in owlText_list:
        owlClass = owlClass_0.strip()
#        owlClass = owlClass_0.strip().replace("\n", "")
        numFragments += 1
#        print owlClass
#        print " FRAGMEEEEEEEEEEEENT\n"
         
        # Regular Expression MATCHINGS
        id_match = id_pattern.search(owlClass)
        if id_match:
            id = id_match.group(1)
            dis += 1
#            print id
            if ';' in id:
                id_split = id.split(';')[-1]
            elif '#' in id:
                id_split = id.split('#')[-1] 
            elif '/' in id:
                id_split = id.split('/')[-1]
            else:
                print 'id without any condition: ', id       
#            print id_split
            vocabulary = id_split.split('_')[0]
            vocabs_dict[vocabulary] = 1
            
            name_match = name_pattern.search(owlClass)
            if name_match:
                name = name_match.group(1)
                nameCount += 1
#            print name
         
            obsolete_match = obsolete_pattern.search(owlClass)
            if obsolete_match:
                disObsoleteCount += 1
#                print id, name, 'OBSOLETE TERM'
            else:
                disActiveCount += 1  
 
                citation_matches = citation_pattern.finditer(owlClass)
                if citation_matches:
                    for citation_match in citation_matches:
                        citations += 1
                        citation = citation_match.group(1)
                        namespace = citation_match.group(2)
                        citation_id = citation_match.group(3)
                        mapping_id = namespace + ':' + citation_id
#                        print "MAPPING: ",citation, " ",namespace , ":",citation_id, " ",id, " ", name
                        if 'UMLS' in mapping_id:
                            if 'EFO' in id_split:
                                #efo2umls_dict[id_split] = mapping_id
                                utils.add_elem_with_dictionary(efo2umls_dict,id_split,mapping_id)
#                                print id_split, " ", mapping_id
                                umls2efo2name_file.write("%s\t%s\t%s\n" % (mapping_id,id_split,name))
                            else: 
                                #vocab2umls_dict[id_split] = mapping_id
                                utils.add_elem_with_dictionary(vocab2umls_dict,id_split,mapping_id)
                                umls2id2name_file.write("%s\t%s\t%s\n" % (mapping_id,id_split,name))
                             
                xref_matches = xref_pattern.finditer(owlClass)
                if xref_matches:
                    for xref_match in xref_matches:
                        xrefs += 1
                        xref_tag = xref_match.group(1)
                        xref_id = xref_match.group(2)
                        xref = xref_tag + ":" + xref_id
#                        print "MAPPING: ", xref, " ",id, " ", name
                        if 'UMLS' in xref:
                            if 'EFO' in id_split:
                                #efo2umls_dict[id_split] = xref
                                utils.add_elem_with_dictionary(efo2umls_dict,id_split,xref)
#                                print id_split, " ", xref
                                umls2efo2name_file.write("%s\t%s\t%s\n" % (xref,id_split,name))
                            else: 
                                #vocab2umls_dict[id_split] = xref
                                utils.add_elem_with_dictionary(vocab2umls_dict,id_split,xref)
#                                print id_split, " ", xref
                                umls2id2name_file.write("%s\t%s\t%s\n" % (xref,id_split,name))
                                
            if id_split not in efo2umls_dict and id_split not in vocab2umls_dict:
                id_withoutcui += 1
            else:
                id_withcui += 1
                
                
                       
            
        id = 'NA'
        name = 'NA'
        citation = 'NA'
        xref = 'NA'
        citation_matches = []
             
    print "Script has ended correctly. Please, find output at: %s%s. Remember to remove manually the last entry label." % (path,out_file)   
    print ""
    print ""
    print "Number of fragments :", numFragments     
    print "Number of IDs: ", dis
    print "Number of ID Names: ", nameCount
    print "Number of Obsolete IDs: ", disObsoleteCount
    print "Number of Active IDs: ", disActiveCount
    print "Number of ID2CITATIONS mappings: ",citations
    print "Number of ID2XREF mappings: ",xrefs
    print "Number of id with umls mapping: ", id_withcui 
    print "Number of id without umls mapping: ", id_withoutcui
    print "Vocabularies in EFO: ", vocabs_dict.keys()
    print "Number of EFO terms with UMLS mapping: ", len(efo2umls_dict)
    print "Number of vocabulary terms other than EFO with UMLS mapping: ", len(vocab2umls_dict)
 
    umlsMaps = 0
    vocabs2umlsNum_dict = {}
    vocabs2vocabid_dict = {}
    for vocabulary in vocabs_dict:
        for vocabid in vocab2umls_dict:
            if vocabulary in vocabid:
                utils.add_elem_with_dictionary(vocabs2vocabid_dict,vocabulary,vocabid)
                for umls in vocab2umls_dict[vocabid]:
                    utils.add_elem_with_dictionary(vocabs2umlsNum_dict,vocabulary,umls)
#                print vocabulary, vocabid
#            else:
#                print "This ", vocabulary, vocabid, " doesn't have umls mappings."    
#        
    for vocabulary in vocabs2umlsNum_dict:
        print "This vocabulary:", vocabulary, "has mappings between ", len(vocabs2vocabid_dict[vocabulary]), "number of vocab_id to ", len(vocabs2umlsNum_dict[vocabulary]), " number of umls cuis."
#            print vocabulary
     
    umls2efo2name_file.close()
    umls2id2name_file.close()
    
    return



if __name__ == "__main__":


    try:
        path = "/home/nqueralt/workspace/disgenet2rdf_2015/in/"
        in_OWL_file = "efo.owl"

        #parsingOWL(path,in_OWL_file)
        parsingXrefOWL(path,in_OWL_file)

    except OSError:
        print "Some problem occurred....T_T"
        sys.exit() 
