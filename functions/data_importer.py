
import pandas as pd
from pandas import read_csv
import os


 ### Data importer function

def data(inputFile, NumberOfVariables):
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
   
    df=pd.read_csv(file)
    global X
    X = df.values[:,0:NumberOfVariables]
    global y
    y = df.values[:,NumberOfVariables]
    return(X, y)

rawFile = 'yeast3_label_class.csv' # Filename needs to be updated!!!!
NoV = 8 # Number of variables needs to be updated!!!!

d = data(rawFile, NoV)

print(d)
