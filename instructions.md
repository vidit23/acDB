# acDB
#### Project for DBMS course

Given ordered tables (array-tables) whose rows consist of strings and integers, you are to write a program which will:

1. Perform the basic operations of relational algebra: selection, projection, join, group by, and count, sum and avg aggregates. The comparators for select and join will be = <, >, ! =, ≥, ≤
2. Because the array-tables are potentially ordered, you can sort an arraytable by one or more columns, and running moving sums and average aggregates on a column of an array-table.
3. Import a vertical bar delimited file into an array-table (in the same order), export from an array-table to a file preserving its order, and assign the result of a query to an array-table.
4. Each operation will be on a single line. Each time you execute a line, you should print the time it took to execute.
5. You will support in memory B-trees and hash structures. You are welcome to take those implementations from wherever you can find them, but you must say where.
6. Your program should be written in python or java. You will hand in clean and well structured source code in which each function has a header that says:
  - what the function does
  - what its inputs are and what they mean
  - what the outputs are and mean
  - any side effects to globals.
7. You must ensure that your software runs on the Courant Institute (cims) machine crunchy5.cims.nyu.edu
8. You may NOT use any relational algebra or SQL library or system (e.g. no SQLite, no mySQL, no other relational database system, no Pandas ). Stick pretty much to the standard stuff (e.g. in Python: numpy, core language features, string manipulation, random number generators, and data structure support for in memory B-trees and hash structures). You may not use anyone else’s code (other than for the data structure implementation). Doing so will constitute plagiarism.
