from BTrees.OOBTree import OOBTree
from collections import defaultdict
import numpy as np
from numpy.lib import recfunctions
from tabulate import tabulate

import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning)

allCollections = {}
hashedKeys = {}
bTreedKeys = {}


def printTable(collectionName):
    headers = collectionName.dtype.names
    table = tabulate(collectionName, headers, tablefmt = "grid")
    print(table)


def readFromFile(outputCollection, readFromFile):
    collection = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    allCollections[outputCollection] = collection


def project(outputCollection, collectionName, fields):
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])


def sortCollection(outputCollection, collectionName, column):
    sortedCollection = np.sort(allCollections[collectionName], order=column)
    allCollections[outputCollection] = sortedCollection
    printTable(allCollections[outputCollection])


def createHash(collectionName, column):
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        hashmap[collection[row][column]].append(row)
    hashedKeys[collectionName + '.' + column] = hashmap
    print('Created a hashmap on ' + column + 'for collection ' + collectionName)


def hashMatch(collection, column, value):
    hashmap = hashedKeys[collection + '.' + column]
    matchingRows = hashmap[value]
    matched = np.full(len(allCollections[collection]), False)
    for i in matchingRows:
        matched[i] = True
    return matched


def createBTree(collectionName, column):
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        hashmap[collection[row][column]].append(row)
    tree = OOBTree()
    tree.update(hashmap)
    bTreedKeys[collectionName + '.' + column] = tree
    print('Created a hashmap on ' + column + 'for collection ' + collectionName)


def bTreeMatch(collection, column, condition, value):
    bTree = bTreedKeys[collection + '.' + column]
    matched = np.full(len(allCollections[collection]), False)
    if condition == '<':
        matchingRows = bTree.values(max=value, excludemax=True)
    elif condition == '>':
        matchingRows = bTree.values(min=value, excludemin=True)
    elif condition == '<=':
        matchingRows = bTree.values(max=value, excludemax=False)
    elif condition == '>=':
        matchingRows = bTree.values(min=value, excludemin=False)
    elif condition == '=':
        if value in bTree:
            matchingRows = [bTree[value]]
        else:
            matchingRows = []
    for key in matchingRows: 
        for row in key:
            matched[row] = True
    return matched


def select(outputCollection, collectionName, conditions, operator):
    allResults = []
    collection = allCollections[collectionName]
    for condition in conditions:
        compare = np.asarray([condition[2]]).astype(collection.dtype[condition[0]])
        if condition[1] == '=' and collectionName + '.' + condition[0] in hashedKeys:
            print('Using the Hash generated earlier to check for the value')
            result = hashMatch(collectionName, condition[0], compare[0])
        elif condition[1] != '!=' and collectionName + '.' + condition[0] in bTreedKeys:
            print('Using the Btree generated earlier to check for the value')
            result = bTreeMatch(collectionName, condition[0], condition[1], compare[0])
        else:
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

def findSumByGroup(outputCollection, collectionName, column, groupBy):
    collection = allCollections[collectionName]
    uniqueCombinations = np.unique(collection[groupBy])
    groupBySums = np.array( [ np.sum(collection[collection[groupBy] == row][column]) for row in uniqueCombinations] )
    groupedCollection = recfunctions.append_fields(uniqueCombinations, 'sum(' + column + ')', groupBySums, usemask=False)
    allCollections[outputCollection] = groupedCollection
    printTable(allCollections[outputCollection])


def findAverageByGroup(outputCollection, collectionName, column, groupBy):
    collection = allCollections[collectionName]
    uniqueCombinations = np.unique(collection[groupBy])
    groupByAvgs = np.array( [ np.mean(collection[collection[groupBy] == row][column]) for row in uniqueCombinations] )
    groupedCollection = recfunctions.append_fields(uniqueCombinations, 'avg(' + column + ')', groupByAvgs, usemask=False)
    allCollections[outputCollection] = groupedCollection
    printTable(allCollections[outputCollection])