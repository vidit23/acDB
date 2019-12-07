## This project tries to emulate how a SQL Database works using Python3. 
#### To run the project:
1. Assuming you have pip installed, run the command `pip3 install -r requirements.txt`
2. And then, `python3 main.py`
    - Type `quit` to exit the program
    - Type `alltest` to run all the queries given in the sample file
    - Type queries as you see fit.
    
#### File structure
1. engine.py - contains the implementation of all the functions
2. parser.py - parsers the query and returns a dictionary of the extracted meaning
3. main.py - Accepts the input from user, calls the parser and accordingly calls the required function

#### The commands that are accepted by the system and the corresponding query format:
1. inputfromfile 
    - `R := inputfromfile(sales1)`
2. outputtofile 
    - `outputtofile(R, R)`
3. project 
    - `R1 := project(R, saleid, qty, pricerange))`
4. sort 
    - `R2 := sort(R1, qty, saleid)`
5. concat 
    - `R3 := concat(R1, R2)`
6. select 
    - `R4 := select(R, (time > 50) or (qty < 30))`
7. avg 
    - `R5 := avg(R4, qty)`
8. max 
    - `R6 := max(R4, qty)`
9. sum 
    - `R7 := sum(R4, qty)`
10. count 
    - `count(R4)`
11. countgroup 
    - `R8 := countgroup(R1, time, pricerange)`
12. sumgroup 
    - `R9 := sumgroup(R1, qty, time, pricerange)`
13. avggroup 
    - `R10 := avggroup(R1, qty, time, pricerange)`
14. movsum 
    - `R11 := movsum(R2, qty, 5)`
15. movavg 
    - `R12 := movavg(R2, qty, 6)`
16. Hash 
    - `Hash(R,itemid)`
17. Btree 
    - `Btree(R, qty)`
18. join 
    - `R115 := join(R1, R, (R1.qty >= R.qty) and (R1.saleid = R.saleid))`

Supports more than 2 conditions

Make sure if the file has a .txt after that is mentioned in the paramter of inputfromfile