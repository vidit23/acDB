from parser import parser
import engine

import numpy as np

def functionalityChooser(queryMeaning):
    if queryMeaning["functionName"] == "inputfromfile":
        engine.readFromFile(queryMeaning["outputDB"], queryMeaning["input"])
    elif queryMeaning["functionName"] == "project":
        engine.project(queryMeaning["outputDB"], queryMeaning["input"], queryMeaning["fields"])

# groupby function 
# n = np.unique(a[:,0])
# np.array( [ list(a[a[:,0]==i,1]) for i in n] )


while 1:
    query = input('Enter your query: ')
    if query == 'quit':
        break
    queryMeaning = parser(query)
    print('Extracted meaning: ', queryMeaning)
    functionalityChooser({"outputDB": 'R', 
                        "functionName": 'inputfromfile', 
                        "input":'myfile.csv',
                        "fields": None,
                        "condition": None })
    
    functionalityChooser({"outputDB": 'R1', 
                        "functionName": 'project', 
                        "input":'R',
                        "fields": ['id', 'name'],
                        "condition": None })
