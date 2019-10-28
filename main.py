import numpy as np 
import warnings
warnings.filterwarnings("ignore", category = np.VisibleDeprecationWarning) 

allDB = {}

def readFromFile(dbName, readFromFile):
    readDB = np.genfromtxt(readFromFile, dtype = None, delimiter = '|', names=True, autostrip=True)
    allDB[dbName] = readDB

def findAverage(dbName, column):
    col = allDB[dbName][column] 
    mean = np.mean(col)
    print(mean)
    print("The Mean for the column " + column + " is " + str(mean))
    


query = input('Enter your query: ')
print('Running query: ', query)
readFromFile("R1", "myfile.csv")
findAverage("R1", "age")
