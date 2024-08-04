##############################
## Create python diagnostics
## 
## This tries to be a collection of debug
## functions made by Petri Toronen
## Currently only useful thing is print_variables2
##############################
import pprint
import sys
import re
import math
import copy

def print_vars(name_list):
  pprint.pprint(name_list)


def print_variables2(data_list, pattern = False):

  # Function for listing of content of name space
  # Directed to debugging
  # Usage: print_variables2(vars())
  # Creator: Petri Toronen
  # 
  # Add pattern processing
  # 
  # might want selection of only functions, modules,
  #

  ##############################################
  # Sub functions. These are kept hidden here
  ##############################################
  def print_header(max_length):
    print "name", " "*(max_length - 4 + 2), "type", " "*6, "\t", \
          "mem size  \t", "Shape/length \t", "Var.type"  
  
  def print_row(name, dat_size, dat_type, dat_dim, max_length, dat_type2):
    #Simple helper function that prints a single row

    # sub function that defines added space
    def end_space(printed, max_len = 10):
      printed_len = len(str(printed))
      if printed_len < max_len :
         added_space = " "*(10 - printed_len)
      else:
         added_space = ""
      return added_space
    
    name_len = len(name)
  
    add_space  = end_space(dat_type)
    add_space2 = end_space(dat_size)
    add_space3 = end_space(dat_dim)
  
    print name, " "*(max_length - name_len + 2), dat_type, add_space, "\t", \
          dat_size, add_space2, "\t", dat_dim, add_space3, "\t", dat_type2

  
  def find_var_types(data_in):
    if isinstance(data_in, dict):
       data_in = data_in.values()
    tmp = {}
    for item in data_in:
       item_type = type(item).__name__
       tmp[item_type] = 1
    output = tmp.keys()
    output = " ".join(output)
    return output

  def get_max_length(names):
    max_name_len = 6  # Default minimum length
    for name in names:
      tmp = len(name)
      if tmp > max_name_len:
          max_name_len = tmp
      #if
    #For
    return max_name_len

  #################################
  ## Following hasn't been tested
  #################################
  def find_pattern(names, pattern, case_sensitive = False):
    orig_names = names  # We need to return original names
    output = []
    if not case_sensitive:
      pattern = pattern.lower()    
    for k in range(0, len(names)):
      tmp_name = names[k]
      if not case_sensitive:
        tmp_name = tmp_name.lower()
      if pattern in tmp_name:
        output.append(orig_names[k])
      # IF
    # FOR
    return output
  ##############################
  # Sub-functions ended        #
  ##############################
  #Set some parameter values
  name_list = data_list.keys()
  if pattern:
    name_list = find_pattern(name_list, pattern )
  
  max_l = 10
  max_name_len = get_max_length(name_list)
  print_header(max_name_len)
  
  for name in name_list:
  
     myvalue = data_list[name]
     type_name = type(myvalue).__name__

     if  type_name == 'module' or type_name == 'function':
	dat_sz  = sys.getsizeof(myvalue)
	print_row(name, dat_sz, type_name, "NA", max_name_len, "NA")
     elif type_name == 'array' or type_name == 'ndarray':  # Numpy array 
        dat_sz    = myvalue.nbytes
	dat_shape = str( myvalue.shape )
	var_type  = myvalue.dtype
        print_row(name, dat_sz, type_name, dat_shape, max_name_len, var_type)
     elif type_name == 'dict' or type_name == 'list' or type_name == 'tuple':
        dat_sz  = sys.getsizeof(myvalue)
	dat_len = len(myvalue)
	if dat_len > 0:
	  dat_types = find_var_types(myvalue)
        else:
	  dat_types = "Empty"
	print_row(name, dat_sz, type_name, dat_len, max_name_len, dat_types)
     elif type_name == 'str':
        dat_sz  = sys.getsizeof(myvalue)
	dat_len = len(myvalue)
	print_row(name, dat_sz, type_name, dat_len, max_name_len, "NA")
     else:
        dat_sz  = sys.getsizeof(myvalue)
        dat_len = "NA"
	print_row(name, dat_sz, type_name, dat_len, max_name_len, "Unknown Data type")
     #if -elif -else
  #For
  print ""

def print_obj_info(data, pattern = False):

  # Function for listing of content of name space
  # Directed to debugging
  # Usage: print_variables2(vars())
  # Creator: Petri Toronen
  # 
  # MODIFICATION FOR OBJECT CONTENT LISTING
  # THIS IS NOT WORKING
  #
  # Add pattern processing
  # 
  # might want selection of only functions, modules,
  #

  ##############################################
  # Sub functions. These are kept hidden here
  ##############################################
  def print_header(max_length):
    print "name", " "*(max_length - 4 + 2), "type", " "*6, "\t", \
          "mem size  \t", "Shape/length \t", "Var.type"  
  
  def print_row(name, dat_size, dat_type, dat_dim, max_length, dat_type2):
    #Simple helper function that prints a single row

    # sub function that defines added space
    def end_space(printed, max_len = 10):
      printed_len = len(str(printed))
      if printed_len < max_len :
         added_space = " "*(10 - printed_len)
      else:
         added_space = ""
      return added_space
    
    name_len = len(name)
  
    add_space  = end_space(dat_type)
    add_space2 = end_space(dat_size)
    add_space3 = end_space(dat_dim)
  
    print name, " "*(max_length - name_len + 2), dat_type, add_space, "\t", \
          dat_size, add_space2, "\t", dat_dim, add_space3, "\t", dat_type2

  
  def find_var_types(data_in):
    if isinstance(data_in, dict):
       data_in = data_in.values()
    tmp = {}
    for item in data_in:
       item_type = type(item).__name__
       tmp[item_type] = 1
    output = tmp.keys()
    output = " ".join(output)
    return output

  def get_max_length(names):
    max_name_len = 6  # Default minimum length
    for name in names:
      tmp = len(name)
      if tmp > max_name_len:
          max_name_len = tmp
      #if
    #For
    return max_name_len

  #################################
  ## Following hasn't been tested
  #################################
  def find_pattern(names, pattern, case_sensitive = False):
    orig_names = names  # We need to return original names
    output = []
    if not case_sensitive:
      pattern = pattern.lower()    
    for k in range(0, len(names)):
      tmp_name = names[k]
      if not case_sensitive:
        tmp_name = tmp_name.lower()
      if pattern in tmp_name:
        output.append(orig_names[k])
      # IF
    # FOR
    return output
  ##############################
  # Sub-functions ended        #
  ##############################
  #Set some parameter values
  name_list = dir(data)
  if pattern:
    name_list = find_pattern(name_list, pattern )
  
  max_l = 10
  max_name_len = get_max_length(name_list)
  print_header(max_name_len)
  
  for name in name_list:
  
     myvalue = data_list[name]
     type_name = type(myvalue).__name__

     if  type_name == 'module' or type_name == 'function':
	dat_sz  = sys.getsizeof(myvalue)
	print_row(name, dat_sz, type_name, "NA", max_name_len, "NA")
     elif type_name == 'array' or type_name == 'ndarray':  # Numpy array 
        dat_sz    = myvalue.nbytes
	dat_shape = str( myvalue.shape )
	var_type  = myvalue.dtype
        print_row(name, dat_sz, type_name, dat_shape, max_name_len, var_type)
     elif type_name == 'dict' or type_name == 'list' or type_name == 'tuple':
        dat_sz  = sys.getsizeof(myvalue)
	dat_len = len(myvalue)
	if dat_len > 0:
	  dat_types = find_var_types(myvalue)
        else:
	  dat_types = "Empty"
	print_row(name, dat_sz, type_name, dat_len, max_name_len, dat_types)
     elif type_name == 'str':
        dat_sz  = sys.getsizeof(myvalue)
	dat_len = len(myvalue)
	print_row(name, dat_sz, type_name, dat_len, max_name_len, "NA")
     else:
        dat_sz  = sys.getsizeof(myvalue)
        dat_len = "NA"
	print_row(name, dat_sz, type_name, dat_len, max_name_len, "Unknown Data type")
     #if -elif -else
  #For
  print ""

def print_some_dict(dict_in, max_count = 10, Print_vals = True):
   """
   print_some_dict(dict_in, max_count = 10, Print_vals = True)
   Simple helper that prints 10 items from dict.
   Print_vals (True/False)defines if dict_in[key] is printed
   
   I use this to get test keys for dict, to check if the data is OK...
   No rocket science here... :-)
   Petri Toronen
   """
   import random
   max_count = min(len(dict_in), max_count)
   if Print_vals:
     tmp_dict = random.sample(dict_in.items(), max_count)
   else:
     tmp_dict = random.sample(dict_in.keys(), max_count)
   
   for tmp in tmp_dict:
     print tmp
     

def percentile(M, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.
    
    Code is copied: 
    http://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
    http://code.activestate.com/recipes/511478/
    
    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.
    

    @return - the percentile of the values
    """
    #if percent > 1:
    #  sys.exit("percent value in percentile function should be <= 1")
    N = copy.copy(M)
    N.sort()
    #if not N:
    #    return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    #print k
    #print int(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1
    
def multi_percentile(data, limit_vals = [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]):
    """
    extend percentile to multiple thresholds
    """
    
    data_out = []
    for limit in limit_vals:
       data_out.append( percentile(data, limit) )
    return data_out
