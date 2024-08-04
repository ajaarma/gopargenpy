function [data, col_names, row_names] = process_pyth_data(data_file, row_name_file, col_name_file)

% Write better explanation when time....
% usage:
% [data, col_names, row_names] = process_pyth_data(data_file, row_name_file, col_name_file)
% input: Name for three files
% output:
% data matrix, col_names, row_names

   delimiter = '\t';
   disp('first reading data in')
   tmp = dlmread(data_file, delimiter);
   tmp(:,3) = 1;
   disp('next reading the column info in')
   row_names = read_text_in(row_name_file); % this function probably slows this down
   col_names = read_text_in(col_name_file);
   disp('checking the matrices that they match')   
   col_name_sz = size(col_names);
   row_name_sz = size(row_names);
   matr_sz = [max(tmp(:,1)) max(tmp(:,2))];

   if(max(tmp(:,1)) > row_name_sz(1))
     disp('Error!! More rows in data file than there are row names. Check the input!!')
     disp('')
     whos
   elseif(max(tmp(:,1)) < row_name_sz(1))
     disp('Potential error!! There is more row names than there are data rows. Check the input')
     disp('This is allowed difference but still most likely an error')
     disp('')
     matr_sz(1) = row_name_sz(1);
     whos
   end
   
   if(max(tmp(:,2)) > col_name_sz(1))
     disp('Error!! More columns in data file than there are column names. Check the input!!')
     disp('')
     whos
   elseif(max(tmp(:,2)) < col_name_sz(1))
     disp('Potential error!! There is more column names than there are data columns. Check the input')
     disp('This is allowed difference but still most likely an error')
     disp('')
     matr_sz(2) = row_name_sz(2);
     whos
   end
   
   data = sparse(tmp(:,1), tmp(:,2), tmp(:,3), matr_sz(1), matr_sz(2));
end

function out = read_text_in(file_name)
% Sub function for project where we read
% data from Ajays python program
%
% This function reads the text data in 
% and creates the cell array

  delimiter = '\t';
  fid = fopen(file_name, 'r');
  tmp = textscan(fid, '%[^\n]');
  out = split_text(tmp{1}, delimiter);
  %out = delimiter;
end 

function output = split_text(input_cell, delimiter)
% REading cell array of rows
% Generating a cell array 
%

  tmp_len = length(input_cell);
  %textscan( char(input_cell{1}), '%s', 'delimiter', delimiter)
  tmp_tmp =  textscan( char(input_cell{1}), '%s', 'delimiter', delimiter);
  tmp_len2 = length( tmp_tmp{1});
  output = cell( tmp_len, tmp_len2);
  % Following part should rewritten. Probably very 
  % unoptimal with two for loops!!
  for k = 1:tmp_len
    tmp_tmp = textscan( char(input_cell{1}), '%s', 'delimiter', delimiter);
    for l = 1:tmp_len2
       output{k, l} = tmp_tmp{1}(l);
    end
  end
  
end
