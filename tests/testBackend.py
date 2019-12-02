import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

import engine


def functionalityChooser(queryMeaning):
    if queryMeaning['functionName'] == 'inputfromfile':
        # Read from a file
        engine.readFromFile(queryMeaning['outputDB'], queryMeaning['input'])
    elif queryMeaning['functionName'] == 'outputtofile':
        # Output to a file
        engine.outputToFile(queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'project':
        # Select a particular set of columns from a collection
        engine.project(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'sort':
        # Sort the collection based on a set of columns
        engine.sortCollection(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'concat':
        # Concatenate two collections
        engine.concatenateCollection(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'select':
        # Select rows from a collection based on some conditions
        engine.select(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'], queryMeaning['condition'])
    elif queryMeaning['functionName'] == 'avg':
        # Find the average value of a column
        engine.findAverage(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'max':
        # Find the Maximum value of a column
        engine.findMax(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'sum':
        # Find the sum of all the values in a column
        engine.findSum(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'sumgroup':
        # Find the sum of all the values in a column after grouping
        engine.findSumByGroup(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1:])
    elif queryMeaning['functionName'] == 'avggroup':
        # Find the average of all the values in a column after grouping
        engine.findAverageByGroup(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1:])
    elif queryMeaning['functionName'] == 'movsum':
        # Find the moving sum of all the values in a column based on window size
        engine.findMovingSum(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], int(queryMeaning['fields'][1]))
    elif queryMeaning['functionName'] == 'movavg':
        # Find the moving average of all the values in a column based on window size
        engine.findMovingAverage(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], int(queryMeaning['fields'][1]))
    elif queryMeaning['functionName'] == 'Hash':
        # Create a hashmap for a particular column
        engine.createHash(queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'Btree':
        # Create a hashmap for a particular column
        engine.createBTree(queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'join':
        # Create a hashmap for a particular column
        engine.join(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1:], queryMeaning['condition'])
    else:
        print('The command ' + queryMeaning['functionName'] + ' is not recognized')


def runningBackendTests():
    print('\n\n\n\n\nR := inputfromfile(sales1)')
    functionalityChooser({'outputDB': 'R', 
                        'functionName': 'inputfromfile', 
                        'input':'sales1',
                        'fields': None,
                        'condition': None })

    print('\n\n\n\n\nR1 := select(R, (time > 50) or (qty < 30))')
    functionalityChooser({'outputDB': 'R1', 
                        'functionName': 'select', 
                        'input':'R',
                        'fields': [['time', '>', '50'],['qty', '<', '30']],
                        'condition': 'or' })

    print('\n\n\n\n\nR2 := project(R1, saleid, qty, pricerange)')
    functionalityChooser({'outputDB': 'R2', 
                        'functionName': 'project', 
                        'input':'R1',
                        'fields': ['saleid', 'qty', 'pricerange'],
                        'condition': None })

    print('\n\n\n\n\nR3 := avg(R1, qty)')
    functionalityChooser({'outputDB': 'R3', 
                        'functionName': 'avg', 
                        'input':'R1',
                        'fields': ['qty'],
                        'condition': None })

    print('\n\n\n\n\nR4 := sumgroup(R1, time, qty)')
    functionalityChooser({'outputDB': 'R4', 
                        'functionName': 'sumgroup', 
                        'input':'R1',
                        'fields': ['time', 'qty'],
                        'condition': None })

    print('\n\n\n\n\nR5 := sumgroup(R1, qty, time, pricerange)')
    functionalityChooser({'outputDB': 'R5', 
                        'functionName': 'sumgroup', 
                        'input':'R1',
                        'fields': ['qty', 'time', 'pricerange'],
                        'condition': None })

    print('\n\n\n\n\nR6 := avggroup(R1, qty, pricerange)')
    functionalityChooser({'outputDB': 'R6', 
                        'functionName': 'avggroup', 
                        'input':'R1',
                        'fields': ['qty', 'pricerange'],
                        'condition': None })

    print('\n\n\n\n\nS := inputfromfile(sales2)')
    functionalityChooser({'outputDB': 'S', 
                        'functionName': 'inputfromfile', 
                        'input':'sales2',
                        'fields': None,
                        'condition': None })
    
    print('\n\n\n\n\nT := join(R, S, R.customerid = S.C)')
    functionalityChooser({'outputDB': 'T', 
                        'functionName': 'join', 
                        'input':'R',
                        'fields': ['S', ['R.customerid', '=', 'S.C']],
                        'condition': None })

    print('\n\n\n\n\nT1 := join(R1, S, (R1.qty > S.Q) and (R.customerid = S.C))')
    functionalityChooser({'outputDB': 'T1', 
                        'functionName': 'join', 
                        'input':'R1',
                        'fields': ['S', ['R1.qty', '>', 'S.Q'], ['S.saleid', '=', 'R1.saleid']],
                        'condition': 'and' })
    
    print('\n\n\n\n\nT2 := sort(T1, S_C)')
    functionalityChooser({'outputDB': 'T2', 
                        'functionName': 'sort', 
                        'input':'T1',
                        'fields': ['S_C'],
                        'condition': None })
    
    print('\n\n\n\n\nT2prime := sort(T1, R1_time, S_C)')
    functionalityChooser({'outputDB': 'T2prime', 
                        'functionName': 'sort', 
                        'input':'T1',
                        'fields': ['R1_time', 'S_C'],
                        'condition': None })

    print('\n\n\n\n\nT3 := movavg(T2prime, R1_qty, 3)')
    functionalityChooser({'outputDB': 'T3', 
                        'functionName': 'movavg', 
                        'input':'T2prime',
                        'fields': ['R1_qty', '3'],
                        'condition': None })

    print('\n\n\n\n\nT4 := movsum(T2prime, R1_qty, 5)')
    functionalityChooser({'outputDB': 'T4', 
                        'functionName': 'movsum', 
                        'input':'T2prime',
                        'fields': ['R1_qty', '5'],
                        'condition': None })

    print('\n\n\n\n\nQ1 := select(R, qty = 5)')
    functionalityChooser({'outputDB': 'Q1', 
                        'functionName': 'select', 
                        'input':'R',
                        'fields': [['qty', '=', '5']],
                        'condition': None })

    print('\n\n\n\n\nBtree(R, qty)')
    functionalityChooser({'outputDB': None, 
                        'functionName': 'Btree', 
                        'input':'R',
                        'fields': ['qty'],
                        'condition': None })

    print('\n\n\n\n\nQ2 := select(R, qty = 5)')
    functionalityChooser({'outputDB': 'Q2', 
                        'functionName': 'select', 
                        'input':'R',
                        'fields': [['qty', '=', '5']],
                        'condition': None })

    print('\n\n\n\n\nHash(R,itemid)')
    functionalityChooser({'outputDB': None, 
                        'functionName': 'Hash', 
                        'input':'R',
                        'fields': ['itemid'],
                        'condition': None })

    print('\n\n\n\n\nQ4 := select(R, itemid = 7)')
    functionalityChooser({'outputDB': 'Q4', 
                        'functionName': 'select', 
                        'input':'R',
                        'fields': [['itemid', '=', '7']],
                        'condition': None })

    print('\n\n\n\n\nQ5 := concat(Q4, Q2)')
    functionalityChooser({'outputDB': 'Q5', 
                        'functionName': 'concat', 
                        'input':'Q4',
                        'fields': ['Q2'],
                        'condition': None })

    print('\n\n\n\n\noutputtofile(Q5, Q5)')
    functionalityChooser({'outputDB': None, 
                        'functionName': 'outputtofile', 
                        'input':'Q5',
                        'fields': ['Q5'],
                        'condition': None })