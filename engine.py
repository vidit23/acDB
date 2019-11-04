def printData(collection):
    headers = collection.dtype.names
    table = tabulate(collection, headers, tablefmt="grid")
    print(table)

def readFromFile(collectionName, readFromFile):
    readDB = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names=True, autostrip=True)
    allCollections[collectionName] = readDB

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