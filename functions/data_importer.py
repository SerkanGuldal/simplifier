
import pandas as pd
from pandas import read_csv
import os


 ### Data importer function

def data(inputFile, NumberOfVariables):
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
    global df
    df=pd.read_csv(file)
    global X
    X = df.values[:,0:NumberOfVariables]
    global y
    y = df.values[:,NumberOfVariables]
    return(df, X, y)



