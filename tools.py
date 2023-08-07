
import os
import pandas as pd


def data(inputFile): # Data importer function
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
    df=pd.read_csv(file)
    NumberOfColumns = len(df.columns)
    NumberOfVariables = NumberOfColumns - 1 # The last colum is the label/class
    X = df.values[:,0:NumberOfVariables]
    y = df.values[:,NumberOfVariables]
    return(X, y)