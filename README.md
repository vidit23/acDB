## This project tries to emulate how a SQL Database works using Python3. 
#### To run the project:
1. Assuming you have pip installed, run the command `pip3 install -r requirements.txt`
2. And then, `python3 main.py`
    - Type `quit` to exit the program
    - Type `alltest` to run all the queries given in the sample file
    - Type queries according to the command list given below.
    - Does not accept commands from a file
    
#### File structure
1. engine.py - contains the implementation of all the functions
2. parser.py - parsers the query and returns a dictionary of the extracted meaning
3. main.py - Accepts the input from user, calls the parser and accordingly calls the required function
4. tests/ - contains a bunch of test cases written to chec correctness

#### The commands that are accepted by the system and the corresponding query format:
1. inputfromfile - reads a collection from the given file name. Please make sure to add file suffix such as .txt in the parameter if the file has it.
    - `R := inputfromfile(fileName)`
2. outputtofile  - outputs a given collection to a file
    - `outputtofile(collectionName, fileName)`
3. project - Selects the listed columns from the table in the particular order.
    - `R1 := project(collectionName, column1, column2, column3)`
4. sort - Sorts the collection according to given column names. Can take multiple columns
    - `R2 := sort(collectionName, column1, column2)`
5. concat - Concatenates two collections, make sure the column names are the same and in the same order for both collection.
    - `R3 := concat(collectionName_1, collectionName_2)`
6. select - Filter rows based on given queries. Can handle more than two condition but only when combined using either 'or' or 'and'.
    - `R4 := select(collectionName, (column1 > column2 + 50) or (column3 != 30/2))`
7. avg - Returns a table containing the average of a column in a collection
    - `R5 := avg(collectionName, column)`
8. max - Returns a table containing the maximum of a column in a collection
    - `R6 := max(collectionName, column)`
9. sum - Returns a table containing the sum of a column in a collection
    - `R7 := sum(collectionName, column)`
10. count - Returns a table containing the number of rows in a collection
    - `count(collectionName)`
11. countgroup - Groups the collection using columns and counts how many rows in each group
    - `R8 := countgroup(collectionName, groupBy_1, groupBy_2)`
12. sumgroup - Groups the collection using columns and sums rows in each group
    - `R9 := sumgroup(collectionName, sum_column, groupBy_column1, groupBy_column2)`
13. avggroup - Groups the collection using columns and averages rows in each group
    - `R10 := avggroup(collectionName, avg_column, groupBy_column1, groupBy_column2, groupBy_column3)`
14. movsum - Calculates moving sum based on window size
    - `R11 := movsum(collectionName, sum_column, windowSize)`
15. movavg - Calculates moving average based on window size
    - `R12 := movavg(collectionName, sum_column, windowSize)`
16. Hash - Indexes a column using hash
    - `Hash(collectionName, columnName)`
17. Btree - Indexes a column using BTree
    - `Btree(collectionName, columnName)`
18. join - Inner joins two collections using given condition. Can handle more than two condition but only when combined using either 'or' or 'and'.
    - `R115 := join(collection1, collection2, (collection1.col1 >= collection2.col2 + 50) and (collection2.col3 - 4 = collection1.col5))`


Make sure if the file has a .txt after that is mentioned in the paramter of inputfromfile