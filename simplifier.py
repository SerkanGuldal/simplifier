from json.encoder import INFINITY
from optparse import Values
import pandas as pd
from pandas import read_csv
import os
import numpy as np
from sklearn.feature_selection import chi2

def data_importer(inputFile, NumberOfVariables):
    file = open(os.path.dirname(__file__) + '/datasets/' + inputFile)
    global df
    df=pd.read_csv(file)
    global X
    X = df.values[:,0:NumberOfVariables]
    global y
    y = df.values[:,NumberOfVariables]
    return(df, X, y)


df, X, y =  data_importer("yeast3_label_class.csv", 8)

print(X)
print('\n', 'Chi values')
chi2_values, p_values = chi2(X, y)
print(chi2_values,'\n')

for i in range(len(chi2_values)):
    min_value_position = chi2_values.argmin(axis=0)
    print(min_value_position)
    chi2_values[min_value_position] = INFINITY
    print(chi2_values)
    selected_features = np.isfinite(chi2_values)

    print(selected_features)
    print(X[:,selected_features])

