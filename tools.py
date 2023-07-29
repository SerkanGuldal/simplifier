<<<<<<< HEAD
def data(inputFile): # Data importer function
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
    df=pd.read_csv(file)
    NumberOfColumns = len(df.columns)
    NumberOfVariables = NumberOfColumns - 1 # The last colum is the label/class
    X = df.values[:,0:NumberOfVariables]
    y = df.values[:,NumberOfVariables]
=======
def data(inputFile): # Data importer function
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
    df=pd.read_csv(file)
    NumberOfColumns = len(df.columns)
    NumberOfVariables = NumberOfColumns - 1 # The last colum is the label/class
    X = df.values[:,0:NumberOfVariables]
    y = df.values[:,NumberOfVariables]
>>>>>>> a31df81993c68bae07102ab3cac8ef9d3f463a29
    return(X, y)