from BTrees.OOBTree import OOBTree
from collections import defaultdict
import numpy as np
from numpy.lib import recfunctions
from tabulate import tabulate

import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning)

# Contains all collections with keys as their name and numpy array as value
allCollections = {}
# Stores all the hashes generated in the form "collectionName.column: hashmap" 
hashedKeys = {}
# Stores all the BTrees generated in the form "collectionName.column: BTree" 
bTreedKeys = {}


def findDataType(param):
    try:
        num = int(param)
    except ValueError:
        try:
            num = float(param)
        except ValueError:
            num = str.encode(param)
    return num


def printTable(collection, limit = 10):
    # Finds the column names of the collection
    headers = collection.dtype.names
    # Forms a table in a pretty manner
    table = tabulate(collection[: limit], headers, tablefmt = "grid")
    print(table)
    print("Number of rows returned: " + str(len(collection)))


def readFromFile(outputCollection, readFromFile):
    # Read data from a file in which the first line is the name of columns and each column is followed by a |
    collection = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    # Stores the read collection into a global variable that can be accessed anywhere in this file
    allCollections[outputCollection] = collection
    printTable(allCollections[outputCollection])


def outputToFile(collection, fileName):
    prefix = ''
    headers = allCollections[collection].dtype.names
    for name in headers:
        prefix += ('|' + name)
        
    with open(fileName, 'w') as filePointer:
        filePointer.write(prefix[1:] + '\n')
        for row in allCollections[collection]:
            rowInStr = ''
            for field in row:
                if type(field) == np.bytes_:
                    rowInStr += ('|' + bytes.decode(field))
                else:
                    rowInStr += ('|' + str(field))
            filePointer.write(rowInStr[1:] + '\n')


def project(outputCollection, collectionName, fields):
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])


def sortCollection(outputCollection, collectionName, column):
    sortedCollection = np.sort(allCollections[collectionName], order=column)
    allCollections[outputCollection] = sortedCollection
    printTable(allCollections[outputCollection])


def concatenateCollection(outputCollection, collection1, collection2):
    try:
        concatenatedCollection = np.concatenate((allCollections[collection1], allCollections[collection2]), axis = 0)
        allCollections[outputCollection] = concatenatedCollection
        printTable(allCollections[outputCollection])
    except:
        print('The columns do not match')


def createHash(collectionName, column):
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        hashmap[collection[row][column]].append(row)
    hashedKeys[collectionName + '.' + column] = hashmap
    print('Created a hashmap on ' + column + ' for collection ' + collectionName)


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
    print('Created a BTree on ' + column + ' for collection ' + collectionName)


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


def findComparatorMeaning(comparator, collection):
    if comparator in collection.dtype.names:
        return collection[comparator]
    elif '+' in comparator:
        comparator = comparator.split('+')
        comparator = [i.strip() for i in comparator]
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] + findDataType(comparator[1])
        else:
            return findDataType(comparator[0]) + findDataType(comparator[1])
    elif '-' in comparator: 
        comparator = comparator.split('-')
        comparator = [i.strip() for i in comparator]
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] + findDataType(comparator[1])
        else:
            return findDataType(comparator[0]) + findDataType(comparator[1])
    elif '*' in comparator: 
        comparator = comparator.split('*')
        comparator = [i.strip() for i in comparator]
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] + findDataType(comparator[1])
        else:
            return findDataType(comparator[0]) + findDataType(comparator[1])
    elif '/' in comparator:
        comparator = comparator.split('/')
        comparator = [i.strip() for i in comparator]
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] + findDataType(comparator[1])
        else:
            return findDataType(comparator[0]) + findDataType(comparator[1])
    else:
        return findDataType(comparator)


def select(outputCollection, collectionName, conditions, operator):
    allResults = []
    collection = allCollections[collectionName]
    for condition in conditions:     
        if condition[1] == '=' and collectionName + '.' + condition[0] in hashedKeys:
            print('Using the Hash generated earlier to check for the value')
            compare = np.asarray([condition[2]]).astype(collection.dtype[condition[0]])
            result = hashMatch(collectionName, condition[0], compare[0])
        elif condition[1] == '=' and collectionName + '.' + condition[2] in hashedKeys:
            print('Using the Hash generated earlier to check for the value')
            compare = np.asarray([condition[0]]).astype(collection.dtype[condition[2]])
            result = hashMatch(collectionName, condition[2], compare[0])
        elif condition[1] != '!=' and collectionName + '.' + condition[0] in bTreedKeys:
            print('Using the Btree generated earlier to check for the value')
            compare = np.asarray([condition[2]]).astype(collection.dtype[condition[0]])
            result = bTreeMatch(collectionName, condition[0], condition[1], compare[0])
        elif condition[1] != '!=' and collectionName + '.' + condition[2] in bTreedKeys:
            print('Using the Btree generated earlier to check for the value')
            compare = np.asarray([condition[0]]).astype(collection.dtype[condition[2]])
            result = bTreeMatch(collectionName, condition[2], condition[1], compare[0])
        else:
            lhs = findComparatorMeaning(condition[0], collection)
            rhs = findComparatorMeaning(condition[2], collection)   
            if condition[1] == '<':
                result = lhs < rhs
            elif condition[1] == '>':
                result = lhs > rhs
            elif condition[1] == '<=':
                result = lhs <= rhs
            elif condition[1] == '>=':
                result = lhs >= rhs
            elif condition[1] == '!=':
                result = lhs != rhs
            elif condition[1] == '=':
                result = lhs == rhs
        allResults.append(result)

    allResults = np.asarray(allResults)
    if operator == 'and':
        allCollections[outputCollection] = np.extract(np.all(allResults, axis = 0), collection)
    else:
        allCollections[outputCollection] = np.extract(np.any(allResults, axis = 0), collection)
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


def findMovingSum(outputCollection, collectionName, column, windowSize):
    wholeColumn = allCollections[collectionName][column]
    movingSum = []
    sumTillHere = 0
    for rowNum in range(len(wholeColumn)):
        if rowNum < windowSize:
            sumTillHere += wholeColumn[rowNum]
        else:
            sumTillHere -= wholeColumn[rowNum - windowSize]
            sumTillHere += wholeColumn[rowNum]
        movingSum.append(sumTillHere)
    allCollections[outputCollection] = np.array(movingSum, dtype=[('movsum(' + column + ')', wholeColumn.dtype)])
    printTable(allCollections[outputCollection])


def findMovingAverage(outputCollection, collectionName, column, windowSize):
    wholeColumn = allCollections[collectionName][column]
    movingAverage = []
    sumTillHere = 0
    for rowNum in range(len(wholeColumn)):
        if rowNum < windowSize:
            sumTillHere += wholeColumn[rowNum]
            movingAverage.append(sumTillHere / (rowNum + 1))
        else:
            sumTillHere -= wholeColumn[rowNum - windowSize]
            sumTillHere += wholeColumn[rowNum]
            movingAverage.append(sumTillHere / windowSize)
    allCollections[outputCollection] = np.array(movingAverage, dtype=[('movavg(' + column + ')', 'float_')])
    printTable(allCollections[outputCollection])

