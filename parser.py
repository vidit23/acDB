
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
