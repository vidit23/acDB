import numpy as np
import time

from parser import parser
import engine
import tests.testBackend as test

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
    elif queryMeaning['functionName'] == 'BTree':
        # Create a hashmap for a particular column
        engine.createBTree(queryMeaning['input'], queryMeaning['fields'][0])
    elif queryMeaning['functionName'] == 'join':
        # Create a hashmap for a particular column
        engine.join(queryMeaning['outputDB'], queryMeaning['input'], queryMeaning['fields'][0], queryMeaning['fields'][1:], queryMeaning['condition'])
    else:
        print('The command ' + queryMeaning['functionName'] + ' is not recognized')


while 1:
    query = input('Enter your query: ')
    if query == 'quit':
        break
    elif query == 'test':
        test.runningBackendTests()
        continue
    queryMeaning = parser(query)
    print('\n\n\n\nExtracted meaning: ', queryMeaning)
    try:
        startTime = time.time()
        functionalityChooser(queryMeaning)
        print("It took " + str(time.time() - startTime) + " seconds to execute this query")
    except Exception as err:
        print("There was an error in processing the query")
        print(err)
