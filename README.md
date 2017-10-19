(X) Produce a python module (ayasdi_python_code.py)
    
(I/P) Create a tab-delimited file (ayasdi_assignment.csv) 20 columns and a million rows
    
(X) Column 1 (labeled as col1 is the index column where the values are 1 to 1 million)
    
( ) The next 9 columns (2 to 10) contain randomly distributed gaussian data 

( ) and are labelled col2_x ... col10_x where 'x' is the mean of the gaussian distribution.
For example, if you chose means of 10, 20, 30, 40, 50, 60, 70, 80 for col2 through col10, the labels are col2_10, col3_20, col4_30 and etc. You can choose whatever mean and variance you would like for each column.

(I/P) Additionally, each of these columns have 10% nulls, randomly distributed.

(I/P) Columns 11 to 19 are labelled as col11...col19, 
where each column has random strings selected from the English Dictionary.

(I/P) 10% randomly distributed nulls in this column as well.

( ) Column 20 has random dates selected between January 1, 2014 to December 31, 2014.
No nulls in this column.

(I/P) Once this dataset has been created, load it into a single table in a sqlite database (ayasdi_assignment.db).

* Do not use 3rd party packages. For example, do not use numpy, pandas, and SQLAlchemy.