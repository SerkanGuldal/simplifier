
import pandas as pd
from pandas import read_csv
import os


class data_parser:

    def __init__(self, inputFile, NumberOfVariables):
        self.inputFile = inputFile
        self.NumberOfVariables = NumberOfVariables
    
    def data_importer(self):
        file = open(os.path.dirname(__file__) + '/../datasets/' + self.inputFile)
        global df
        df=pd.read_csv(file)
        global X
        X = df.values[:,0:self.NumberOfVariables]
        global y
        y = df.values[:,self.NumberOfVariables]
        return(df, X, y)

if __name__ == "__main__":
    file = data_parser("yeast3_label_class.csv", 8)
    print(file.data_importer())