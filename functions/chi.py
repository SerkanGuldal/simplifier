from data_importer import data
from sklearn.feature_selection import chi2

# EXAMPLE
# file_name = 'yeast3_label_class.csv' # Filename needs to be updated!!!!
# NoV = 8 # Number of variables needs to be updated!!!!
# data(file_name, NoV)


d = data('yeast3_label_class.csv', 8)
df = d[0]  # All dataset
X  = d[1]  # features
y  = d[2]  # labels

chi = chi2(X,y)

print(chi)