import functions.data_parser as dp

class simplifier():
    def __init__(self, inputFile, NumberOfVariables):
        self.inputFile = inputFile
        self.NumberOfVariables = NumberOfVariables


    file =  dp.data_parser("yeast3_label_class.csv", 8)
    print(file.data_importer())