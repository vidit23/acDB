## This project tries to emulate how a SQL Database works using Python3. 
#### To run the project:
1. Assuming you have pip installed, run the command `pip3 install -r requirements.txt`
2. And then, `python3 main.py`
    - Type `quit` to exit the program
    - Type `test` to run all the queries given in the sample file
    - Type queries as you see fit.
    
#### File structure
1. engine.py - contains the implementation of all the functions
2. parser.py - parsers the query and returns a dictionary of the extracted meaning
3. main.py - Accepts the input from user, calls the parser and accordingly calls the required function

#### The commands that are accepted by the system are:
1. inputfromfile
2. outputtofile
3. project
4. sort
5. concat
6. select
7. avg
8. max
9. sum
10. sumgroup
11. avggroup
12. movsum
13. movavg
14. Hash
15. Btree
16. join
