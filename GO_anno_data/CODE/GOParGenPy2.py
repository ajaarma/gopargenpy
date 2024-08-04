#!\usr\bin\python

################################################################################
#                                                                              #
#GOParGenPy: A High Throughput method to generate Gene Ontology data matrices  #
#Copyright (C) 2012 Holm Group, University of Helsinki                         #
#                                                                              #
#author: Ajay Anand Kumar (firstname.lastname@helsinki.fi                      #                                                
#Radically edited by Petri Toronen (2017)                                                                             #
################################################################################



import time
import sys
import re
from GeneOntology3 import * 
from python_diagnostics import *
import argparse
from argparse import RawTextHelpFormatter

if __name__=="__main__":
   """
   command = sys.argv
   if re.search("\-help",",".join(command)):
      #if hlp_ind:
      print "\n"
      print "***COMMAND***"
      print "$ python   GOParGenPy   -obo obo_file   -i  [input_value]  -h  [header_value] -a [altid_value]  user_annotation_file_name -o output_file_name   -m   gene_col_num   GO_col_num    mat_flag"
      print "\n"
      print "***Parameters Description***\n"
      print "obo_file                  :  Standard Gene Ontology OBO file"
      print " -i                       :  input file format flag"
      print "input_value               :  Integer Value 1, 2, 3. For individual types see GOParGenPy webpage for further details"
      print "                             1 : For user defined tab separated input annotation file"
      print "                             2 : For species specific annotation file"
      print "                             3 : For UNIPROT-GOA file"
      print " -h                       :  header flag for the input file"
      print "header_value              :  Boolean Type T or F"
      print " -a                       :  Alternate id flag for the GO ids"
      print "altid_value               :  Boolean Type T or F"
      print "user_annotation_file_name :  Input annotation file. File should only be TAB (\\t) separated"
      print " -o                       :  The output file parameter [OPTIONAL]"
      print "output_file_name          :  User specific name for the all the output. If no given INPUT file name will be used"
      print "-m                        :  Matrix parameters flag"
      print "gene_col_num              :  The column number(s) of the tab separated annotation file that contains gene ids and other descriptors. E.g. 2,4,5,6 or just 2"
      print "GO_col_num                :  The column number(singular value) of tab separated annotation file that contains GO IDs."
      print "mat_type                  :  S or F. S for sparse matrix and F for full binary matrix"
      print "\n"
      print "See GOParGenPy webpage for detailed usage "
      print " http://ekhidna.biocenter.helsinki.fi/users/ajay/private/GOParGenPy/GOParGenPy/ "
      print "\n"
      sys.exit()
   """
   # Following methods are represented here:
   # argparse:
   # https://docs.python.org/3/howto/argparse.html
   # Integer lists:
   # https://stackoverflow.com/questions/15459997/passing-integer-lists-to-python
   # Help text with new line:
   # https://stackoverflow.com/questions/29613487/multiple-lines-in-python-argparse-help-display
   # https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
   
   parser = argparse.ArgumentParser(description='Generate GO annotation data matrix',
               usage='python GOParGenPy2.py   -obo obo_file -i input_file  -form input_form  -h [header_value] -o output_name -Ncol GeneID_col -GOcol GO_ID_col -alt [altid_value]   -m mat_flag',
               formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument("-obo",  "--OBO_file", help = "Standard Gene Ontology OBO file")
   parser.add_argument("-form", "--FormIn",   help = "Define Annotation data type\n" + \
                                                     "1 : For user defined tab separated input annotation file \n" + \
					             "2 : For species specific annotation file \n" + \
						     "3 : For UNIPROT-GOA file \n" + \
						     "4 : For BioMART output file (not well tested)" , type=int, choices=[1, 2, 3, 4])
   parser.add_argument("-i",    "--Input",    help = "File containing gene annotations")
   parser.add_argument("-hder", "--Header",   help = "Does input have a header. Default is T",  choices=["T","F"], default="T")
   parser.add_argument("-Ncol", "--NameCol",  help = "Column containing gene ID. Can include many columns", nargs='+', type=int)
   parser.add_argument("-GOcol","--GO_Col",   help = "Column containing GO ID. Can include only one column", type=int)
   parser.add_argument("-o",    "--Output",   help = "Output file base name. Actual output files extend from this.", default = "")
   parser.add_argument("-m",    "--MatrForm", help = "Form of output matrix (full/sparse). default S, recommended", default="S", choices=["S","F"])
   parser.add_argument("-sort", "--SortList", help = "Optional file that contains ID list used to sort output.\n" + \
                                                     "Make sure that these IDs match the IDs in the input file\n" + \
						     "Currently this file should not have a header.\n"  + \
						     "ID's should be in the first column (or just one column)", default="")
      
   parser.add_argument("-alt", "--altid_value", help = "Do we consider alternative GO IDs. default T, recommended", default="T", choices=["T","F"])
   args = parser.parse_args()
   
   ########################################################
   # Mapping the parser parameters to old variable names  #
   ########################################################
   obo_file     = args.OBO_file
   inp_flag_val = args.FormIn
   inp_file     = args.Input
   hd_fl_val    = args.Header.lower()
   mt_fl_valR   = args.NameCol
   mt_fl_valR   = ",".join( str(x) for x in mt_fl_valR)   # convert to string. Old code uses string.
   mt_fl_valC   = args.GO_Col
   al_fl_val    = args.altid_value.lower()
   out_fl_val   = args.Output
   if len(out_fl_val) == 0:
       tmp = inp_file.split("." )
       if len( tmp[-1]) <= 4: # Max length for file extension
	  tmp = tmp[:-1]
       file_arg = ".".join( tmp )
       file_str = file_arg+'_preprocess_file.txt' 
   else:
       file_arg = out_fl_val
       file_str = file_arg+'_preprocess_file.txt' 
   
   mt_fl_valM   = args.MatrForm

##################################
#                                #
# Main Process starts here       #
#                                #
##################################

   t0 = time.clock()
   method = GOMethod()
   engine = OBOEngine() 
   if inp_flag_val ==1:
         print "Processing input File of type 1 .....\n"
         #print inp_file,"\t",mt_fl_valR,"\t",mt_fl_valC,"\t",hd_fl_val
         method.randomInpParser(inp_file, mt_fl_valR, mt_fl_valC, hd_fl_val, file_arg)
   elif inp_flag_val ==2:
         print "Processing Input File of type 2 .....\n"
         #method.modelOrgParser(inp_file, mt_fl_valR, mt_fl_valC, mt_fl_valM, file_arg)
	 method.modelOrgParserPT(inp_file, mt_fl_valR, mt_fl_valC, file_arg)
   elif inp_flag_val ==3:
         print "Processing Input File of type 3 .....\n"
	 print inp_file,"\t",mt_fl_valR,"\t",mt_fl_valC,"\t",hd_fl_val
         method.uniProtParser(   inp_file, mt_fl_valR, mt_fl_valC, mt_fl_valM, file_arg)
	 #method.modelOrgParserPT(inp_file, mt_fl_valR, mt_fl_valC, file_arg, header_count = 1)
   elif inp_flag_val ==4:	#This is Ensembl data  #PETRI MODIFIED HERE
         print "Processing Input File of type 4 .....\n"
         method.modelOrgParserPT(inp_file, mt_fl_valR, mt_fl_valC, file_arg, header_count = 1)
   else:
         print "The input file format flag value entered is incorrect. Please enter either 1,2  3, or 4 for respective file format!"
         sys.exit()

   if len(args.SortList) > 0:
       method.ReorderDataTable(file_arg + "_preprocess_file.txt", args.SortList, 0, 0, 1, header2 = 0 )
   #t0 = time.clock()
   print "Processing OBO File.....\n"
   GO_hash = engine.goHashTable(obo_file)
   print "Generating Ancestor Terms...\n"
   method.getFile_go(GO_hash,file_str,al_fl_val)       
   #print "check file name" + file_arg
   rownames,colnames,ind_go_hash = method.printRow_Col(file_arg+'_'+'gene_go.txt',GO_hash)
   #print_variables2(vars())
   if mt_fl_valM =='S'or mt_fl_valM == 's':
         print "Printing out Sparse Matrix"
         method.getSparseMat_alt(file_arg+'_'+'gene_go.txt',ind_go_hash)
   elif mt_fl_valM =='F' or mt_fl_valM =='f':
         print "Printing out Full matrix"
         full_mat = method.getFullMat(file_arg+'_'+'gene_go.txt',rownames,colnames,ind_go_hash)
         file_mat = file_arg+'_'+'binary_matrix'
         mat = open(file_mat,'w')
         for i in range(len(rownames)):
            for j in range(len(colnames)):
               print >>mat,full_mat[i][j],"\t",
            print >>mat,"\n"

         mat.close()
   print "Total execution time taken:",time.clock()-t0,"seconds"
