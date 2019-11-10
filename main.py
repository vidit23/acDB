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
        engine.findAverage(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'max':
        # Find the Maximum value of a column
        engine.findMax(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'sum':
        # Find the sum of all the values in a column
        engine.findSum(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'])
    elif queryMeaning['functionName'] == 'Hash':
        # Create a hashmap for a particular column
        engine.createHash(queryMeaning['input'], queryMeaning['fields'])

# groupby function 
# n = np.unique(a[:,0])
# np.array( [ list(a[a[:,0]==i,1]) for i in n] )


while 1:
    query = input('Enter your query: ')
    if query == 'quit':
        break
    queryMeaning = parser(query)
    print('Extracted meaning: ', queryMeaning)
    functionalityChooser({'outputDB': 'R', 
                        'functionName': 'inputfromfile', 
                        'input':'myfile.csv',
                        'fields': None,
                        'condition': None })
    
    functionalityChooser({'outputDB': 'R1', 
                        'functionName': 'project', 
                        'input':'R',
                        'fields': ['id', 'name'],
                        'condition': None })
    
    functionalityChooser({'outputDB': 'R3', 
                        'functionName': 'select', 
                        'input':'R',
                        'fields': [[],[],[]],
                        'condition': 'or' })

    functionalityChooser({'outputDB': 'R1', 
                        'functionName': 'project', 
                        'input':'R',
                        'fields': ['id', 'name'],
                        'condition': None })
