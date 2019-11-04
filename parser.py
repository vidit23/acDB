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
    meaning = {}
    position_bracket1 = None
    position_comma = None
    position_braketEnd = None 
    length_x = len(inputQuery)
    position_bracket1 = inputQuery.find("(") #finds the position of 1 bracket
    comma_count = inputQuery.count(",") #finds the Number of Comma's
    position_comma = inputQuery.find(",") #finds the position of First Comma
    position_braketEnd = inputQuery.find(")") #finds the position of Last bracket
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
            print(inputQuery[:position_bracket1])
            if position_comma != -1:
                print(inputQuery[position_bracket1 + 1:position_comma])
                print(inputQuery[position_comma + 1:position_braketEnd])
            elif position_comma == -1 and position_bracket1 != -1:
                print(inputQuery[position_bracket1 + 1:position_braketEnd])
        else:
            print(inputQuery)
    else:
        print ("there are " + str(comma_count) +" comma's present in the string")
        if position_bracket1 != -1 and position_braketEnd != -1:
            print(inputQuery[:position_bracket1])
            i = 0
            while i < len(inputQuery):
                b = inputQuery.find(",",i)
                print(inputQuery[position_bracket1 + 1:b])
                position_bracket1 = b
                i = b + 1
                if b == (-1):
                    break
        else:
            print("Syntax Error")
    return meaning
