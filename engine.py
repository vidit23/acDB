from BTrees.OOBTree import OOBTree
from collections import defaultdict
from copy import copy, deepcopy
import numpy as np
from numpy.lib import recfunctions as rfn
import re
from tabulate import tabulate

import warnings
warnings.filterwarnings('ignore', category = np.VisibleDeprecationWarning)

# Contains all collections with keys as their name and numpy array as value
allCollections = {}
# Stores all the hashes generated in the form 'collectionName_column: hashmap' 
hashedKeys = {}
# Stores all the BTrees generated in the form 'collectionName_column: BTree' 
bTreedKeys = {}


def findDataType(param):
    """Converts the argument passed to respective data type namely
    int, float or string

    Parameters
    ----------
    param : str
        The parameter in the query
    """
    try:
        num = int(param)
    except ValueError:
        try:
            num = float(param)
        except ValueError:
            num = str.encode(param)
    return num


def checkIfIndexed(column):
    """Checks if the collectionName.column exists in either hashedKeys or bTreedKeys

    Parameters
    ----------
    column : str
        The key to check in the dictionary
    """
    if column in hashedKeys or column in bTreedKeys:
        return True
    else:
        return False


def canEval(expression):
    """Checks whether a string can be evaluated as an mathematical expression

    Parameters
    ----------
    expression : str
        The expression on either side of the query
    """
    try:
        eval(expression)
        return True
    except:
        return False


def printTable(collection, limit = 5):
    """Prints the given collection in a readable format

    Parameters
    ----------
    collection : numpy structured array
        The whole collection we want to display as a 2-D array
    limit : int, optional
        Number of rows to display (default is 10)
    """
    # Finds the column names of the collection
    headers = collection.dtype.names
    # Forms a table in a pretty manner
    table = tabulate(collection[: limit], headers, tablefmt = "grid")
    print(table)
    print('Number of rows returned: ' + str(len(collection)))


def readFromFile(outputCollection, readFromFile):
    """Reads data from a file and stores it in a global variable with given name
    
    Parameters
    ----------
    outputCollection : str
        The name of the collection we store it as
    readFromFile : str
        The file name from which we are supposed to read
    """
    # Read data from a file in which the first line is the name of columns and each column is followed by a |
    collection = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    # Stores the read collection into a global variable that can be accessed anywhere in this file
    allCollections[outputCollection] = collection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def outputToFile(collection, fileName, writeType):
    """Outputs a specified collection onto a file
    
    Parameters
    ----------
    collection : str
        The name of the collection we output
    fileName : str
        The file name we output to
    """
    # Storing all the headers into a string
    prefix = ''
    headers = allCollections[collection].dtype.names
    for name in headers:
        prefix += ('|' + name)
    
    with open('vvb238_dk3718_' + fileName, writeType) as filePointer:
        if writeType == 'a+':
            filePointer.write('\n\n\n')
        # Writing the headers into the file first
        filePointer.write(prefix[1:])
        # Going row by row to write into the file
        for row in allCollections[collection]:
            rowInStr = ''
            for field in row:
                # Converting bytes columns to string
                if type(field) == np.bytes_:
                    rowInStr += ('|' + bytes.decode(field))
                # Converting int or float columns to string
                else:
                    rowInStr += ('|' + str(field))
            filePointer.write('\n' + rowInStr[1:])
        if writeType == 'a+':
            filePointer.write('\n\nNumber of rows in the table: ' + str(len(allCollections[collection])))
        


def project(outputCollection, collectionName, fields):
    """Selects the specified columnns in the given order from a collections 
    and stores it in another collection
    
    Parameters
    ----------
    outputCollection : str
        The name of the collection we output
    collectionName : str
        The name of the collection we want to prune
    fields : Array[str]
        All the columns we need from the given collection
    """
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def sortCollection(outputCollection, collectionName, column):
    """Sorts the given collection based on specified columns
    
    Parameters
    ----------
    outputCollection : str
        The name of the collection we output
    collectionName : str
        The name of the collection we want to sort
    fields : Array[str]
        All the columns we need to sort by
    """
    sortedCollection = np.sort(allCollections[collectionName], order=column)
    allCollections[outputCollection] = sortedCollection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def concatenateCollection(outputCollection, collection1, collection2):
    """Concatenates the second collection below the first collection
    
    Parameters
    ----------
    outputCollection : str
        The name of the collection we output
    collection1 : str
        The name of the first collection
    collection2 : str
        The name of the first collection
    """
    try:
        concatenatedCollection = np.concatenate((allCollections[collection1], allCollections[collection2]), axis = 0)
        allCollections[outputCollection] = concatenatedCollection
        printTable(allCollections[outputCollection])
        outputToFile(outputCollection, 'allOperations', 'a+')
    except:
        print('The column names do not match or they are not in the same order. Try project first')


def createHash(collectionName, column):
    """Creates a hashmap for the given collection based on specific column
    
    Parameters
    ----------
    collectionName : str
        The name of the collection we want to create hash for
    column : str
        Column we use to create hash
    """
    # Creating a defaultdict to prevent KeyError and if a key is not present, it is intialized to empty array
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        # Hash stores the columns value and the index it is present in
        hashmap[collection[row][column]].append(row)
    # We store the hash in a global variable with key collectionName.column
    hashedKeys[collectionName + '_' + column] = hashmap
    print('Created a hashmap on ' + column + ' for collection ' + collectionName)


def hashMatch(collection, column, value):
    """Uses Hash to search for the columns that hold a particular value
    
    Parameters
    ----------
    collectionName : str
        The name of the collection we want to create hash for
    column : str
        Column we use to create hash
    value : any
        Value we have to check for
    """
    # Fetching the hash from global variable
    hashmap = hashedKeys[collection + '_' + column]
    # Finding all the rows that match the value
    matchingRows = hashmap[value]
    # Making an array with False values that is equal to the size of the collection
    matched = np.full(len(allCollections[collection]), False)
    # Marking only the rows that match as True
    for i in matchingRows:
        matched[i] = True
    return matched


def createBTree(collectionName, column):
    """Creates a BTree for the given collection based on specific column
    
    Parameters
    ----------
    collectionName : str
        The name of the collection we want to create BTree for
    column : str
        Column we use to create BTree
    """
    # Creating a defaultdict to prevent KeyError and if a key is not present, it is intialized to empty array
    hashmap = defaultdict(lambda: [])
    collection = allCollections[collectionName]
    for row in range(len(collection)):
        hashmap[collection[row][column]].append(row)
    # Intializing the empty BTree
    tree = OOBTree()
    # To update the tree we need hash of all values which is calculated above
    tree.update(hashmap)
    bTreedKeys[collectionName + '_' + column] = tree
    print('Created a BTree on ' + column + ' for collection ' + collectionName)


def bTreeMatch(collection, column, condition, value):
    """Uses BTree to search for the columns that hold a particular value or a range
    
    Parameters
    ----------
    collectionName : str
        The name of the collection we want to create hash for
    column : str
        Column we use to create hash
    condition : char
        Value we have to check for
    value : any
        Value we have to check for
    """
    bTree = bTreedKeys[collection + '_' + column]
    matched = np.full(len(allCollections[collection]), False)
    # Finding the rows that satisfy the given condition
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
    # We get an array of array containing all the row number and we mark it as True
    for key in matchingRows: 
        for row in key:
            matched[row] = True
    return matched


def findComparatorMeaning(comparator, collection):
    """Takes one side of the comparison query and alters the collection accordingly
    Interprets the following: (Column | Constant) [+|-|*|/ Constant]
    
    Parameters
    ----------
    comparator : str
        The string which we are trying to understand
    collection : numpy structured array
        Collection we have to compare on
    """
    # If it is only a column name
    if comparator in collection.dtype.names:
        return collection[comparator]
    elif '+' in comparator:
        comparator = comparator.split('+')
        comparator = [i.strip() for i in comparator]
        # If we are trying to add to a column
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] + findDataType(comparator[1])
        # If we are trying to add two constants
        else:
            return findDataType(comparator[0]) + findDataType(comparator[1])
    elif '-' in comparator: 
        comparator = comparator.split('-')
        comparator = [i.strip() for i in comparator]
        # If we are trying to subtract from a column
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] - findDataType(comparator[1])
        # If we are trying to subtract two constants
        else:
            return findDataType(comparator[0]) - findDataType(comparator[1])
    elif '*' in comparator: 
        comparator = comparator.split('*')
        comparator = [i.strip() for i in comparator]
        # If we are trying to multiply to a column
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] * findDataType(comparator[1])
        # If we are trying to multiply two constants
        else:
            return findDataType(comparator[0]) * findDataType(comparator[1])
    elif '/' in comparator:
        comparator = comparator.split('/')
        comparator = [i.strip() for i in comparator]
        # If we are trying to divide a column
        if comparator[0] in collection.dtype.names:
            return collection[comparator[0]] / findDataType(comparator[1])
        # If we are trying to divide two constants
        else:
            return findDataType(comparator[0]) / findDataType(comparator[1])
    else:
        return findDataType(comparator)


def select(outputCollection, collectionName, conditions, operator):
    """Filters rows in a collection based on the conditions provided
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we run the conditions on
    conditions : array(array(str))
        of the form [['columnName', '>=', '60'],['4 - 7','!=','columnName * 6']]
    operator : str
        The operator as which we combine the conditions (and/or)
    """
    allResults = []
    collection = allCollections[collectionName]
    # Go through all the conditions provided
    for condition in conditions:    
        # If we are finding equal to some value and hash exists on that column, column is on left
        if condition[1] == '=' and collectionName + '_' + condition[0] in hashedKeys and canEval(condition[2]):
            if outputCollection != None:
                print('Using the Hash generated earlier to check for the value')
            compare = eval(condition[2])
            result = hashMatch(collectionName, condition[0], compare)
        # If we are finding equal to some value and hash exists on that column, column is on right
        elif condition[1] == '=' and collectionName + '_' + condition[2] in hashedKeys and canEval(condition[0]):
            if outputCollection != None:
                print('Using the Hash generated earlier to check for the value')
            compare = eval(condition[0])
            result = hashMatch(collectionName, condition[2], compare)
        # If we are finding anything except not equal to some value and Btree exists on that column, column is on left
        elif condition[1] != '!=' and collectionName + '_' + condition[0] in bTreedKeys and canEval(condition[2]):
            if outputCollection != None:
                print('Using the Btree generated earlier to check for the value')
            compare = eval(condition[2])
            result = bTreeMatch(collectionName, condition[0], condition[1], compare)
        # If we are finding anything except not equal to some value and Btree exists on that column, column is on right
        elif condition[1] != '!=' and collectionName + '_' + condition[2] in bTreedKeys and canEval(condition[0]):
            if outputCollection != None:
                print('Using the Btree generated earlier to check for the value')
            compare = eval(condition[0])
            result = bTreeMatch(collectionName, condition[2], condition[1], compare)
        # If Btree and hash dont work, interpret both sides and compare
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
        # Append the result of all conditions into one array
        allResults.append(result)

    allResults = np.asarray(allResults)
    # Take AND of all the results and extract all the rows that are True
    if operator == 'and':
        finalOutcome = np.extract(np.all(allResults, axis = 0), collection)
    # Take OR of all the results and extract all the rows that are True
    else:
        finalOutcome = np.extract(np.any(allResults, axis = 0), collection)
    if outputCollection == None:
        return finalOutcome
    else:
        allCollections[outputCollection] = finalOutcome
        printTable(allCollections[outputCollection])
        outputToFile(outputCollection, 'allOperations', 'a+')


def findAverage(outputCollection, collectionName, column):
    """Find the average of all the values in a column
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take average
    column : str
        The column name we want the average of
    """
    col = allCollections[collectionName][column] 
    mean = np.mean(col)
    allCollections[outputCollection] = np.array([(mean)], dtype=[('mean(' + column + ')', 'float_')])
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findMax(outputCollection, collectionName, column):
    """Find the Maximum of all the values in a column
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take maximum
    column : str
        The column name we want the maximum of
    """
    col = allCollections[collectionName][column] 
    colMax = np.max(col)
    allCollections[outputCollection] = np.array([(colMax)], dtype=[('max(' + column + ')', col.dtype)])
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findSum(outputCollection, collectionName, column):
    """Find the sum of all the values in a column
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take sum
    column : str
        The column name we want the sum of
    """
    col = allCollections[collectionName][column] 
    colSum = np.sum(col)
    allCollections[outputCollection] = np.array([(colSum)], dtype=[('sum(' + column + ')', col.dtype)])
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findSumByGroup(outputCollection, collectionName, column, groupBy):
    """Group using a column and find the sum of all rows in the group
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take sum
    column : str
        The column name we want the sum of
    groupBy : [str]
        The column name we want to group by
    """
    collection = allCollections[collectionName]
    # Find all the values we can group by
    uniqueCombinations = np.unique(collection[groupBy])
    # Go through the whole collection, find all row in a group and take sum
    groupBySums = np.array( [ np.sum(collection[collection[groupBy] == row][column]) for row in uniqueCombinations] )
    # Append the unique values and their sum in one table
    groupedCollection = rfn.append_fields(uniqueCombinations, 'sum(' + column + ')', groupBySums, usemask=False)
    allCollections[outputCollection] = groupedCollection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findCount(outputCollection, collectionName):
    """Find the number of rows in a table
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we need to count
    """
    col = allCollections[collectionName]
    colSum = len(col)
    allCollections[outputCollection] = np.array([(colSum)], dtype=[('count(*)', col.dtype)])
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findCountByGroup(outputCollection, collectionName, groupBy):
    """Group using a column and find the number of rows in the group
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take sum
    groupBy : [str]
        The column name we want to group by
    """
    collection = allCollections[collectionName]
    # Find all the values we can group by
    uniqueCombinations = np.unique(collection[groupBy])
    # Go through the whole collection, find all row in a group and take count
    groupBySums = np.array( [ len(collection[collection[groupBy] == row]) for row in uniqueCombinations] )
    # Append the unique values and their count in one table
    groupedCollection = rfn.append_fields(uniqueCombinations, 'count(*)', groupBySums, usemask=False)
    allCollections[outputCollection] = groupedCollection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findAverageByGroup(outputCollection, collectionName, column, groupBy):
    """Group using a column and find the average of all rows in the group
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take average
    column : str
        The column name we want the average of
    groupBy : [str]
        The column name we want to group by
    """
    collection = allCollections[collectionName]
    # Find all the values we can group by
    uniqueCombinations = np.unique(collection[groupBy])
    # Go through the whole collection, find all row in a group and take average
    groupByAvgs = np.array( [ np.mean(collection[collection[groupBy] == row][column]) for row in uniqueCombinations] )
    # Append the unique values and their average in one table
    groupedCollection = rfn.append_fields(uniqueCombinations, 'avg(' + column + ')', groupByAvgs, usemask=False)
    allCollections[outputCollection] = groupedCollection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findMovingSum(outputCollection, collectionName, column, windowSize):
    """Find the sum of column based on a window size
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take sum
    column : str
        The column name we want the sum of
    windowSize : int
        The number of rows we sum at a moment
    """
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

    movSumTable = np.array(movingSum, dtype=[('movsum(' + column + ')', wholeColumn.dtype)])
    allCollections[outputCollection] = rfn.merge_arrays((allCollections[collectionName], movSumTable), flatten = True, usemask = False)
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def findMovingAverage(outputCollection, collectionName, column, windowSize):
    """Find the average of column based on a window size
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    collectionName : str
        The collection name we use to take average
    column : str
        The column name we want the average of
    windowSize : int
        The number of rows we average at a moment
    """
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

    movAvgTable = np.array(movingAverage, dtype=[('movavg(' + column + ')', 'float_')])
    allCollections[outputCollection] = rfn.merge_arrays((allCollections[collectionName], movAvgTable), flatten = True, usemask = False)
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')


def join(outputCollection, leftCollection, rightCollection, conditions, operator):
    """Left Joins two collections based on specified conditions
    
    Parameters
    ----------
    outputCollection : str
        The collection name we store the final result as
    leftCollection : str
        The collection name we take use for join
    rightCollection : str
        The collection name we join to the first collection based on conditions
    conditions : array(array(str))
        of the form 
        [['leftCollection.columnName', '!=', 'rightCollection.columnName + 60'],
        ['rightCollection.columnName - 60', '>=', 'leftCollection.columnName / 60'']]
    operator : str
        The operator as which we combine the conditions (and/or)
    """
    replaceAll = []
    for condition in conditions:
        replace = []
        # For each condition we find in which position the leftCollection is mentioned (0/2)
        if leftCollection in condition[0].split('.'):
            lhs = condition[0]
            rhs = condition[2]
            posOfLeftCollection = 0
        elif leftCollection in condition[2].split('.'):
            lhs = condition[2]
            rhs = condition[0]
            posOfLeftCollection = 2

        # finding the occurence of leftCollection.columnName
        left = re.findall(leftCollection + '.[a-zA-Z_$0-9]+', lhs)
        # Splitting based on . to get columnName
        splitted_left = left[0].split('.')
        replace = [posOfLeftCollection, left[0], leftCollection + '_' + splitted_left[1]]
        if checkIfIndexed(leftCollection + '_' + splitted_left[1]):
            print('Using previously indexed column from table ' + leftCollection + ' to speed up the join')
        # finding the occurence of rightCollection.columnName
        right = re.findall(rightCollection + '.[a-zA-Z_$0-9]+', rhs)
        splitted_right = right[0].split('.')
        # Replacing rightCollection.columnName with columnName
        condition[2 - posOfLeftCollection] = re.sub(rightCollection + '.[a-zA-Z_$0-9]+', splitted_right[1], rhs)
        if checkIfIndexed(rightCollection + '_' + splitted_right[1]):
            print('Using previously indexed column from table ' + rightCollection + ' to speed up the join')
        # Replace contains an array of format:
        # [positionOfLeftCollection, leftCollection.columnName, leftCollection_columnName]
        replaceAll.append(replace)

    # Renaming the fields of left collection with format leftCollection_columnName
    fieldRename = {} 
    for name in allCollections[leftCollection].dtype.names:
        fieldRename[name] = leftCollection + '_' + name
    leftCollectionRenamed = rfn.rename_fields(allCollections[leftCollection], fieldRename)

    # Storing but not renaming quite yet the fields of left collection with format leftCollection_columnName because we want to use hash and BTree later
    fieldRename = {} 
    for name in allCollections[rightCollection].dtype.names:
        fieldRename[name] = rightCollection + '_' + name

    joinedCollection = []
    firstTime = 1
    # For each row in leftCollection
    for row in leftCollectionRenamed:
        # Creating a copy of conditions so it doesnt reference original
        rowCondition = deepcopy(conditions)
        for i in range(len(rowCondition)):
            pos = replaceAll[i][0]
            # Replacing the leftCollection.columnName with the actual value
            rowCondition[i][pos] = rowCondition[i][pos].replace(replaceAll[i][1], str(row[replaceAll[i][2]]))
        # Finding all the rows that satisfy the condition from the rightCollection
        columnsThatMatch = select(None, rightCollection, rowCondition, operator)
        if len(columnsThatMatch) > 0:
            # Renaming the result
            columnsThatMatch = rfn.rename_fields(columnsThatMatch, fieldRename)
            # Merging the row from leftCollection and all the rows from rightCollection that matched
            joins = rfn.merge_arrays((np.array([row]*len(columnsThatMatch)), columnsThatMatch), flatten = True, usemask = False)
            if firstTime:
                joinedCollection = joins
                firstTime = 0
            else:
                joinedCollection = np.concatenate((joinedCollection, joins), axis = 0)

    allCollections[outputCollection] = joinedCollection
    printTable(allCollections[outputCollection])
    outputToFile(outputCollection, 'allOperations', 'a+')