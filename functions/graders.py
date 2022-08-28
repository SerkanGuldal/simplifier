import data_parser as dp
from sklearn.feature_selection import chi2

# EXAMPLE
# file_name = 'yeast3_label_class.csv' # Filename needs to be updated!!!!
# NoV = 8 # Number of variables needs to be updated!!!!
# data(file_name, NoV)

class chi_values:

    def __init__(self, inputFile, NumberOfVariables):
        self.inputFile = inputFile
        self.NumberOfVariables = NumberOfVariables

    file =  dp.data_parser(inputFile, NumberOfVariables)
    file = file.data_importer()

    # file = dp('yeast3_label_class.csv', 8)
    # df = d[0]  # All dataset
    # X  = d[1]  # features
    # y  = d[2]  # labels

    # chi = chi2(X,y)

    print(file)