####################################################
## Collection of R functions used with Ajay Kumar's
## Python Code
## Aim of the project is to develop efficient methods for
## obtaining Gene Ontology annotations as sparse matrices
## analysis enviroments like R, Matlab or NumPy
##
## Here I show useful post-processing functions to be used in R
## 
## Petri Toronen (firstname.lastname@helsinki.fi)
#####################################################

read_sparse_data <- function(data_file, colnames_file, rownames_file,
                    colname_choice = c("long","short"), genename_col = 1){

# Function that reads in the sparse data file and its row and column name 
# matrices. DEsigned to work with Ajays code. Therefore, the colnames and 
# rownames are assumed to be matrices. User then selects the correct column
# for colnames and rownames.
#
# datalist <- read_sparse_data(data_file, colnames_file, rownames_file,
#             colname_choice = c("long","short"), genename_col = 1)
#
# ADD EXPLANATION OF INPUT + EXPLANATION OF OUTPUT
#
# Example call:
#
# GO_tair_sparse <- read_sparse_data("gene_association_sparse.txt",
#                  "gene_association_colnames.txt","new_row_names.txt")
#
# Requires library Matrix. Works with R version XX.XX.XX

  library(Matrix)
  sparse_matr <- read.table(data_file,  sep = "\t", header = FALSE, 
                         quote = "")
  colnames <- read.table(colnames_file, sep = "\t", header = FALSE, 
                         quote = "", comment.char = "")
  rownames <- read.table(rownames_file, sep = "\t", header = FALSE, 
                         quote = "", comment.char = "")

  sz_colnames <- dim(colnames)
  sz_rownames <- dim(rownames)
  if(max(sparse_matr[,1]) != sz_rownames[1]) {  # here's two checks 
    print("row names don't fit the matrix. Too few row names")
  }
  if(max(sparse_matr[,2]) != sz_colnames[1]) {
    print("col names don't fit the matrix. Too few col names")
  }
  
  data <- sparseMatrix(i = sparse_matr[,1], j = sparse_matr[,2], 
                       dims = c(sz_rownames[1], sz_colnames[1]))

  if(length(colname_choice) > 1){
     colname_choice <- colname_choice[1] 
  }
  if(colname_choice == "long"){ colnames(data) <- colnames[,2] }
  else                        { colnames(data) <- colnames[,1] }

  rownames(data) <- rownames[,genename_col]
  
  out <- list(sparse_data = data, all_colnames = colnames, all_rownames = rownames)
  out
}


find_arab_gene_names <- function(name_matrix, primary_name_column = 2){

###############################################################
## This code looks for Arabidopsis gene locus identifiers
## 
## Different columns from inut matrix have diff priorities
## Code first looks at the primary name column (default 2)
## Next it moves to column 3 and last it goes to column 4
## The rows that did not have reasonable Arabidopsis name 
## are reported separately
##
## Code is specially designed to work with Ajays code and 
## GO d
## TODO: Make more flexible. With various column orders
###############################################################

###############
# Subfunctions#
###############

  search_AT_ID <- function(names, pattern){
 
    names <- as.vector(names)
    out <- rep("", length(names))
    
    for(k in 1:length(names)){
      tmp <- grep( pattern, names[k], ignore.case = TRUE)
      if(length(tmp) == 1) {
        out[k] <- names[k]
      }
      else{
        tmp <- strsplit(names[k], split = "|", fixed = TRUE)[[1]]
        #print(tmp)
        ind <- grep( pattern, tmp, ignore.case = TRUE)
        #print(ind)
        if(length(ind) > 0){
          out[k] <- tmp[ind[1]]
        }	
      }          
    }
    out
  }

  define_neg_ind <- function(indexes, data_sz){
    if(length(indexes) > 0){
      tmp2 <- 1:data_sz
      neg_ind <- tmp2[-indexes]
    }else { 
      neg_ind <- 1:data_sz
    }
  }

#################
# Main function #
#################

  search_pattern <- "^AT[0-9MC]+G[0-9]{4,6}"
  name_matrix <- as.matrix(name_matrix)
  names_out <- name_matrix[,primary_name_column]
  tmp_ind <- grep(search_pattern, names_out, ignore.case = TRUE)
  not_AT <- define_neg_ind(tmp_ind, length(names_out))
  not_AT1 <- not_AT
  
  tmp_ind2 <- grep(search_pattern, name_matrix[not_AT,3], ignore.case = TRUE)
  names_out[not_AT[tmp_ind2]] <- name_matrix[not_AT[tmp_ind2],3]
  
  #tmp2 <- 1:length(not_AT)
  #not_AT <- not_AT[ tmp2[-tmp_ind2]]
  #print(length(not_AT))
  not_AT <- define_neg_ind(tmp_ind2, length(names_out))
  not_AT2 <- not_AT
  
  if(length(not_AT) > 0){
    last_names <- search_AT_ID(name_matrix[not_AT,4], search_pattern)
    names_out[not_AT] <- last_names
    tmp_ind2 <- grep( search_pattern, names_out, ignore.case = TRUE)
    tmp2 <- 1:length(names_out)
    tmp_ind2 <- tmp2[-tmp_ind2] 
  }
  else {
    tmp_ind2 <- rep(0,0)  
  }  
  out <- list(names = names_out, not_AT_id1 = not_AT1, not_AT_id2 = not_AT2,
              not_AT_id3 = tmp_ind2)
  out
}

filter_same_targ2_sparse_test <- function(gene_names, data, uniq_IDs = "NONAMES"){

# Code that reorganizes a sparse GO-matrix to match the 
# order of ids given in uniq_IDs vector.
# 
#

  library(Matrix)
  if(length(uniq_IDs) == 1 && uniq_IDs[1] == "NONAMES"){
     uniq_IDs <- unique(gene_names)
  }
  dat_sz <- dim(data)
  data_out <- rep(0, length(uniq_IDs) )
  ctrl.ind <- 1:length(gene_names)
  for(k in 1:length(uniq_IDs)){
     #for(k in 1:100){
    row_ind <- match( uniq_IDs[k], gene_names[ctrl.ind])
    if(length(row_ind) > 0 & !is.na(row_ind)){ 
      data_out[k] <-  ctrl.ind[row_ind]
      ctrl.ind <- ctrl.ind[-row_ind]
    }
    if(k %% 400 == 0){print(k)}
  }
  #names(data_out) <- uniq_IDs
  whole_dat_out <- sparseMatrix(i = {}, j ={}, dims = c(length(uniq_IDs), dat_sz[2]) )
  colnames(whole_dat_out) <- colnames(data)
  rownames(whole_dat_out) <- uniq_IDs
  true_ind <- which(data_out > 0)
  whole_dat_out[true_ind,] <- data[data_out[true_ind],]

  whole_dat_out
}

filter_same_targ2_sparse <- function(gene_names, data, uniq_IDs = "NONAMES"){

# R code for aligning the sparse matrix with other data mtrix
# (gene expression matrix, sequence feature matrix ... what ever)
#

  library(Matrix)
  if(length(uniq_IDs) == 1 && uniq_IDs[1] == "NONAMES"){
     uniq_IDs <- unique(gene_names)
  }
  dat_sz <- dim(data)
  data_out <- sparseMatrix(i = c(), j = c(),
                           dims = c(length(uniq_IDs), dat_sz[2]))
  lls()
  colnames(data_out) <- colnames(data)
  ctrl.ind <- 1:length(gene_names)
  for(k in 1:length(uniq_IDs)){
    row_ind <- match( uniq_IDs[k], gene_names[ctrl.ind])
    if(length(row_ind) > 0 & !is.na(row_ind[1])){ 
      data_out[k,] <-  data[ctrl.ind[row_ind],]
      ctrl.ind <- ctrl.ind[-row_ind]
    }
    if(k %% 300 == 0){print(k)}
  }
  rownames(data.out) <- gene.names
  colnames(data.out) <- colnames(data)
  data.out
}

