'''
R := inputfromfile(sales1) - {   "outputDB": “R”, 
                                "functionName": “inputfromfie”, 
                                "input":”sales1”,
                                "fields": None,
                                "condition": None
                             }

R1 := select(R, (time > 50) or (qty != 30) or (qty >= 100)) - { "outputDB": “R1”, 
                                                "functionName": "select", 
                                                "input":"R", 
                                                "fields": [["time", ">", "50"], ["qty", "!=", "30"], ["qty", ">=" ,"100"]]
                                                "condition": "or" }

R2 := project(R1, saleid, qty, pricerange) - { "outputDB": “R2”, 
                                            "functionName": "project", 
                                            "input":"R1", 
                                            "fields": ["saleid", "qty", "pricerange"],
                                            "condition": None }

R3 := avg(R1, qty) - { "outputDB": “R3”, 
                        "functionName": "avg", 
                        "input":"R1", 
                        "fields": ["qty"],
                        "condition": None }

T := join(R, S, R.customerid = S.C) - { "outputDB": “T”, 
                                    "functionName": "join", 
                                    "input":"R", 
                                    "fields": ["S", ["R.customerid", "=", "S.C"]],
                                    "condition": None }
Inequalities: =, <, >, !=, >=, <=
'''


def parser(inputQuery):
    answer = {"outputDB": None,"functionName": None,"input":None,"fields": None,"condition": None}
    arr = []
    Comparison_operator = ['!=','<','>','=','>=','<=']
    Logical_operator = ['and','or']
    inputQuery = inputQuery.strip()
    position_bracket1 = None
    position_comma = None
    position_braketEnd = None 
    position_assignment_character = None
    #length of input query 
    length_inputQuery = len(inputQuery)
    #finds the position of 1 bracket
    position_bracket1 = inputQuery.find("(") 
    #finds the Number of Comma's
    comma_count = inputQuery.count(",") 
    #finds the position of First Comma
    position_comma = inputQuery.find(",") 
    #finds the position of Last bracket
    position_braketEnd = inputQuery.find(")") 
    #finds the position of Assignment character
    position_assignment_character = inputQuery.find(":=") 

    #if the assignment operator is present then "else" happens otherwise if is executed
    if position_assignment_character == -1:
        print("the length of string is: " + str(length_inputQuery))
        if position_bracket1 != -1:
            print ("the position of First bracket: " + str(position_bracket1))
        if position_braketEnd != -1:
            print ("the position of Last bracket: " + str(position_braketEnd))
        #if there is only 1 comma present
        if comma_count != 0 and comma_count == 1: 
            if position_comma != -1:
                print ("the position of Comma: " + str(position_comma))
            #if there is no end bracket in the given query, the code Doesn’t execute and gives SYNTAX ERROR
            if position_bracket1 != -1 and position_braketEnd == -1:
                print("Syntax Error")
            #if the query given by the user is in correct format i.e. with a starting and an end bracket
            elif position_bracket1 != -1:
                #the value before the bracket i.e. function name is stored in a variable and the variable is stored in Dictionary 
                function_Name = inputQuery[:position_bracket1]
                function_Name = function_Name.strip()
                # print (function_Name)
                answer["functionName"] = function_Name
                #if there is 1 comma present
                #the input between 1 bracket and 1 comma is stored in variable and the variable is stored in Dictionary
                if position_comma != -1:
                    brac1_comma1 = inputQuery[position_bracket1 + 1:position_comma]
                    brac1_comma1 = brac1_comma1.strip()
                    # print (brac1_comma1)
                    answer["input"] = brac1_comma1
                    #number of "or" in the query is been stored in the variable or_count
                    or_count = inputQuery[position_comma + 1:-1].count('or')
                    # print (or_count)
                    #number of "and" in the query is been stored in the variable and_count
                    and_count = inputQuery[position_comma + 1:-1].count('and')
                    # print (and_count)
                    #if there is an "and" or "or" in the query then code continues otherwise else is executed
                    if or_count != 0 or and_count != 0:
                        flag = False
                        check_logical = ''
                        #the value between the comma and the last bracket is stored in comma1_bracketEnd
                        comma1_bracketEnd = (inputQuery[position_comma + 1:-1].strip()).split()
                        # print (comma1_bracketEnd)
                        #presence of logical Operators is checked: if present the logical operator present is stored in Dictionary 
                        for check_logical in Logical_operator:
                            if check_logical in comma1_bracketEnd:
                                flag = True
                                break
                        answer['condition'] = check_logical
                        if flag:
                            #if "or" is present in the query
                            if or_count != -1 and and_count == 0:
                                comma1_bracketEnd = inputQuery[position_comma + 1:-1].split('or')
                                # print (comma1_bracketEnd)
                                m = 0
                                #the 2 conditions generated on "or" are stripped and splitted removing the Parentheses and Appended to array
                                while m <= or_count:
                                    z1 = comma1_bracketEnd[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                            #if "and" is present in the query
                            elif and_count != -1 and or_count == 0:
                                comma1_bracketEnd = inputQuery[position_comma + 1:-1].split('and') 
                                # print (comma1_bracketEnd)
                                m = 0
                                #the 2 conditions generated on "and" are stripped and splitted removing the Parentheses and Appended to array
                                while m <= and_count:
                                    z1 = comma1_bracketEnd[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                    #if there are no "and" and "or" in the query then else is executed
                    else:
                        comma1_bracketEnd = inputQuery[position_comma + 1:position_braketEnd]
                        comma1_bracketEnd = comma1_bracketEnd.strip()
                        arr = []
                        arr.append(comma1_bracketEnd)
                        # print (comma1_bracketEnd)
                    # print (arr)
                    answer["fields"] = arr
                #if there are no comma's present in the query 
                elif position_comma == -1 and position_bracket1 != -1:
                    if_only_1_input = inputQuery[position_bracket1 + 1:position_braketEnd]
                    if_only_1_input = if_only_1_input.strip()
                    # print (if_only_1_input)
                    answer["input"] = if_only_1_input
                return answer
            else:
                print("Syntax Error")
        #if there are more than 1 comma present in the input query
        else:
            # print ("there are " + str(comma_count) +" comma's present in the string")
            #if the query is in perfect format i.e. present with a starting and end bracket
            #the value before the bracket i.e. function name is stored in a variable and the variable is stored in Dictionary 
            if position_bracket1 != -1 and position_braketEnd != -1:
                function_Name = inputQuery[:position_bracket1]
                function_Name = function_Name.strip()
                # print (function_Name)
                answer["functionName"] = function_Name
                i = 0
                b = inputQuery.find(",")
                c = inputQuery[position_bracket1 + 1:b].strip()
                # print (c)
                answer["input"] = c
                position_bracket1 = b
                i = b + 1
                if b != (-1):
                    while i < len(inputQuery):
                        b = inputQuery.find(",",i)
                        c = inputQuery[position_bracket1 + 1:b].strip()
                        # print (c)
                        c = c.split()
                        flag = False
                        check_comparison = ''
                        for check_comparison in Comparison_operator:
                            if check_comparison in c:
                                flag = True
                                break
                        if flag:
                            arr.append((inputQuery[position_bracket1 + 1:b].strip()).split())
                            break
                        else:
                            arr.append(inputQuery[position_bracket1 + 1:b].strip())
                        position_bracket1 = b
                        i = b + 1
                        if b == (-1):
                            break
                        answer["fields"] = arr
                return answer
            else:
                print("Syntax Error")
    #if the assignment operator is present then below part of the code executes 
    else:
        inputQuery1 = inputQuery.split(":=")
        inputQuery2 = inputQuery1[1]
        inputQuery2 = inputQuery2.strip()
        position_bracket1 = None
        position_comma = None
        position_braketEnd = None 
        position_assignment_character = None
        length_inputQuery = len(inputQuery2)
        #finds the position of 1 bracket
        position_bracket1 = inputQuery2.find("(") 
        #finds the Number of Comma's
        comma_count = inputQuery2.count(",") 
        #finds the position of First Comma
        position_comma = inputQuery2.find(",") 
        #finds the position of Last bracket
        position_braketEnd = inputQuery2.find(")") 
        #finds the position of Assignment character
        position_assignment_character = inputQuery2.find(":=") 
        #if the assignment operator is present then "else" happens otherwise if is executed
        if position_assignment_character == -1:
            print("the length of string is: " + str(length_inputQuery))
        if position_bracket1 != -1:
            print ("the position of First bracket: " + str(position_bracket1))
        if position_braketEnd != -1:
            print ("the position of Last bracket: " + str(position_braketEnd))
        #if there is only 1 comma present
        if comma_count != 0 and comma_count == 1: 
            if position_comma != -1:
                print ("the position of Comma: " + str(position_comma))
            #if there is no end bracket in the given query, the code Doesn’t execute and gives SYNTAX ERROR
            if position_bracket1 != -1 and position_braketEnd == -1:
                print("Syntax Error")
            #if the query given by the user is in correct format i.e. with a starting and an end bracket
            #the value before the assignment Operator i.e. output database is stored in a variable and the variable is stored in Dictionary
            elif position_bracket1 != -1:
                output_db = inputQuery1[0]
                output_db = output_db.strip()
                # print(output_db)
                answer["outputDB"] = output_db
                #the value before the bracket i.e. function name is stored in a variable and the variable is stored in Dictionary
                function_Name = inputQuery2[:position_bracket1]
                function_Name = function_Name.strip()
                # print (function_Name)
                answer["functionName"] = function_Name
                #if there is 1 comma present the query
                #the input between 1 bracket and 1 comma is stored in variable and the variable is stored in Dictionary
                if position_comma != -1:
                    brac1_comma1 = inputQuery2[position_bracket1 + 1:position_comma]
                    brac1_comma1 = brac1_comma1.strip()
                    # print ("brac1_comma1")
                    answer["input"] = brac1_comma1
                    #number of "or" in the query is been stored in the variable or_count
                    or_count = inputQuery[position_comma + 1:-1].count('or')
                    # print (or_count)
                    #number of "and" in the query is been stored in the variable and_count
                    and_count = inputQuery[position_comma + 1:-1].count('and')
                    # print (and_count)
                    #if there is an "and" or "or" in the query then code continues otherwise else is executed
                    if or_count != 0 or and_count != 0:
                        flag = False
                        check_logical = ''
                        comma1_bracketEnd = (inputQuery2[position_comma + 1:-1].strip()).split()
                        # print (comma1_bracketEnd)
                        for check_logical in Logical_operator:
                            if check_logical in comma1_bracketEnd:
                                flag = True
                                break
                        answer['condition'] = check_logical
                        if flag:
                            if or_count != -1 and and_count == 0:
                                comma1_bracketEnd = inputQuery2[position_comma + 1:-1].split('or')
                                # print (comma1_bracketEnd)
                                m = 0
                                while m <= or_count:
                                    z1 = comma1_bracketEnd[m].strip()
                                    for check_comparison in Comparison_operator:
                                        if check_comparison in z1:
                                            flag = True
                                            break
                                    if flag:
                                        z1 = z1[1:-1].split(check_comparison)
                                        arr.append([z1[0].strip(), check_comparison, z1[1].strip()])   
                                    m = m +1
                            elif and_count != -1 and or_count == 0:
                                comma1_bracketEnd = inputQuery2[position_comma + 1:-1].split('and') 
                                # print (comma1_bracketEnd)
                                m = 0
                                flag = False
                                check_comparison = ''
                                while m <= and_count:
                                    z1 = comma1_bracketEnd[m].strip()
                                    for check_comparison in Comparison_operator:
                                        if check_comparison in z1:
                                            flag = True
                                            break
                                    if flag:
                                        z1 = z1[1:-1].split(check_comparison)
                                        arr.append([z1[0].strip(), check_comparison, z1[1].strip()])   
                                    m = m +1
                    else:
                        i = 0
                        b = inputQuery2.find(",")
                        c = inputQuery2[position_bracket1 + 1:b].strip()
                        # print(c)
                        answer["input"] = c
                        position_bracket1 = b
                        i = b + 1
                        if b != (-1):
                            while i < len(inputQuery2):
                                b = inputQuery2.find(",",i)
                                c = inputQuery2[position_bracket1 + 1:b].strip()
                                # print (c)
                                position = c.find("(") 
                                # print (position)
                                if position != -1:
                                    flag = False
                                    check_comparison = ''
                                    for check_comparison in Comparison_operator:
                                        if check_comparison in c:
                                            flag = True
                                            break
                                    if flag:
                                        new_var = (c[1:-1].strip()).split(check_comparison)
                                        # print (new_var)
                                        arr.append([new_var[0].strip(), check_comparison, new_var[1].strip()])
                                        break
                                    else:
                                        arr.append(c.strip())
                                    position_bracket1 = b
                                    i = b + 1
                                    if b == (-1):
                                        break
                                else:
                                    flag = False
                                    check_comparison = ''
                                    for check_comparison in Comparison_operator:
                                        if check_comparison in c:
                                            flag = True
                                            break
                                    if flag:
                                        new_var = (inputQuery2[position_bracket1 + 1:b].strip()).split(check_comparison)
                                        # print (new_var)
                                        arr.append([new_var[0].strip(), check_comparison, new_var[1].strip()])
                                        break
                                    else:
                                        arr.append(inputQuery2[position_bracket1 + 1:b].strip())
                                    position_bracket1 = b
                                    i = b + 1
                                    if b == (-1):
                                        break
                    # print (arr)
                    answer["fields"] = arr
                elif position_comma == -1 and position_bracket1 != -1:
                    if_only_1_input = inputQuery2[position_bracket1 + 1:position_braketEnd]
                    if_only_1_input = if_only_1_input.strip()
                    # print (if_only_1_input)
                    answer["input"] = if_only_1_input
                return answer
            else:
                print("Syntax Error")
        else:
            # print ("there are " + str(comma_count) +" comma's present in the string")
            if position_bracket1 != -1 and position_braketEnd != -1:
                output_db = inputQuery1[0]
                output_db = output_db.strip()
                # print (output_db)
                answer["outputDB"] = output_db
                function_Name = inputQuery2[:position_bracket1]
                function_Name  = function_Name.strip()
                # print(function_Name)
                answer["functionName"] = function_Name
                i = 0
                b = inputQuery2.find(",")
                c = inputQuery2[position_bracket1 + 1:b].strip()
                # print(c)
                answer["input"] = c
                position_bracket1 = b
                i = b + 1
                if b != (-1):
                    while i < len(inputQuery2):
                        b = inputQuery2.find(",",i)
                        c = inputQuery2[position_bracket1 + 1:b].strip()
                        # print (c)
                        or_count = c.count('or')
                        # print (or_count)
                        and_count = c.count('and')
                        # print (and_count)
                        if or_count != 0 or and_count != 0:
                            flag = False
                            check_logical = ''
                            c = c.strip()
                            # print (c)
                            for check_logical in Logical_operator:
                                if check_logical in c:
                                    flag = True
                                    break
                            answer['condition'] = check_logical
                            if flag:
                                if or_count != -1 and and_count == 0:
                                    c = c.split('or')
                                    # print (c)
                                    m = 0
                                    while m <= or_count:
                                        z1 = c[m].strip()
                                        for check_comparison in Comparison_operator:
                                            if check_comparison in z1:
                                                flag = True
                                                break
                                        if flag:
                                            z1 = z1[1:-1].split(check_comparison)
                                            arr.append([z1[0].strip(), check_comparison, z1[1].strip()])   
                                        m = m +1
                                elif and_count != -1 and or_count == 0:
                                    c = c.split('and') 
                                    # print (c)
                                    m = 0
                                    flag = False
                                    check_comparison = ''
                                    while m <= and_count:
                                        z1 = c[m].strip()
                                        for check_comparison in Comparison_operator:
                                            if check_comparison in z1:
                                                flag = True
                                                break
                                        if flag:
                                            z1 = z1[1:-1].split(check_comparison)
                                            arr.append([z1[0].strip(), check_comparison, z1[1].strip()])   
                                        m = m +1
                            position_bracket1 = b
                            i = b + 1
                            if b == (-1):
                                break
                            answer["fields"] = arr
                        else:
                            c = c.split()
                            flag = False
                            check_comparison = ''
                            for check_comparison in Comparison_operator:
                                if check_comparison in c:
                                    flag = True
                                    break
                            if flag:
                                arr.append((inputQuery2[position_bracket1 + 1:b].strip()).split())
                                break
                            else:
                                arr.append(inputQuery2[position_bracket1 + 1:b].strip())
                            position_bracket1 = b
                            i = b + 1
                            if b == (-1):
                                break
                            answer["fields"] = arr
                return answer
            else:
                print("Syntax Error")