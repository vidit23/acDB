import numpy as np 

dbsStored = {}

def readFromFile(dbName, readFromFile):
    readDB = np.genfromtxt(readFromFile, dtype = None, delimiter = ',', names=True, autostrip=True)
    dbsStored[dbName] = readDB
    

query = input('Enter your query: ')
print('Running query: ', query)
readFromFile("R1", "myfile.csv")
