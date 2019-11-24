from parser import parser
import engine

import numpy as np

def functionalityChooser(queryMeaning):
    if queryMeaning['functionName'] == 'inputfromfile':
        # Read from a file
        engine.readFromFile(queryMeaning['outputDB'], queryMeaning['input'])
    elif queryMeaning['functionName'] == 'project':
        # Select a particular set of columns from a collection
        engine.project(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'sort':
        # Sort the collection based on a set of columns
        engine.sortCollection(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
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
        engine.findMovingSum(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1])
    elif queryMeaning['functionName'] == 'movavg':
        # Find the moving average of all the values in a column based on window size
        engine.findMovingAverage(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1])
    elif queryMeaning['functionName'] == 'Hash':
        # Create a hashmap for a particular column
        engine.createHash(queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'BTree':
        # Create a hashmap for a particular column
        engine.createBTree(queryMeaning['input'], queryMeaning['fields'][0])

# groupby function 
# n = np.unique(a[:,0])
# np.array( [ list(a[a[:,0]==i,1]) for i in n] )


while 1:
    query = input('Enter your query: ')
    if query == 'quit':
        break
    queryMeaning = parser(query)
    print('Extracted meaning: ', queryMeaning)
    functionalityChooser(queryMeaning)
    # functionalityChooser({'outputDB': 'R', 
    #                     'functionName': 'inputfromfile', 
    #                     'input':'myfile.csv',
    #                     'fields': None,
    #                     'condition': None })
    
    # functionalityChooser({'outputDB': 'R1', 
    #                     'functionName': 'project', 
    #                     'input':'R',
    #                     'fields': ['id', 'age'],
    #                     'condition': None })
    
    # functionalityChooser({'outputDB': 'R3', 
    #                     'functionName': 'select', 
    #                     'input':'R',
    #                     'fields': [['job', '=', 'ba'],['sal', '>', '100']],
    #                     'condition': 'or' })

    # functionalityChooser({'outputDB': 'R4', 
    #                     'functionName': 'avg', 
    #                     'input':'R',
    #                     'fields': ['sal'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R5', 
    #                     'functionName': 'sum', 
    #                     'input':'R',
    #                     'fields': ['sal'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R6', 
    #                     'functionName': 'max', 
    #                     'input':'R',
    #                     'fields': ['sal'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': None, 
    #                     'functionName': 'Hash', 
    #                     'input':'R',
    #                     'fields': ['name'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': None, 
    #                     'functionName': 'BTree', 
    #                     'input':'R',
    #                     'fields': ['age'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R7', 
    #                     'functionName': 'select', 
    #                     'input':'R',
    #                     'fields': [['name', '=', 'vidit'],['age', '=', '23']],
    #                     'condition': 'or' })
                
    # functionalityChooser({'outputDB': 'R8', 
    #                     'functionName': 'sumgroup', 
    #                     'input':'R',
    #                     'fields': ['sal', 'job', 'name'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R9', 
    #                     'functionName': 'avggroup', 
    #                     'input':'R',
    #                     'fields': ['sal', 'job'],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R10', 
    #                     'functionName': 'movsum', 
    #                     'input':'R',
    #                     'fields': ['age', 3],
    #                     'condition': None })

    # functionalityChooser({'outputDB': 'R11', 
    #                     'functionName': 'movavg', 
    #                     'input':'R',
    #                     'fields': ['sal', 2],
    #                     'condition': None })
