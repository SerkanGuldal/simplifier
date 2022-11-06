from optparse import Values
import pandas as pd
from pandas import read_csv
import os
import numpy as np
from sklearn.feature_selection import chi2

def data_importer(inputFile, NumberOfVariables):
    """ This takes input as csv file and number of variables as integers."""
    file = open(os.path.dirname(__file__) + '/datasets/' + inputFile)

    global df
    df=pd.read_csv(file)
    header = df.columns
    global X
    X = df.values[:,0:NumberOfVariables]
    global y
    y = df.values[:,NumberOfVariables]
    return(df, header, X, y)

input_file_name = "yeast3_label_class.csv"
df, header, X, y =  data_importer(input_file_name, 8)



# Chi2 values
chi2_values, p_values = chi2(X, y)
np.savetxt('datasets/' + input_file_name + '_chi2_values.csv', chi2_values, delimiter=',')
np.savetxt('datasets/' + input_file_name + '_p_values.csv', p_values, delimiter=',')

# Removing feature starting from lowest score until 1 feature is left
for i in range(len(chi2_values)):
    max_value_position = chi2_values.argmin(axis=0)

    # The lowest scored column is labeled infinity to be skipped.
    chi2_values[max_value_position] = np.inf
  
    if not(np.all((chi2_values == np.inf))): # At least one column is available

        selected_features = np.isfinite(chi2_values)

        output_features = np.append(selected_features,True)
        number_of_features = np.count_nonzero(selected_features) 
        output = df[header[output_features]]
        output.to_csv('datasets/' + input_file_name + '_'+ str(number_of_features) +'.csv', index = False)