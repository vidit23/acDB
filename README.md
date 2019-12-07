We will run your programs on test cases of our choosing. For ease of parsing there will be one operation per line. 

Input | Meaning
-------------------------------------------  | ----------------------------------------
R := inputfromfile(sales1)                   | import vertical bar delimited foo, first line has column headers. Suppose they are saleid, itemid, customerid, storeid, time, qty, pricerange
R1 := select(R, (time > 50) or (qty < 30))   | select * from R where time > 50 or qty < 30
R2 := project(R1, saleid, qty, pricerange)   | select saleid, qty, pricerange from R1
R3 := avg(R1, qty)                           | select avg(qty) from R1
R4 := sumgroup(R1, time, qty)                | select qty, sum(time) from R1 group by qty
R5 := sumgroup(R1, qty, time, pricerange)    | select sum(qty), time, pricerange from R1 group by time, pricerange
R6 := avggroup(R1, qty, pricerange)          | select avg(qty), pricerange from R1 group by by pricerange
S := inputfromfile(sales2)                   | suppose column headers are saleid, I, C, S, T, Q, P
T := join(R, S, R.customerid = S.C)          | select * from R, S where R.customerid = S.C
T1 :=  join(R1, S, (R1.qty > S.Q) and (R1.saleid = S.saleid)) | select * from R1, S where R1.qty > S.Q
T2 := sort(T1, S_C)                          | sort T1 by S_C
T2prime := sort(T1, R1_time, S_C)            | sort T1 by R_itemid, S_C (in that order)
T3 := movavg(T2prime, R1_qty, 3)             | perform the three item moving average of T2prime on column R_qty. This will be as long as R_qty with the three way moving average of 4 8 9 7 being 4 6 7 8
T4 := movsum(T2prime, R1_qty, 5)             | perform the five item moving sum of T2prime on column R_qty
Q1 := select(R, qty = 5)                     | select * from R where qty=5 
Btree(R, qty)                                | create an index on R based on column qty. Equality selections and joins on R should use the index.
Q2 := select(R, qty = 5)                     | this should use the index
Q3 := select(R, itemid = 7)                  | select * from R where itemid = 7
Hash(R,itemid)                               | make hash on some field
Q4 := select(R, itemid = 7)                  | this should use the hash index
Q5 := concat(Q4, Q2)                         | concatenate the two tables (must have the same schema). Duplicate rows may result (though not with this example).
outputtofile(Q5, Q5)                         | This should output the table Q5 into a file
outputtofile(T, T)                         | This should output the table T into a file
