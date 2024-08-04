############################################################################################################################################################
#Class: OBOEngine
#Funtion of class: It has two methods __init__ and goHashTable. goHashTable method accept 'gene_ontology_ext.obo' file an creates a hash table about relation#ship of various GOTerms.
#Method: goHashTable
#        input args => file name(OBO file format). For e.g='gene_ontology_ext.obo'                  
#        returns an object of hash that can be used in furhter analysis.
#Usage: Create an object of OBOEngine. Then using that object access the goHashTable method For e.g 
#       engine = OBOEngine()
#       GO_hash = engine.goHashTable('gene_ontology_ext.obo')
#       
#############################################################################################################################################################

import re
import os # REMOVE THIS LATER. Only for debugging
from python_diagnostics import *

class OBOEngine:

    def __init__(self,elements=[]):
        self.__elements={}
        for e in elements:
            self.__elements[e]=1

    def goHashTable(self,file_arg):
        self.file_arg = file_arg
        self.GO_hash = {}
        ids=0
        namespaces=''
        names =''
        defs = ''
        is_a =''
        is_a_str=[]
        consider_obj=[]
        alt_id_obj =[]
        rel_part=[]
        is_obs_str = []
        rep_by_str = []
        rel_regulate =[]
        id_pattern = re.compile('^id\:\W+GO\:(\w+)$')
        namespace_pattern = re.compile('^namespace\:\W+(.+)$')
        name_pattern = re.compile('^name\:\W+(.+)$')
        def_pattern = re.compile('^def\:\W+(.+)$')
        is_a_pattern = re.compile('^is_a\:\W+GO\:(\w+)\W+\!\W+(\w+)')
        is_obs_pattern = re.compile('^is_obsolete\:\W+true')
        is_rep_pattern = re.compile('^replaced_by\:\W+GO\:(\w+)\W*$')
        is_consider_pattern = re.compile('^consider\:\W+GO\:(\w+)\W*$')
        is_alt_pattern = re.compile('^alt_id\:\W+GO\:(\w+)\W*')
        is_relp_pattern = re.compile('^relationship\:\W+part\_of\W+GO\:(\w+)\W*\!')
        is_relg_pattern = re.compile('^relationship\:\W+regulates\W+GO\:(\w+)\W*\!')
        try:
           fh = open(self.file_arg)
           #import re
           for lines in fh:
              lines = lines.strip()
              exp = re.search('\W+',lines)

              if  exp:                
                 #if re.search('^id\:\W+GO\:(\w+)$',lines):
                 if id_pattern.search(lines):
                    strs = re.split('\:(\w+)$',lines)
                    ids = strs[1]
                    continue
                 #if re.search('^namespace\:\W+(.+)$',lines):
                 if namespace_pattern.search(lines):
                    strs = re.split('\:\W+(\w+)$',lines)
                    namespaces = strs[1]
                    continue
                 #if re.search('^name\:\W+(.+)$',lines):
                 if name_pattern.search(lines):
                    strs = re.split('\:\W+(.+)$',lines)
                    names = strs[1]
                    continue
                 #if re.search('^def\:\W+(.+)$',lines):
                 if def_pattern.search(lines):
                    strs = re.split('\:\W+(.+)$',lines)
                    defs = strs[1]
                    continue
                 #if re.search('^is_a\:\W+GO\:(\w+)\W+\!\W+(\w+)',lines):
                 if is_a_pattern.search(lines):
                    strs = re.split('^is_a\:\W+GO\:(\w+)\W+(.+)',lines,2)
                    is_a = strs[1]
                    is_a_str.append(is_a)
                    continue
                 #if re.search('^is_obsolete\:\W+true'',lines):
                 if is_obs_pattern.search(lines):
                    strs = re.split('\:\W+',lines)
                    is_obs = strs[1]
                    is_obs_str.append(is_obs)
                    continue
                 #if re.search('^replaced_by\:\W+GO\:(\w+)\W*$',lines):
                 if is_rep_pattern.search(lines):
                    strs = re.split('^replaced_by\:\W+GO\:(\w+)\W*',lines)
                    replaced_by = strs[1]
                    rep_by_str.append(replaced_by)
                    continue
                 #if re.search('^consider\:\W+GO\:(\w+)\W*$',lines):
                 if is_consider_pattern.search(lines):
                    strs = re.split('^consider\:\W+GO\:(\w+)\W*',lines)
                    consider = strs[1]
                    consider_obj.append(consider)
                    continue
                 #if re.search('^alt_id\:\W+GO\:(\w+)\W*',lines):
                 if is_alt_pattern.search(lines):
                    strs = re.split('^alt_id\:\W+GO\:(\w+)\W*',lines)
                    alt_id = strs[1]
                    alt_id_obj.append(alt_id)
                    continue
                 #if re.search('^relationship\:\W+part\_of\W+GO\:(\w+)\W*\!',lines):
                 if is_relp_pattern.search(lines):
                    strs = re.split('^relationship\:\W+part\_of\W+GO\:(\w+)\W*\!',lines)
                    relationship = strs[1]
                    rel_part.append(relationship)
                    continue
                 #if re.search('^relationship\:\W+regulates\W+GO\:(\w+)\W*\!',lines):
                 if is_relg_pattern.search(lines):
                    strs = re.split('^relationship\:\W+regulates\W+GO\:(\w+)\W*\!',lines)
                    regulate = strs[1]
                    rel_regulate.append(regulate)
                    continue
              else:
                 if ids:
                    self.GO_hash[ids]={'namespaces':namespaces,'names':names,'def':defs, 'is_a':is_a_str,'consider':consider_obj,'alt_id':alt_id_obj,'part_of':rel_part,'regulate':rel_regulate,'is_obsolete':is_obs_str,'replaced_by':rep_by_str}
                    is_a_str = []
                    consider_obj = []
                    alt_id_obj = []
                    rel_part = []
                    rel_regulate = []
                    is_obs_str = []
                    rep_by_str = []
                    continue
        except (IOError, TypeError):
           import sys
           print "NO such file exists:",self.file_arg
           print "Please enter a valid OBO file"
           sys.exit()
        else:
           fh.close()
        return self.GO_hash
   
    

############################################################################################################################################################
# Class Name : GOMethod
# Function   : It holds various method for Gene Ontology Analysis.
# Methods    :
#            __init__
#            args => accepts anything and used to create an object for GOMethod. It is constructor
#            usage => obj = GOMethod()
#
#            getParents(self,GO_hash,go_id)
#            args => GO_hash object of class OBOEngine, go_id object (GOTerms which includes only numerical part i.e other than GO:)
#            function => used to find the corresponding parent GOTerm ids for a given GO id.
#            output   => gives a list of GO ids
#            e.g      => method = GOMethod()
#                        GOTerms = method.getParents(GO_hash,'0003674')
#
#            getGOCommon(GO_hash,go_id1,go_id2)
#            args     => GO_hash object of class OBOEngine, go_id1( first GO id),go_id2 (second GO id)
#            function => finds the common GO parents between two GO ids
#            output   => returns a list of common parents
#            e.g      => method = GOMethod()
#                        GOCommon = method.getGOCommon(GO_hash,'0003674','0000345')
#
#            getId_AltId(self,GO_hash,go_id)
#            args     => GO_hash object of class OBOEngine, go_id (The GO id)
#            function => get the alternate ID of the given GO id.
#            output   => returns the alternate ID of the given GO id.
#            e.g      => method = GOMethod()
#                        alt_id = method.getId_AltID(GO_hash,'0003451')
#
#            getFile_go(GO_hash,file)
#            args     => GO_hash object of class OBOEngine, file (input *_preprocess_file.txt)
#            function => Parses out the input file. After parsing generates the output in following format:
#                        Gene Name                 GO Terms                                 GO Parents
#                        AT2G47850       '0003676', '0008150', '0008270'       '0005488', '0003674', '0043167', '0043169', '0046872', '0008150', '0046914'
#            output   => returns nothing. It prints out the output in the above format in the file 'gene_go.txt' in the same directory. Additionally, it prints out the list of GO ids  whose annotation definition was not available in current version of OBO file used. 
#            e.g      => method = GOMethod()
#                        method.getFile_go(GO_hash,'gene_association_preprocess_file.txt')
#
#            printRow_Col(self, file, GO_hash)
#            args     => file: The corresponding *_gene_go.txt file obtained from previous step.
#                        GO_hash : Object of class OBOEngine
#            function => gets the rownames (set of gene ids), colnames (set of GO ids) and indices of the unique GO ids.
#            output   => returns row names, column names and indices of column names.
#            e.g      => method = GOMethod()
#                        rownames, colnames, ind_go_hash = method.printRow_col("gene_association_gene_go.txt",GO_hash)
#
#            printCol(self, file_str, colnames, GO_hash)
#            printRow(self, file_str, rownames, GO_hash)
#            args     => file_str: The name of file
#                        colnames: list object obtained from previous function.
#                        rownames: list object obtained from previous function.
#                        GO_hash: object of class OBOEngine.
#            function => Helper function to print out the column names or the total unique GO ids (linked+parent terms) to the file *_colnames.txt. Used in tandem with printRow_Col() method in previous step.                          
#            
#            getSparseMat_alt(file,ind_go_hash)
#            Function => It use the input file generated by getFile_go method in the desired format. Another input argument is index of all goterms. as hash object. This function is called after getPrintCol_Row method.
#            args     => file, go_gene_list, go_parents_list
#            output   => prints the output in '*_sparse.txt' in format compatible with R/MATLAB (row numer   column number)
#
#INPUT FILE FORMATS RELATED FUNCTIONS:
#
#            randomInpParser(self, file, col_ind1, col_ind2, m_flag)
#            args     => file: The given TAB separated input file with gene ids and linked GO terms. See GOParGenPy webpage for details.
#                        col_ind1: single integer value or multiple integer values(separated by comma) that sepcifies the list of user defined gene id column col_ind2: The column number of GO terms linked to gene ids of col_ind1
#                        m_flag  : Header value that specifies whether the input file contains header. See the GOParGenPy webpage for detials.
#            output   => Parses the input file to *_preprocess_file.txt
#            function => See GOParGenPy tutorial webpage for details
#            
#            modelOrgParser(self, file, col_ind1, col_ind2, m_flag)
#            args     => file: The given TAB separated "species specific" annotation file. See GOParGenPy webpage for details.
#                        Rest other parameter same as previous
#            output   => Parses the input file to *_preprocess_file.txt.
#            function => See GOParGenPy tutorial webpage for details. 
#
#            uniProtParser(self, file, col_ind1, col_ind2, m_flag)
#            args     => file: TAB separated input file having format of UNIPROT-GOA annotation file.
#                        Rest other parameter same as previous.
#            output   => Parses the input file to *_preprocess_file.txt
#            function => See GOParGenPy tutorial webpage for details.
#            
############################################################################################################################################################

class GOMethod:
    parents =[]
    sorted_parents = {}
    alt_id = {}
    no_go = {}
    altid_flag_val = 't'

    def __init__(self,elements=[]):
        self.__elements={}
        for e in elements:
            self.__elements[e]=1

    def getParents(self,GO_hash,go_id):
        self.GO_hash= GO_hash
        self.go_id = go_id

        if self.go_id == '0008150' or self.go_id == '0003674' or self.go_id == '0005575':
            if not go_id in GOMethod.parents:
                GOMethod.parents.append(self.go_id)
        else:
            if self.GO_hash.has_key(self.go_id):
               keys =self.go_id
               if self.GO_hash[keys]['is_a']:
                  isA_go = self.GO_hash[keys]['is_a']
                  for e in isA_go:
                     GOMethod.parents.append(e)
                     self.getParents(self.GO_hash,e)

               if self.GO_hash[keys]['part_of']:
                  isA_part = self.GO_hash[keys]['part_of']
                  for e in isA_part:
                     GOMethod.parents.append(e)
                     self.getParents(self.GO_hash,e)

               if self.GO_hash[keys]['consider']:
                  isA_consider = self.GO_hash[keys]['consider']
                  for e in isA_consider:
                     GOMethod.parents.append(e)
                     self.getParents(self.GO_hash,e)
              # Added replaced_by on 06.10.2011
               if self.GO_hash[keys]['replaced_by']:
                  isA_replaced = self.GO_hash[keys]['replaced_by']
                  for e in isA_replaced:
                     GOMethod.parents.append(e)
                     self.getParents(self.GO_hash,e)
                
            else:
               print "Key not found, No parents available for GO:"+self.go_id
               if GOMethod.altid_flag_val=='t':
                  print "Looking for the alternate id ........."
                  flag = 0
                  for keys in self.GO_hash: #keys() removed
                     alt_id_tmp = self.GO_hash[keys]['alt_id']
                     for ele in alt_id_tmp:
                        if ele == self.go_id:
                           print "alternate id for GO:"+self.go_id,"is GO:"+keys,"\n"
                           flag = 1
                           GOMethod.alt_id[self.go_id] = keys
                           if self.GO_hash[keys]['is_a']:
                              isA_go = self.GO_hash[keys]['is_a']
                              for e in isA_go:
                                 GOMethod.parents.append(e)
                                 self.getParents(self.GO_hash,e)
                        
                           if self.GO_hash[keys]['part_of']:
                              isA_part = self.GO_hash[keys]['part_of']
                              for e in isA_part:
                                 GOMethod.parents.append(e)
                                 self.getParents(self.GO_hash,e)

                           if self.GO_hash[keys]['consider']:
                              isA_consider = self.GO_hash[keys]['consider']
                              for e in isA_consider:
                                 GOMethod.parents.append(e)
                                 self.getParents(self.GO_hash,e) 
                           if self.GO_hash[keys]['replaced_by']:
                              isA_replaced = self.GO_hash[keys]['replaced_by']
                              for e in isA_replaced:
                                 GOMethod.parents.append(e)
                                 self.getParents(self.GO_hash,e)
                  if flag ==0:
                     GOMethod.no_go[self.go_id] = 1
                     print "No alternate id found for GO:"+self.go_id,"\n" 
               #else:
                  #continue
                            
        for outer in GOMethod.parents:
            GOMethod.sorted_parents[outer]=1
        return GOMethod.parents

    def getGOCount(self,elements =[]):
        self.GO_count = {}
        self.temp_hash = {}

        fh = open("count_output.txt")

        pattern = re.compile('^GO\:(\w+)\W+')
        for lines in fh.readlines():
            lines = lines.strip()
            if pattern.search(lines):
                strs = re.split('^GO\:(\w+)\W+',lines)
                go_id = strs[1]
                count = strs[2]
                self.GO_count[go_id] = count

        for ele in elements:
            self.temp_hash[ele] = self.GO_count[ele]

        return self.temp_hash
        fh.close()
    
    def getId_AltId(self,GO_hash,go_id):
        
        self.tmp = []
        for keys in GO_hash:
           ele = GO_hash[keys]['alt_id']
           for e in ele:
              if e == go_id:
                 self.tmp=keys
        
        return self.tmp
           
   
    def getGOtermCount(self,file_arg):
       self.file_arg = file_arg
       self.go_gene_list = []
       self.go_parents_list = []
       self.go_gene_count = {}
       self.go_total_count = {}
       
       fh = open(self.file_arg)
       op =open('go_count.txt','w')
       ot = open('go_total.txt','w')
       for lines in fh:
          lines = lines.strip()
          if lines:
             strs = re.split("\t",lines)
             go_gene = re.split('\,',strs[1])
             for ele in go_gene:
                ele=ele.strip()
                self.go_gene_list.append(ele)
             go_parents = re.split('\,',strs[2])
             for ele in go_parents:
                ele = ele.strip()
                self.go_parents_list.append(ele)

       for ele in self.go_gene_list:
          self.go_parents_list.append(ele)

       for ele in self.go_gene_list:
          self.go_gene_count[ele] = self.go_gene_count.get(ele,0)+1
          print ele,"\t",self.go_gene_count[ele]
       
       for ele in self.go_parents_list:
          self.go_total_count[ele] = self.go_total_count.get(ele,0)+1

       
       for keys in self.go_gene_count.keys():
          print >>op,keys,"\t",self.go_gene_count[keys]
       for keys in self.go_total_count.keys():
          print >>ot,keys,"\t",self.go_total_count[keys]
       
       op.close()
       ot.close()

    def getGOCommon(self,GO_hash,go_id1,go_id2):
        self.GO_hash = GO_hash
        self.igo_id1 = go_id1
        self.go_id2 = go_id2
        parents1 = self.getParents(self.Go_hash, self.go_id1)
        parents2 = self.getParents(self.GO_hash, self.go_id2)
        self.common_parents = []

        for outer in parents1:
            for inner in parents2:
                if outer == inner:
                    self.common_parents.append(outer)

        return self.common_parents

    def MapGO_DictToParents(self,GO_hash,Gene_GO_Dict,file_arg, altid_val):

       # Create a code for taking dict and propagating GO classes to parents
       # Here comes something
       file_str = file_arg + '_gene_go.txt'
       op = open(file_str,'w')
       for gene_id in Gene_GO_Dict:
          parent_list = []
	  for go_id in Gene_GO_Dict[gene_id]:
	     
	     tmp = self.getParents(GO_hash, re.sub("^GO\:","", go_id))
	     if len(tmp) > 0:
	        parent_list.extend(tmp) 
	  parent_list = list(set(parent_list))
	  print >>op, gene_id,"\t",','.join(Gene_GO_Dict[gene_id]),"\t",','.join(parent_list) 
       op.close

    def getFile_go(self,GO_hash,file_arg,altid_val):
       self.file_arg = file_arg
       self.GO_hash =GO_hash
       self.go_lib ={}
       GOMethod.altid_flag_val = altid_val

       tmp = re.split('\_preprocess_file\.txt',self.file_arg)
       file_str = tmp[0]+'_'+'gene_go.txt'
       file_no_go = tmp[0]+'_'+'no_go.txt'
       
       op = open(file_str,'w')
       ng = open(file_no_go,'w')
       
       gene_id_list = []
       self.gene_go_hash = {}
       
       fh = open(self.file_arg)

       parents_list =[]
      
       self.go_lib = {}
       no_go = []

       lines = fh.readline()
       while lines:
          lines = lines.strip()
          exp = re.split('\t',lines)
          self.comb_parents = {}
          if exp:
             gene_id = exp[0].strip()
             gene_id_list.append(gene_id)
             if len(exp)>1:
                gene_go = re.split('\s|,|;',exp[1])
             else:
                gene_go = []
             list_go = []
             for ele_go in gene_go:
                ele_go = ele_go.strip()
                if ele_go:
                   exp = re.split("\:",ele_go)
                   element = exp[1]
                   list_go.append(element)
                   if self.go_lib.has_key(element):
                      parents_list = self.go_lib[element]
                      for ele in parents_list:
                         self.comb_parents[ele]=1
                      parents_list = []
                   else:
                      if not GOMethod.no_go.has_key(element):
                         try:
                            parents_list = self.getParents(self.GO_hash,element)
                            if parents_list:
                               self.go_lib[element] = parents_list
                               for ele in parents_list:
                                  self.comb_parents[ele] = 1
                            else:
                               no_go.append(element)
                         except IndexError:
                            print "Error occurred!",element
                         GOMethod.parents = []
                         GOMethod.sorted_parents = {}
                         parents_list = []
             if self.comb_parents:
                print >>op,gene_id,"\t",','.join(list_go),"\t",','.join(self.comb_parents.keys())
             else:
                print >>op,gene_id,"\t",','.join(list_go),"\t"
          lines = fh.readline()   
       if GOMethod.no_go:
          for keys in GOMethod.no_go:
             print >>ng,keys
       self.comb_parents = {}
       GOMethod.no_go = {}
       op.close()
       ng.close()
       fh.close()

    def printRow_Col(self,file_arg,GO_hash): 

       self.file_arg = file_arg
       self.gene_name = {}
       self.go_gene = {}
       self.go_parents = {}
       self.go_list = {}
       self.ind_go = {}
       import re

       tmp = re.split("\_gene\_go\.txt",file_arg)
       file_str = tmp[0]

       fh = open(self.file_arg)
       gene_count = 0
       lines = fh.readline()
       while lines:
          lines = lines.strip()
          if lines:
             strs = re.split("\t",lines)
             gene = strs[0].strip()
             self.gene_name[gene_count] = gene
	     if len(strs)>1:
                go_gene = re.split('\,',strs[1])
                for ele in go_gene:
                   ele = ele.strip()
                   if ele:
                      self.go_list[ele] = 1
             if len(strs)==3:
                go_parents = re.split('\,',strs[2])
                for ele in go_parents:
                   ele = ele.strip()
                   if ele:
                      self.go_list[ele] = 1
             gene_count += 1
          lines = fh.readline()
       gene_list = self.gene_name.values()
       comb_go = self.go_list.keys()
       #print "sub-function: print rows cols"
       for ele in comb_go:
          self.ind_go[ele] = comb_go.index(ele)+1
       rownames = gene_list
       colnames = comb_go
       self.printRowPT(file_str,rownames)
       self.printCol(file_str,colnames,GO_hash)
       fh.close()
       return rownames,colnames,self.ind_go

    def getSparseMat_alt(self,file_arg,ind_go_hash):
       #import re
       self.file_arg = file_arg
       fh = open(self.file_arg)
       tmp = re.split("\_gene\_go\.txt",self.file_arg)
       file_str = tmp[0]
       sp = open(file_str+'_'+'sparse.txt','w')
       row_ind_count = 0
       lines = fh.readline()
       while lines:
          row_ind_count = row_ind_count + 1
          lines = lines.strip()
          go_hash = {}
          if lines:
             strs = re.split("\t",lines)
             gene = strs[0].strip()
             if len(strs) > 1:
                go_gene = re.split("\,",strs[1])
                #print go_gene
                for ele in go_gene:
                   ele = ele.strip()
                   if ele:
                      go_hash[ele]=1
             if len(strs) ==3:
                go_parents = re.split("\,",strs[2])
                for ele in go_parents:
                   ele = ele.strip()
                   if ele:
                      go_hash[ele]=1
          for elem in go_hash:#keys() removed
             ind = ind_go_hash[elem]
             print >>sp,row_ind_count,"\t",ind
          lines = fh.readline()
       ind_go_hash = {}
       fh.close()
       sp.close()
    

    def printCol(self,file_str,colnames,GO_hash):
       
       fh = open(file_str+'_'+'colnames.txt','w')
       exp = []
       for ele in colnames:
          ele = ele.strip() 
          if GO_hash.has_key(ele):
             exp = GO_hash[ele]['namespaces']
             if exp == 'biological_process':
                print >>fh,ele,"\t","BP:",ele,":",GO_hash[ele]['names']
             elif exp == 'molecular_function':
                print >>fh,ele,"\t","MF:",ele,":",GO_hash[ele]['names']
             elif exp == 'cellular_component':
                print >>fh,ele,"\t","CC:",ele,":",GO_hash[ele]['names']
          elif GOMethod.alt_id.has_key(ele):
             alt_ele = GOMethod.alt_id[ele]
             exp = GO_hash[alt_ele]['namespaces']
             if exp == 'biological_process':
                print >>fh,ele,"\t","BP:",alt_ele,":",GO_hash[alt_ele]['names']
             elif exp == 'molecular_function':
                print >>fh,ele,"\t","MF:",alt_ele,":",GO_hash[alt_ele]['names']
             elif exp == 'cellular_component':
                print >>fh,ele,"\t","CC:",alt_ele,":",GO_hash[alt_ele]['names']
          else:
             print >>fh,ele,"\t","NO ANNOTATION"
       GO_hash = {}
       fh.close()
   
    def printRow(self,file_str,rownames):
       
       fh = open(file_str+'_'+'rownames.txt','w')
       #print "printRow sub-function"
       #import re
       for ele in rownames:
          strs = re.split("\|\|",ele)
          for e in strs:
             print >>fh,e.strip()#,"\t",
          #print >>fh
       fh.close()
 
    def printRowPT(self,file_str,rownames):
    
       # PT documented out a split command (\|\|)   
       fh = open(file_str+'_'+'rownames.txt','w')
       #import re
       row_count = 0
       for ele in rownames:
          row_count = row_count + 1
	  #strs = re.split("\|\|",ele)
	  ele = re.sub("\|\|", "\t", ele)
	  print >>fh,ele.strip()#,"\t",
          #for e in strs:
          #   print >>fh,e.strip()#,"\t",
          ##print >>fh
       print "row count sub-function: "+ str(row_count)
       fh.close()

    def headerCheck(self,lines,col_ind1,col_ind2):
       header = ''
       #import re
       try:
          strs = re.split("\t",lines)
          if strs[col_ind2]:
             exp = re.search('GO\:(\d+)',strs[col_ind2])
             if exp :
                print strs[col_ind2]
                header = 'F'
             else:
                header = 'T'
          else:
             header ='F'
       except IndexError:
          print "The file is not tab separated or Column Index doesnot exist"
       return header

    def randomInpParser(self,file_arg,col_ind1,col_ind2,m_flag,file_out):
       self.file_arg = file_arg
       self.file_out = file_out
       gene_hash = {}
       go_id = []
       
       #import re
       import sys
       col_ind1_str = re.split("\,",col_ind1)
       col_ind2 = int(col_ind2) -1
       
       file_str = self.file_out+'_'+'preprocess_file.txt'
       try:
          wh = open(file_str,'w')
          fh = open(self.file_arg)
          count = 0
          #import re
          lines = fh.readline()
          header = self.headerCheck(lines,col_ind1,col_ind2)
          if m_flag.lower() =='t' and  header.lower() =='t':
             lines = fh.readline()
          elif m_flag.lower() =='f' and header.lower() =='t':
             print "The entered header flag value",m_flag," is incorrect"
             print "The file contains header"
             print "Removing the header from the file\n\n"
             lines = fh.readline()
          elif m_flag.lower() =='t' and header.lower() =='f':
             print "The entered header flag value",m_flag,"is incorrect"
             print "The file doestnot have any header\n\n"
          
          while lines:
             col_ind1 = ''
             lines = lines.strip()
             if lines:
                strs = re.split("\t",lines)
                for e in col_ind1_str:
                   e = e.strip()
                   e = int(e)-1
                   col_ind1 = col_ind1+"||"+strs[e]
                col_ind1 = str(col_ind1.split('||',1)[1].strip())
                if gene_hash.has_key(col_ind1):
                   go_id = gene_hash[col_ind1]
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)
                   except IndexError:
                      go_id = []
                      go_id.append(go_id)
                   gene_hash[col_ind1] = go_id
                   go_id = []
                else:
                   go_id = []
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)
                   except IndexError:
                      go_id = []
                   gene_hash[col_ind1] = go_id
             lines = fh.readline()
          for keys in gene_hash.keys():
             tmp = {}
             go_list = gene_hash[keys]
             for ele in go_list:
                tmp[ele]=1
             go_list = tmp.keys()
             print >>wh,keys,"\t",','.join(go_list)
          fh.close()
          wh.close()
       except IOError:
          print "ERROR! Could not open the input file"
          sys.exit()
       except IndexError:
          print "ERROR! The gene id column index doesnot exist"
          sys.exit()
       except ValueError:
          print "ERROR! The column index is inappropriate. Please enter an Integer value"
          sys.exit()
    
    def ParseGO_ID(self, input_str, GO_ID_col, separ = "\t"):
       # PT addition 
       strs = re.split(separ,input_str) 
       if len(strs) > GO_ID_col and strs[GO_ID_col].strip():
          if re.search('(GO\:\d{7})',strs[GO_ID_col]):
            go_id_tmp = re.split('(GO\:\d{7})',strs[GO_ID_col])
	    go_id_tmp = [ s.strip() for s in go_id_tmp ]
	    output    = filter(bool, go_id_tmp) 
	  else:
	    print "sub-function ParseGO_ID"
	    print "GO data did not match the required GO syntax"
	    print  "Analyzed field was " + strs[GO_ID_col]
	    raise Exception, "GO data did not match the pattern"
       else:	# Here process empty fields
          output = []
       return output

    def modelOrgParserPT(self, file_arg, col_ind1, col_ind2, file_out,
                         comment_chars = "\!\#", header_count = 0, ReturnDict = False):
       # Petri Modified...
       # Redoing this code. Using sub-function for GO processing
       # file_arg 	name of the input file
       # col_ind1	gene-ID columns. Separate with comma, if many columns
       # col_ind2	GO class ID column
       # file_out	name of temporary file
       # comment_chars	these are used to filter comment rows from the start (default "\!\#")
       # header_count	This is used to filter header rows from the beginning (default 0)
       # ReturnDict	Do we return a dict or print to the results to file 
       #self.file_arg = file_arg
       #self.file_out = file_out
       col_ind2 = int(col_ind2) -1
       gene_hash = {}
       go_id = []
       col_ind1_list = re.split("\,",col_ind1)
       file_str = file_out+'_preprocess_file.txt'
       try:
          f_out = open(file_str,'w')
       except IOError:
          print "ERROR! Could not open the file " + file_str
          sys.exit()
       if not ReturnDict:
          try:	  
             f_in = open(file_arg, "r")
          except IOError:
             print "ERROR! Could not open the file " + file_arg
             sys.exit()
       counter = 0
       try:	  
          for line in f_in:
	     counter = counter + 1
             gene_ID = ''
             line = line.strip()
             exp = re.search("^["+comment_chars+"]",line)
             if not exp and counter > header_count:   #Filter by count and by comment char
                strs = re.split("\t",line)
                for e in col_ind1_list:
                   e = e.strip()
                   e = int(e)-1
		   if gene_ID:
                     gene_ID = gene_ID +"||"+strs[e]
		   else:
		     gene_ID = strs[e]
		tmp_GO_ID = self.ParseGO_ID(line, col_ind2)
		if gene_hash.has_key(gene_ID):
		   gene_hash[gene_ID].extend(tmp_GO_ID)
		else:
		   gene_hash[gene_ID] = tmp_GO_ID
       except ValueError:
          print "ERROR! The column index is in appropriate. Please enter an Integer value"
          raise Exception
       except IndexError:
          print "ERROR!The column index for gene id doesnot exist."
          raise Exception
       # Code could return the gene-GO classes Dict
       # instead of writing it to a file.  
       if ReturnDict:
          return gene_hash
       else:        
          for gene in gene_hash:
             go_list = list(set(gene_hash[gene]))
	     gene_hash[gene] = go_list
	     print >>f_out,gene,"\t",','.join(go_list)
	  f_out.close()
       f_in.close()
           
       
    def modelOrgParser(self,file_arg,col_ind1,col_ind2,m_flag,file_out):
       # weird processing is done because col_ind1 can include many columns
       # 
       self.file_arg = file_arg
       self.file_out = file_out
       col_ind2 = int(col_ind2) -1
       gene_hash = {}
       go_id = []
       col_ind1_str = re.split("\,",col_ind1)
       file_str = self.file_out+'_'+'preprocess_file.txt'
       print_variables2(vars())
       print file_arg
       print self.file_arg
       try:
          wh = open(file_str,'w')
          fh = open(self.file_arg)
          lines = fh.readline()
          while lines:
             col_ind1 = ''
             lines = lines.strip()
             exp = re.search("^\!",lines)
             if not exp:
                strs = re.split("\t",lines)
                for e in col_ind1_str:
                   e = e.strip()
                   e = int(e)-1 
                   col_ind1 = col_ind1+"||"+strs[e]
                col_ind1 = str(col_ind1.split('||',1)[1].strip())
                if gene_hash.has_key(col_ind1):
		   #print "here"
                   go_id = gene_hash[col_ind1]
		   
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)
		      # Above Ajays code creates empty fields
		      # those are filtered
                   except IndexError:
                      go_id = []
                      #go_id.append(go_id)
                   gene_hash[col_ind1] = go_id
                   go_id = []
                else:
                   go_id = []
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)
                   except IndexError:
		      #print "second exception"
                      go_id = []
                   gene_hash[col_ind1] = go_id
             lines = fh.readline()
          for keys in gene_hash:
             tmp = {}
             go_list = gene_hash[keys]
             for ele in go_list:
                tmp[ele] = 1
             go_list = tmp.keys()
	     print >>wh,keys,"\t",','.join(go_list)
          fh.close()
          wh.close()
       except IOError:
          print "ERROR! Could not open the file"
          sys.exit()
       except IndexError:
          print "ERROR!The column index for gene id doesnot exist."
          sys.exit()
       except ValueError:
          print "ERROR! The column index is in appropriate. Please enter an Integer value"
          sys.exit()
          
       
    def uniProtParser(self,file_arg,col_ind1,col_ind2,m_flag,file_out):
       self.file_arg = file_arg
       self.file_out = file_out
       col_ind2 = int(col_ind2) -1
       gene_hash = {}
       go_id = []
       col_ind1_str = re.split("\,",col_ind1)
       file_str = self.file_out+'_'+'preprocess_file.txt'
       try:
          wh = open(file_str,'w')
          fh = open(self.file_arg)
          lines = fh.readline()
          while lines:
             col_ind1 = ''
             lines = lines.strip()
             exp =  re.search("^\!",lines)
             if not exp:#else:
                strs = re.split("\t",lines)
                for e in col_ind1_str:
                   e = e.strip()
                   e = int(e) -1
                   col_ind1 = col_ind1+"||"+strs[e]
                col_ind1 = str(col_ind1.split('||',1)[1].strip())
                if gene_hash.has_key(col_ind1):
                   go_id  = gene_hash[col_ind1]
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)                             
                   except IndexError:
                      go_id_tmp = []
                      go_id.append(go_id_tmp)
                   gene_hash[col_ind1] = go_id
                else:
                   go_id = []
                   if gene_hash:
                      for keys in gene_hash.keys():
                         tmp = {}
                         go_list = gene_hash[keys]
                         for ele in go_list:
                            tmp[ele] = 1
                         go_list = tmp.keys()
                         print >>wh,keys,"\t",','.join(go_list)
                   gene_hash = {}
                   try:
                      go_id_tmp = re.split('(GO\:\d{7})',strs[col_ind2])
                      for ele in go_id_tmp:
                         inp = re.search('GO\:\d{7}',ele)
                         if inp:
                            go_id.append(ele)
                   except IndexError:
                      go_id = [] 
                   gene_hash[col_ind1] = go_id
             lines = fh.readline()

          for keys in gene_hash:
             go_list = gene_hash[keys]
             print >>wh,keys,"\t",','.join(go_list)
          fh.close()
          wh.close()
       
       except IOError:
          print "ERROR! Could not open the file"
          sys.exit()
       except IndexError:
          print "ERROR! The column Index for gene id is incorrect"
          sys.exit()
       except ValueError:
          print "ERROR! The column index is in appropriate. Please enter an Integer value"
          sys.exit()
       
    def getFullMat(self,file_arg,rownames,colnames,ind_go_hash):   
 
       self.file_arg = file_arg
       self.matrix = []
       row_count = 0
 
       for i in range(len(rownames)):
          ea_row = []
          for j in range(len(colnames)):
             ea_row.append(0) 
          self.matrix.append(ea_row)
       
       fh = open(self.file_arg)
       for lines in fh:
          lines = lines.strip()
          if lines:
             strs = re.split("\t",lines)
             try:
                go_gene = re.split("\,",strs[1])
             except IndexError:
                go_gene = []
             for ele in go_gene:
                ele=ele.strip()
                if ele:
                   index = ind_go_hash[ele]
                   self.matrix[row_count][index -1]=1
             try:
                go_parent = re.split("\,",strs[2])
             except IndexError:
                go_parent = []
             for ele in go_parent:
                ele=ele.strip()
                if ele:
                   index = ind_go_hash[ele]
                   self.matrix[row_count][index -1]=1
          row_count = row_count+1 
       
       return self.matrix

    def ReorderDataTable(self, file1, file2, ID_col1, ID_col2, GO_col,
                         header1 = 0, header2 = 0, split_char = "\t", 
			 NoGeneSTR = "NA", file_out = ""):
       # Code reads in the GO-annotations in file1 (using ID_col1 and GO_col)
       # Next it reads file2 and collects the IDs.
       # After this the data in file1 is printed in the same order
       # as data is in file2
       #
       # ReorderDataTable(self, file1, file2, ID_col1, ID_col2, GO_col,header1 = 0, header2 = 0, file_out = "")
       #  Where:
       # file1		GO data anotation table (this is re-ordered)
       # file2		RNAseq, microarray (or what ever) data table. This is used to order GO
       # ID_col1	Gene ID column for file1. Numbering starts with 0
       # ID_col2	Gene ID column for file2. Numbering starts with 0
       # GO_col		GO ID column for file2. Numbering starts with 0
       # header1	number of header rows for file 1 (default = 0)
       # header2	number of header rows for file 2 (default = 0)
       # NoGeneSTR	String used if Gene Name field is empty. Default is "NA"
       # file_out	File for reordered GO data. Function overwrites file1 if file_out = ""
       # ExactMatch     True  = Identifiers must match exactly
       #                False = Partial match to ID in file1 to ID in file2 is allowed
       # NOTE: define file_out for debug purpose. Code overwrites file1 if file_out = ""
       #
       # PT added this code
       #
       # This is little silly code. This prints result to text file
       # We shoulf rather read the data into the program and process that
       try:
         FileRead = open(file1, "r")
       except IOError:
         print "Function ReorderDataTable fails"
	 print "cannot open "+ file1
	 raise Exception
       if not file_out:
         file_out = file1
       # Check how many name fields we have
       # assume:
       # Different name fields are merged together with "||"
       tmp_str = FileRead.readline()
       tmp_str = tmp_str.split(split_char)[ID_col1]
       tmp_len = len(re.split("\|\|",tmp_str))
       #GO_anno_dict = {}
       GO_dict_list = [{} for i in range(tmp_len)]
       FileRead.close

       FileRead = open(file1, "r")
       row_count = 0
       Split_GO_chars = "."
       for line in FileRead:	# Read the GO data in 
         row_count = row_count + 1
	 if row_count > header1:
	   split_array = line.split(split_char)
	   if len( split_array) >= GO_col and \
	   split_array[GO_col].strip():  # Check if field exists 	      
	        GO_data = split_array[GO_col].strip()
	   else: 
	        GO_data = ""
	   if len( split_array) >= ID_col1:    
	     #print split_array[ID_col1]
	     tmp_str = split_array[ID_col1].strip()
	     tmp_tab = re.split("\|\|",tmp_str)
	     for i in range(len( tmp_tab)):
	        # GO merges ID's like abc|cde in synonyms
		# below I select the first one to test
	        tmp_str2 = tmp_tab[i].strip()
		tmp_tab2 = tmp_str2.split("|")
	        GO_dict_list[i][tmp_tab2[0]] = GO_data
	     #GO_dict[ split_array[ID_col1].strip()] = GO_data 
	     #print GO_data
	     #print row_count
           else:
	     print " Function ReorderDataTable fails" 
	     print " cannot process row " + str(row_count)
	     print line
	     print " No ID field!!"
	     raise Exception
       FileRead.close()	
       
       try:
          FileRead = open(file2, "r")
       except IOError:
          print "Function ReorderDataTable fails"
	  print "cannot open "+ file2
	  raise Exception
       
       try:
          FileOut = open(file_out, "w")
       except IOError:
          print "Function ReorderDataTable fails"
       	  print "cannot write to "+ FileOut
       	  raise Exception

       row_count2 = 0
       match_count = 0
       mismatch_count = 0
       #Data_Out = []		#This could export data to python
       for line in FileRead:
         row_count2 = row_count2 + 1
	 if row_count2 > header2:
	   split_array = line.split(split_char)	   
	   if len( split_array) >= ID_col2:
              Data_str = split_array[ID_col2].strip()	
	      #tmp_list = Data_str.split(" || ")
	      check_match = 0
	      if Data_str:
	        for i in range(len(GO_dict_list)):
		  if Data_str in GO_dict_list[i]:
		     #tmp_tmp = GO_dict_list[i][Data_str]
		     Data_str = Data_str + "\t" + GO_dict_list[i][Data_str]
		     match_count = match_count + 1
		     check_match = 1
	      if not Data_str or check_match == 0:
	        if not Data_str:   # Gene name field is empty in Reorder data
		   Data_str = NoGeneSTR #Tassa
	        Data_str = Data_str + "\t"
		mismatch_count = mismatch_count + 1
	      FileOut.write( Data_str + "\n" )
	      #Data_Out.append( Data_str )
           else:
	     print " Function ReorderDataTable fails "+ file2 
	     print " cannot process row " + str(row_count)
	     print line
	     print len(split_array) 
	     print " No ID field!!"
	     raise Exception

       #print_variables2(vars())	      
       print "Processing steps in ReorderDataTable done"
       print "There was "+ str(match_count) +" Matching IDs"
       print "There was "+ str(mismatch_count) +" IDs without match"	
       print "First table was " + str(row_count) + " rows"
       print "Second was " + str(row_count2) + " rows" 

    def ReorderDataTable2(self, file1, file2, ID_col1, ID_col2, GO_col,
                         header1 = 0, header2 = 0, split_char = "\t", 
			 NoGeneSTR = "NA", file_out = ""):
       # Code reads in the GO-annotations in file1 (using ID_col1 and GO_col)
       # Next it reads file2 and collects the IDs.
       # After this the data in file1 is printed in the same order
       # as data is in file2
       #
       # PT added this code
       #
       # This is little silly code. This prints result to text file
       # We shoulf rather read the data into the program and process that
       #
       # This is modified to process multiple gene IDs from one row. Artefact of one data
       try:
         FileRead = open(file1, "r")
       except IOError:
         print "Function ReorderDataTable fails"
	 print "cannot open "+ file1
	 raise Exception
       if not file_out:
         file_out = file1
       GO_anno_dict = {}
       row_count = 0
       Split_GO_chars = "."
       for line in FileRead:	# Read the GO data in 
         row_count = row_count + 1
	 if row_count > header1:
	   split_array = line.split(split_char)
	   if len( split_array) >= GO_col and \
	   split_array[GO_col].strip():  # Check if field exists 	      
	        GO_data = split_array[GO_col].strip()
	   else: 
	        GO_data = ""
	   if len( split_array) >= ID_col1:    
	     #print split_array[ID_col1]
	     GO_anno_dict[ split_array[ID_col1].strip()] = GO_data 
	     #print GO_data
	     #print row_count
           else:
	     print " Function ReorderDataTable fails" 
	     print " cannot process row " + str(row_count)
	     print line
	     print " No ID field!!"
	     raise Exception
       FileRead.close()	
       
       print_some_dict( GO_anno_dict )
              
       try:
          FileRead = open(file2, "r")
       except IOError:
          print "Function ReorderDataTable fails"
	  print "cannot open "+ file2
	  raise Exception
         
       try:
          FileOut = open(file_out, "w")
       except IOError:
          print "Function ReorderDataTable fails"
       	  print "cannot write to "+ FileOut
       	  raise Exception

       row_count2 = 0
       match_count = 0
       mismatch_count = 0
       #Data_Out = []
       for line in FileRead:
         row_count2 = row_count2 + 1
	 if row_count2 > header2:
	   split_array = line.split(split_char)	   
	   if len( split_array) >= ID_col2:
              Data_str = split_array[ID_col2].strip()	
	      tmp_list = Data_str.split(" || ")
	      #print len( tmp_list)
	      #print tmp_list
	      #afgafgaf     
	      GO_str = ""
	      for ID in tmp_list:
	        if ID and ID in GO_anno_dict:
	          GO_str = GO_str + "," + GO_anno_dict[ID]
	          #Data_str = Data_str + "\t" + GO_anno_dict[ID]
	      #match_count = match_count + 1
	      #else:
	      #  Data_str = Data_str + "\t"
	      if not Data_str: # Gene name field is empty in Reorder data
	        Data_str = NoGeneSTR #Tassa
	      if GO_str:
	        match_count = match_count + 1
	      else:
	        #print Data_str
		#print tmp_list
	      	mismatch_count = mismatch_count + 1
              Data_str = Data_str + "\t" + GO_str
	      FileOut.write( Data_str + "\n" )
	      #Data_Out.append( Data_str )
           else:
	     print " Function ReorderDataTable fails "+ file2 
	     print " cannot process row " + str(row_count)
	     print line
	     print len(split_array) 
	     print " No ID field!!"
	     raise Exception
	      
       FileOut.close()
       FileRead.close()
       print "first processing steps in ReorderDataTable done"
       print "There was "+ str(match_count) +" Matching IDs"
       print "There was "+ str(mismatch_count) +" IDs without match"	   
       print_variables2(vars())
