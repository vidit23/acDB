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
    arr1 = ['=','<','>','!=','>=','<=']
    arr2 = ['and','or']
    inputQuery = inputQuery.strip()
    position_bracket1 = None
    position_comma = None
    position_braketEnd = None 
    position_character = None
    length_x = len(inputQuery)
    position_bracket1 = inputQuery.find("(") #finds the position of 1 bracket
    comma_count = inputQuery.count(",") #finds the Number of Comma's
    position_comma = inputQuery.find(",") #finds the position of First Comma
    position_braketEnd = inputQuery.find(")") #finds the position of Last bracket
    position_character = inputQuery.find(":=") #finds the position of Special character
    if position_character == -1:
        print("the length of string is: " + str(length_x))
        if position_bracket1 != -1:
            print ("the position of First bracket: " + str(position_bracket1))
        if position_braketEnd != -1:
            print ("the position of Last bracket: " + str(position_braketEnd))
        if comma_count != 0 and comma_count == 1: #if there is a comma present 
            if position_comma != -1:
                print ("the position of Comma: " + str(position_comma))
            if position_bracket1 != -1 and position_braketEnd == -1:
                print("Syntax Error")
            elif position_bracket1 != -1:
                x = inputQuery[:position_bracket1]
                x = x.strip()
                print (x)
                answer["functionName"] = x
                if position_comma != -1:
                    y = inputQuery[position_bracket1 + 1:position_comma]
                    y = y.strip()
                    print (y)
                    answer["input"] = y
                    x1 = inputQuery[position_comma + 1:-1].count('or')
                    print (x1)
                    x2 = inputQuery[position_comma + 1:-1].count('and')
                    print (x2)
                    if x1 != 0 or x2 != 0:
                        flag = False
                        k = ''
                        z = (inputQuery[position_comma + 1:-1].strip()).split()
                        print (z)
                        for k in arr2:
                            if k in z:
                                flag = True
                                break
                        answer['condition'] = k
                        if flag:
                            if x1 != -1 and x2 == 0:
                                z = inputQuery[position_comma + 1:-1].split('or')
                                print (z)
                                m = 0
                                while m <= x1:
                                    z1 = z[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                            elif x2 != -1 and x1 == 0:
                                z = inputQuery[position_comma + 1:-1].split('and') 
                                print (z)
                                m = 0
                                while m <= x2:
                                    z1 = z[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                    else:
                        z = inputQuery[position_comma + 1:position_braketEnd]
                        z = z.strip()
                        arr = []
                        arr.append(z)
                        print (z)
                    print (arr)
                    answer["fields"] = arr
                elif position_comma == -1 and position_bracket1 != -1:
                    a = inputQuery[position_bracket1 + 1:position_braketEnd]
                    a = a.strip()
                    print (a)
                    answer["input"] = a
                print (answer)
                return answer
            else:
                print("Syntax Error")
        else:
            print ("there are " + str(comma_count) +" comma's present in the string")
            if position_bracket1 != -1 and position_braketEnd != -1:
                x = inputQuery[:position_bracket1]
                x = x.strip()
                print (x)
                answer["functionName"] = x
                i = 0
                b = inputQuery.find(",")
                c = inputQuery[position_bracket1 + 1:b].strip()
                print (c)
                answer["input"] = c
                position_bracket1 = b
                i = b + 1
                if b != (-1):
                    while i < len(inputQuery):
                        b = inputQuery.find(",",i)
                        c = inputQuery[position_bracket1 + 1:b].strip()
                        print (c)
                        c = c.split()
                        flag = False
                        j = ''
                        for j in arr1:
                            if j in c:
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
                print (answer)
                return answer
            else:
                print("Syntax Error")
    else:
        inputQuery1 = inputQuery.split(":=")
        inputQuery2 = inputQuery1[1]
        inputQuery2 = inputQuery2.strip()
        position_bracket1 = None
        position_comma = None
        position_braketEnd = None 
        position_character = None
        length_x = len(inputQuery2)
        position_bracket1 = inputQuery2.find("(") #finds the position of 1 bracket
        comma_count = inputQuery2.count(",") #finds the Number of Comma's
        position_comma = inputQuery2.find(",") #finds the position of First Comma
        position_braketEnd = inputQuery2.find(")") #finds the position of Last bracket
        position_character = inputQuery2.find(":=") #finds the position of Special character
        if position_character == -1:
            print("the length of string is: " + str(length_x))
        if position_bracket1 != -1:
            print ("the position of First bracket: " + str(position_bracket1))
        if position_braketEnd != -1:
            print ("the position of Last bracket: " + str(position_braketEnd))
        if comma_count != 0 and comma_count == 1: #if there is a comma present 
            if position_comma != -1:
                print ("the position of Comma: " + str(position_comma))
            if position_bracket1 != -1 and position_braketEnd == -1:
                print("Syntax Error")
            elif position_bracket1 != -1:
                a = inputQuery1[0]
                a = a.strip()
                print(a)
                answer["outputDB"] = a
                x = inputQuery2[:position_bracket1]
                x = x.strip()
                print (x)
                answer["functionName"] = x
                if position_comma != -1:
                    y = inputQuery2[position_bracket1 + 1:position_comma]
                    y = y.strip()
                    print (y)
                    answer["input"] = y
                    x1 = inputQuery[position_comma + 1:-1].count('or')
                    print (x1)
                    x2 = inputQuery[position_comma + 1:-1].count('and')
                    print (x2)
                    if x1 != 0 or x2 != 0:
                        flag = False
                        k = ''
                        z = (inputQuery2[position_comma + 1:-1].strip()).split()
                        print (z)
                        for k in arr2:
                            if k in z:
                                flag = True
                                break
                        answer['condition'] = k
                        if flag:
                            if x1 != -1 and x2 == 0:
                                z = inputQuery2[position_comma + 1:-1].split('or')
                                print (z)
                                m = 0
                                while m <= x1:
                                    z1 = z[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                            elif x2 != -1 and x1 == 0:
                                z = inputQuery2[position_comma + 1:-1].split('and') 
                                print (z)
                                m = 0
                                while m <= x2:
                                    z1 = z[m].strip()
                                    z1 = z1[1:-1].split()
                                    m = m +1
                                    arr.append(z1)
                    else:
                        z = inputQuery2[position_comma + 1:position_braketEnd]
                        z = z.strip()
                        arr = []
                        arr.append(z)
                        print (z)
                    print (arr)
                    answer["fields"] = arr
                elif position_comma == -1 and position_bracket1 != -1:
                    a = inputQuery2[position_bracket1 + 1:position_braketEnd]
                    a = a.strip()
                    print (a)
                    answer["input"] = a
                print(answer)
                return answer
            else:
                print("Syntax Error")
        else:
            print ("there are " + str(comma_count) +" comma's present in the string")
            if position_bracket1 != -1 and position_braketEnd != -1:
                a = inputQuery1[0]
                a = a.strip()
                print (a)
                answer["outputDB"] = a
                x = inputQuery2[:position_bracket1]
                x  = x.strip()
                print(x)
                answer["functionName"] = x
                i = 0
                b = inputQuery2.find(",")
                c = inputQuery2[position_bracket1 + 1:b].strip()
                print(c)
                answer["input"] = c
                position_bracket1 = b
                i = b + 1
                if b != (-1):
                    while i < len(inputQuery2):
                        b = inputQuery2.find(",",i)
                        c = inputQuery2[position_bracket1 + 1:b].strip()
                        print (c)
                        c = c.split()
                        flag = False
                        j = ''
                        for j in arr1:
                            if j in c:
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
                print (answer)
                return answer
            else:
                print("Syntax Error")