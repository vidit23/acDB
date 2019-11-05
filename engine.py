import numpy as np
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning)

allCollections = {}

def readFromFile(outputCollection, readFromFile):
    collection = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    allCollections[outputCollection] = collection

def printTable(collectionName):
    headers = collectionName.dtype.names
    table = tabulate(collectionName, headers, tablefmt = "grid")
    print(table)

def project(outputCollection, collectionName, fields):
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])

def select(outputCollection, collectionName, conditions, operator):
    allResults = []
    collection = allCollections[collectionName]
    for condition in conditions:
        compare = np.asarray([condition[2]]).astype(collection.dtype[condition[0]])
        if condition[1] == '<':
            result = collection[condition[0]] < compare
        elif condition[1] == '>':
            result = collection[condition[0]] > compare
        elif condition[1] == '<=':
            result = collection[condition[0]] <= compare
        elif condition[1] == '>=':
            result = collection[condition[0]] >= compare
        elif condition[1] == '!=':
            result = collection[condition[0]] != compare
        elif condition[1] == '=':
            result = collection[condition[0]] == compare
        allResults.append(result)
    allResults = np.asarray(allResults)
    if operator == 'or':
        allCollections[outputCollection] = np.any(allResults, axis = 0)
    elif operator == 'and':
        allCollections[outputCollection] = np.all(allResults, axis = 0)

def findAverage(collectionName, column):
    col = allCollections[collectionName][column] 
    mean = np.mean(col)
    print("The Mean for the column " + column + " is " + str(mean))

def findMax(collectionName, column):
    col = allCollections[collectionName][column] 
    colMax = np.max(col)
    print("The Maximum for the column " + column + " is " + str(colMax))

def findSum(collectionName, column):
    col = allCollections[collectionName][column] 
    colSum = np.sum(col)
    print("The Sum for the column " + column + " is " + str(colSum))

def sortCollection(collectionName, column, sortedCollectionName):
    sortedCollection = np.sort(allCollections[collectionName], order=column)
    allCollections[sortedCollectionName] = sortedCollection