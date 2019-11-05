import numpy as np
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning)

allCollections = {}

def readFromFile(outputCollection, readFromFile):
    readDB = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names = True, autostrip = True)
    allCollections[outputCollection] = readDB

def printTable(collectionName):
    headers = collectionName.dtype.names
    table = tabulate(collectionName, headers, tablefmt = "grid")
    print(table)

def project(outputCollection, collectionName, fields):
    allCollections[outputCollection] = allCollections[collectionName][fields]
    printTable(allCollections[outputCollection])

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