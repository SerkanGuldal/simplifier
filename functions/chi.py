from data_importer import data
from sklearn.feature_selection import chi2

d = data('yeast3_label_class.csv', 8)
df = d[0]  # All dataset
X  = d[1]  # features
y  = d[2]  # labels

chi = chi2(X,y)

print(chi)