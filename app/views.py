from flask import redirect, request, render_template, url_for, session, g, jsonify, make_response
from flask_wtf import Form
from wtforms import RadioField
from app import app
import os
import copy
import json
import numpy as np
import os.path as op
import pandas as pd
from matplotlib.cm import jet
from matplotlib.colors import rgb2hex


Rawdatapath= 'rawdata/OnlineNewsPopularity.csv'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def columns():
    newdf = dataReformat(Rawdatapath)

    data = {}
    for col in newdf:
        hist = binGen(newdf[col])[0]
        data[col] = hist
    data['columns'] = list(newdf.columns.values)
    return  json.dumps(data)





def dataReformat(Rawdatapath):
    df = pd.read_csv(Rawdatapath)
    df.columns = [col.strip(" ") for col in df.columns]
    webAddr = df.ix[:, 0].values
    newsTitle = [addr.split('/')[-2] for addr in webAddr]
    target = df.ix[:,-1].values
    newdf = df.ix[:,1:]
    #newdf['newsTitle'] = newsTitle
    return newdf#.ix[1:20,3:7]

def binGen(array, binsNumber=200):
    """
    input an array
    return a list of dicts for drawing barchart
    """
    array_his = np.histogram(array,binsNumber)
    array_his = [list(i) for i in array_his]

    def getDatainBins(ticks):
        """
        ticks: [(lowerbound, upperbound),..]
        return a list of lists which contains data index for
        each bins
        """
        binData = []
        for k, bounds in enumerate(ticks):
            lower, upper= bounds
            if k == len(ticks)-1:
                #last bar, should inclue the last number
                dataIndex = array.ix[(array >= float(lower))& (array <= float(upper))].index.values
            else:
                dataIndex = array.ix[(array >= float(lower)) & (array < float(upper))].index.values
            binData.append(list(dataIndex))
        return binData

    bins = array_his[0]
    ticksOrigin = array_his[1]
    ticksOrigin = zip(ticksOrigin[:-1], ticksOrigin[1:])

    binData = getDatainBins(ticksOrigin)
    ticks = ['%.2f'%i for i in array_his[1]]
    ticks = zip(ticks[:-1], ticks[1:])


    assert type(binsNumber)==int
    jetcolor = genJetColormap(binsNumber)
    feature_his = []
    for k, v in enumerate(zip(bins, ticks)):
        dic = {'bins':v[0], 'ticks':v[1], 'binData':binData[k], 'color':jetcolor[k]}
        feature_his.append(dic)

    return (feature_his, ticksOrigin)

def genJetColormap(n):
    """
    give the length of the list contains only distict attribute value
    return an HX color map range which has the same length
    """
    interval = 256. / n
    indexes = [interval*(i) for i in range(n)]
    indexes[-1] = 255
    return [str(rgb2hex(jet(int(j)))) for j in indexes]
