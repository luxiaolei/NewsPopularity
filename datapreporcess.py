"""
*-Run this script to preporcess the raw data
*-Raw data will split in two parts, data and target
*-Provides an dataloader utility function, which cut data&target into default 70%/30% for training
* and testing usage
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dataReformat(Rawdatapath):
    df = pd.read_csv(Rawdatapath)
    df.columns = [col.strip(" ") for col in df.columns]
    webAddr = df.ix[:, 0].values
    newsTitle = [addr.split('/')[-2] for addr in webAddr]
    target = df.ix[:,-1].values
    newdf = df.ix[:,1:]
    newdf['newsTitle'] = newsTitle
    return newdf

def sparsityCheck(newdf, sparseValue=0, threlhodDensity_for_print= 0.5):
    """
    print dataframe's density with given defined sparseValue
    print the columns whose density is samller than the threlhodDensity_for_print
    """
    df = newdf.ix[:, newdf.columns.difference(['newsTitle'])]
    dfsparse = df.to_sparse(fill_value= sparseValue)
    print("If treate {0} as sparse value, then the dataFrame's density is {1}")\
            .format(sparseValue, dfsparse.density)
    sparseInfo= []
    for col in df.columns:
        dfsparse = df[col].to_sparse(fill_value= sparseValue)
        if dfsparse.density <= threlhodDensity_for_print:
            sparseInfo.append([col,dfsparse.density])
    ansDf = pd.DataFrame(sparseInfo, columns=['columnName', 'SparseDensity'])
    print ansDf


def outliersCheck(newdf, n_times_std =3, outlierPercentagePrintThrelhod=0.01):
    """
    For each columns, print the data percentage for which lies below
    n_times_std times of the std, or larger.
    """
    df = newdf.ix[:, newdf.columns.difference(['newsTitle'])]
    count = df.shape[0]
    outlier_cout_list = []
    for col in df.columns:
        mean, std = df[col].mean(), df[col].std()
        outliers = df[col][np.abs(df[col] - mean) >= n_times_std* std]
        outliers_count = outliers.shape[0]

        percentage = float(outliers_count)/ count
        if percentage >= outlierPercentagePrintThrelhod:
            outlier_cout_list.append([col, outliers_count, percentage])
    outlierSummary = pd.DataFrame(outlier_cout_list,\
                    columns=['ColumnName','OutlierCount', 'CountPercentage'])
    print outlierSummary


def collinearityCheck(newdf, variationThrehod= 0.1):
    """
    PCA method, use the eigen values of the correlation matrix to check the collinearity
    If the eigenvalue is close to zero, it means, no variation, or collinear to Other columns
    Print the corresponding columns if the eigenvalue is smaller than variationThrehod value
    """
    df = newdf.ix[:, newdf.columns.difference(['newsTitle'])]
    corrMatrix = np.corrcoef(df.values, rowvar=0)
    eigenvalues, eigenvectos = np.linalg.eig(corrMatrix)
    ans = []
    for col, eigV in zip(df.columns, eigenvalues):
        if eigV <= variationThrehod:
            ans.append([col,eigV])
    ansDf = pd.DataFrame(ans, columns=['columnName', 'Eigenvalue'])
    print ansDf




if __name__=='__main__':
    datapath = 'rawdata/OnlineNewsPopularity.csv'

    #trim sapces in columnNames, and parse website address
    newdf = dataReformat(datapath)

    print "**Sparseness Check!**"*3
    sparsityCheck(newdf, sparseValue=0, threlhodDensity_for_print= 0.5)

    print "**Outliers Check!**"*3
    outliersCheck(newdf, n_times_std =3, outlierPercentagePrintThrelhod=0.01)

    print "**collinearity Check!**"*3
    collinearityCheck(newdf, variationThrehod= 0.1)
