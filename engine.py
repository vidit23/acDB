from collections import defaultdict
import numpy as np
from tabulate import tabulate

import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning)

allCollections = {}
hashedKeys = {}
btreedKeys = {}


def printTable(collectionName):
    headers = collectionName.dtype.names
    table = tabulate(collectionName, headers, tablefmt = "grid")
    print(table)


def readFromFile(outputCollection, readFromFile):
    collection = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    allCollections[outputCollection] = collection


def createHash(collectionName, column):
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        hashmap[collection[row][column]].append(row)
    hashedKeys[collectionName + '.' + col] = hashmap
    print('Created a hashmap on ' + column + 'for collection ' + collectionName)


def hashMatch(collection, column, value):
    hashmap = hashedKeys[collection + '.' + column]
    matchingRows = hashmap[value[0]]
    matched = np.full(len(allCollections[collection]), False)
    for i in matchingRows:
        matched[i] = True
    return matched


def project(outputCollection, collectionName, fields):
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])


def sortCollection(outputCollection, collectionName, column):
    sortedCollection = np.sort(allCollections[collectionName], order=column)
    allCollections[outputCollection] = sortedCollection
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
            if collectionName + '.' + condition[0] in hashedKeys:
                result = hashMatch(collectionName, condition[0], compare)
            else:
                result = collection[condition[0]] == compare
        allResults.append(result)
    allResults = np.asarray(allResults)
    if operator == 'or':
        allCollections[outputCollection] = np.extract(np.any(allResults, axis = 0), collection)
    elif operator == 'and':
        allCollections[outputCollection] = np.extract(np.all(allResults, axis = 0), collection)
    printTable(allCollections[outputCollection])


def findAverage(outputCollection, collectionName, column):
    col = allCollections[collectionName][column] 
    mean = np.mean(col)
    allCollections[outputCollection] = np.array([(mean)], dtype=[('mean(' + column + ')', 'float_')])
    printTable(allCollections[outputCollection])


def findMax(outputCollection, collectionName, column):
    col = allCollections[collectionName][column] 
    colMax = np.max(col)
    allCollections[outputCollection] = np.array([(colMax)], dtype=[('max(' + column + ')', col.dtype)])
    printTable(allCollections[outputCollection])


def findSum(outputCollection, collectionName, column):
    col = allCollections[collectionName][column] 
    colSum = np.sum(col)
    allCollections[outputCollection] = np.array([(colSum)], dtype=[('sum(' + column + ')', col.dtype)])
    printTable(allCollections[outputCollection])