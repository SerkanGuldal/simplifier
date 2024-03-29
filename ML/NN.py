# Author Serkan Güldal 2021.09.19
from itertools import filterfalse
import os

from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from sklearn.neural_network import MLPClassifier
from imblearn.metrics import *

from collections import Counter
from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report, accuracy_score, make_scorer
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import *

from pandas import DataFrame
from pandas import read_csv
from numpy import mean
from matplotlib import pyplot
import numpy

import multiprocessing as mp
import numpy as np
import time
import xlwt
from xlwt import Workbook


debug =False

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')



def data_importer(inputFile): # Data importer function
    file = open(os.path.dirname(__file__) + '/../datasets/' + inputFile)
    df=pd.read_csv(file)
    NumberOfColumns = len(df.columns)
    NumberOfVariables = NumberOfColumns - 1 # The last colum is the label/class
    X = df.values[:,0:NumberOfVariables]
    y = df.values[:,NumberOfVariables]
    return(X, y)


def ml(X, y, r): # Machine learning approach
    
    if debug:
        print("Round ", r)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.40, random_state = 0)
    c = MLPClassifier(random_state=42, solver='sgd', max_iter=1500)
    c.fit(X_train, y_train)
    y_pred = c.predict(X_test)

    # Measurements
    Accuracy = accuracy_score(y_test, y_pred)    
    AreaUnderROCcurve = roc_auc_score(y_test, c.predict_proba(X_test)[:, 1])
    
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred, pos_label=0)
    AreaUndercurve0 = metrics.auc(fpr, tpr)

    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred, pos_label=1)
    AreaUndercurve1 = metrics.auc(fpr, tpr)

    Recall = recall_score(y_test, y_pred, average='macro')
    Precision = precision_score(y_test, y_pred, average='macro')
    f1score = f1_score(y_test, y_pred, average='macro')
    specificity = specificity_score(y_test, y_pred, average='macro')
    sensitivity = sensitivity_score(y_test, y_pred, average='macro')
    geometric = geometric_mean_score(y_test, y_pred, average='macro')

    return(Accuracy, AreaUnderROCcurve, AreaUndercurve0, AreaUndercurve1, Recall, Precision, f1score, specificity, sensitivity, geometric)


def moving_average(x):
    global ave
    ave = []
    for i in range(len(x)):
        m = mean(x[0:i+1])
        ave.append(m)
    return ave

input_file_name = "yeast3_label_class.csv"

if __name__ == '__main__':
    
    print('Number of CPUs available:', mp.cpu_count())
    pool = mp.Pool()

    NoV = 8 # Number of variables needs to be updated!!!!

    # Column names in output (excel file)
    row = 1
    sheet1.write(0, 0, 'Method')
    sheet1.write(0, 1, 'Accuracy')
    sheet1.write(0, 2, 'Area Under ROC curve')
    sheet1.write(0, 3, 'Area Under the Curve 0')
    sheet1.write(0, 4, 'Area Under the Curve 1')
    sheet1.write(0, 5, 'Recall')
    sheet1.write(0, 6, 'Precision')
    sheet1.write(0, 7, 'F1 Score')
    sheet1.write(0, 8, 'Specificity')
    sheet1.write(0, 9, 'Sensitivity')
    sheet1.write(0, 10, 'Geometric Mean')
    sheet1.write(0, 11, 'Arithmetic Mean')
    sheet1.write(0, 12, 'Total time')

    files = [] # List of input files
    for i, file in enumerate(os.listdir("datasets")):
        if file.startswith(input_file_name) and i < NoV:
            files.append(file)

    for file in files:
        print(file)
        X, y = data_importer(file)
        print(X)
        print(y)
            
        ts = time.time()

        a = [pool.apply_async(ml, args = (X, y, r)) for r in range(1,50)]
        
        score = numpy.array([i.get() for i in a])
        acc = score[:,0]
        aucroc = score[:,1]
        auc0 = score[:,2]
        auc1 = score[:,3]
        rc = score[:,4]
        pre = score[:,5]
        f = score[:,6]
        sp = score[:,7]
        sen = score[:,8]
        geo = score[:,9]
        aveALL = mean([ mean(acc), mean(aucroc), mean(auc0), mean(auc1), mean(rc), mean(pre), mean(f), mean(sp), mean(sen)])
        duration = time.time() - ts

        #Writing all results to a file

        sheet1.write(row, 0, file[1:-4])
        sheet1.write(row, 1, mean(acc))
        sheet1.write(row, 2, mean(aucroc))
        sheet1.write(row, 3, mean(auc0))
        sheet1.write(row, 4, mean(auc1))
        sheet1.write(row, 5, mean(rc))
        sheet1.write(row, 6, mean(pre))
        sheet1.write(row, 7, mean(f))
        sheet1.write(row, 8, mean(sp))
        sheet1.write(row, 9, mean(sen))
        sheet1.write(row, 10, mean(geo))
        sheet1.write(row, 11, mean(aveALL))
        sheet1.write(row, 12, mean(duration))
        wb.save(os.path.dirname(__file__) + '/../datasets/' + input_file_name + '_NN.xls')
        
        row += 1

        if debug:
            print(file + ' is completed. Here is the summary.')
            print("Accuracy:",mean(acc))
            print("Area Under ROC curve:", mean(aucroc))
            print("Area Under the Curve 0:", mean(auc0))
            print("Area Under the Curve 1:", mean(auc1))
            print("Recall:", mean(rc))
            print("Precision:", mean(pre))
            print("F1 Score:", mean(f))
            print("Specificity:", mean(sp))
            print("Sensitivity:", mean(sen))
            print("Geometric Mean:", mean(geo))
            print("Arithmetic Mean:", mean(aveALL))        
            print('Time in parallel:', duration)

            ###### Writinng to files ########

            # with open('RF_' + dataname + '_' + 'scores.csv', 'w') as filehandle:
            #     for listitem in score:
            #         filehandle.write('%s\n' % listitem)

            prename = os.path.dirname(__file__) + '/../datasets/' + file + '/debug/NN`_' + data_type + '_'

            with open(prename + 'Accuracy.csv', 'w') as filehandle:
                for listitem in acc:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'AUCROC.csv', 'w') as filehandle:
                for listitem in aucroc:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'AUC_0.csv', 'w') as filehandle:
                for listitem in auc0:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'AUC_1.csv', 'w') as filehandle:
                for listitem in auc1:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'Recall.csv', 'w') as filehandle:
                for listitem in rc:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'Precision.csv', 'w') as filehandle:
                for listitem in pre:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'F1_Score.csv', 'w') as filehandle:
                for listitem in f:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'Specificity.csv', 'w') as filehandle:
                for listitem in sp:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'Sensitivity.csv', 'w') as filehandle:
                for listitem in sen:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'Geometric.csv', 'w') as filehandle:
                for listitem in geo:
                    filehandle.write('%s\n' % listitem)

            with open(prename + 'summary.txt', 'w') as filehandle:
                filehandle.write('              Accuracy: %s' % mean(acc))
                filehandle.write('\n  Area Under ROC curve: %s' % mean(aucroc))
                filehandle.write('\nArea Under the Curve 0: %s' % mean(auc0))
                filehandle.write('\nArea Under the Curve 1: %s' % mean(auc1))
                filehandle.write('\n                Recall: %s' % mean(rc))
                filehandle.write('\n             Precision: %s' % mean(pre))
                filehandle.write('\n              F1 Score: %s' % mean(f))
                filehandle.write('\n           Specificity: %s' % mean(sp))
                filehandle.write('\n           Sensitivity: %s' % mean(sen))
                filehandle.write('\n        Geometric Mean: %s' % mean(geo))
                filehandle.write('\n       Arithmetic Mean: %s' % aveALL)
                filehandle.write('\n            Total time: %s' % duration)

            with open(prename + 'Time.csv', 'w') as filehandle:
                filehandle.write('Total time is %s' % duration)

            moving_average(acc)
            with open(prename + 'Accuracy_Convergence.csv', 'w') as filehandle:
                for listitem in ave:
                    filehandle.write('%s\n' % listitem)

            time.sleep(5)

            # pyplot.plot(acc)
            # pyplot.plot(ave)
            # pyplot.show()

    # pyplot.plot(acc)
    # pyplot.plot([mean(acc) for x in range(len(acc))])
    # pyplot.show()