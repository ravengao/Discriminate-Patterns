from flask import Flask, render_template, request, Response, send_file
from pymongo import MongoClient
import json
from bson import json_util
import logging
from bson.json_util import dumps
import io
import numpy as np
import pandas as pd
from orangecontrib.associate.fpgrowth import *  
import Orange


app = Flask(__name__)
df = pd.read_csv('static/input/lilly_beta.csv',header=None,low_memory=False)
rowNum = 2615
colNum = 1024
activeNum = 663
A = df.loc[1:,1:].astype(int).as_matrix()
    
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/parallelCoord",methods=['GET','POST'])
def parallelCoord():
    return render_template("parallel_coord.html")

@app.route("/network",methods=['GET','POST'])
def network():
    return render_template("network.html")

@app.route("/network/createSubset",methods=['GET','POST'])
def create_subset():
    selected_pattern = request.form['pattern']
    support = int(request.form['supp'])
    confidence = float(request.form['conf'])
    itemsets = dict(frequent_itemsets(A, .5))
    target = list(map(int, selected_pattern.split(',')))
    
    com_list = []
    new_active_num = 0
    new_pattern_freq = {}
    for row in range(rowNum):
        a_counter = 0
        appear = 1
        for n in target:
            appear = appear & A[row][n]
        if appear:
            com_list.append(A[row])
            if row <= activeNum:
                new_active_num += 1
    df1 = pd.DataFrame(com_list)
    for n in range(colNum):
        new_freq = sum(df1[n])
        if (new_freq/support >= confidence) & (n not in target):
            active_num = sum(df1.loc[:new_active_num,n])/activeNum
            inactive_num = sum(df1.loc[new_active_num:,n])/(rowNum - activeNum)
            new_pattern_freq[frozenset([n]+target)] = [new_freq,[active_num,inactive_num]]
    if len(new_pattern_freq) > 0:
        df2 = pd.DataFrame(new_pattern_freq).T
        df2.columns = ['size','aiScore']
        df2['name'] = df2.index
        jsbuffer = df2.to_json(orient='records')
        return jsbuffer
    else:
        return ""


@app.route("/network/createUnion",methods=['GET','POST'])
def create_union():
    overallPatterns = request.form['overall']
    selected = set(map(int, request.form['pattern'].split(',')))
    overall = overallPatterns.replace('[[','').replace(']]','').split("],[")
    unionList = []

    com_list = []
    new_active_num = 0
    new_pattern_freq = {}
    for row in range(rowNum):
        a_counter = 0
        appear = 1
        for n in selected:
            appear = appear & A[row][n]
        if appear:
            com_list.append(A[row])
            if row <= activeNum:
                new_active_num += 1
    df1 = pd.DataFrame(com_list)    
                
    for element in overall:
        eleSet = set(map(int,element.split(',')))
        difference = eleSet - selected
        active_freq = 0
        inactive_freq = 0
        for row in range(len(df1)):
            if row < new_active_num:
                appear = 1
                for col in difference:
                    appear = appear & df1.loc[row,col]
                if appear == 1:
                    active_freq += 1
            else:
                appear = 1
                for col in difference:
                    appear = appear & df1.loc[row,col]
                if appear == 1:
                    inactive_freq += 1

        total_freq = active_freq + inactive_freq
        #if (total_freq/support >= confidence):
        if (eleSet|selected) != selected:
            new_pattern_freq[frozenset(eleSet|selected)] = [total_freq,[(active_freq/activeNum), (inactive_freq/(rowNum - activeNum))]]

    if len(new_pattern_freq) > 0:
        df2 = pd.DataFrame(new_pattern_freq).T
        df2.columns = ['size','aiScore']
        df2['name'] = df2.index   
        jsbuffer = df2.to_json(orient='records')
        return jsbuffer
    else:
        return ""
    

@app.route("/calculation/aiRatio",methods=['GET','POST'])
def calculation_aiRatio():
    cp1 = int(request.form['cp1'])
    cp2 = int(request.form['cp2'])
    #app.logger.info(cp1,cp2)
    
    A_prefilter = df[(df[cp1+1]=='1') & (df[cp2+1]=='1')]
    ai_ratio = aiRatio(A_prefilter)
    
    output_arr = []
    for row in range(colNum):
        for col in range(colNum):
            if ai_ratio.loc[row][col] != 0:
                output_arr.append([row,col,ai_ratio.loc[row][col]])
    output = pd.DataFrame(output_arr)
    jsbuffer = output.to_json(orient='records')
    return jsbuffer


def aiRatio(matrix_pre):
    matrix = matrix_pre.loc[:,1:].astype(int).as_matrix()
    
    W = np.dot(matrix, matrix.T) #row relationship(compound)
    U = np.dot(matrix.T, matrix) #col relationship(structure)

    active_matrix = matrix_pre.loc[1:activeNum,1:].astype(int).as_matrix()
    active_matrix

    activeC = np.dot(active_matrix, active_matrix.T) #row relationship(compound)
    activeS = np.dot(active_matrix.T, active_matrix) #col relationship(structure)

    inactive_matrix = matrix_pre.loc[activeNum+1:,1:].astype(int).as_matrix()

    inactiveC = np.dot(inactive_matrix, inactive_matrix.T) #row relationship(compound)
    inactiveS = np.dot(inactive_matrix.T, inactive_matrix) #col relationship(structure)

    activePercentage = activeS/activeNum
    inactivePercentage = inactiveS/(rowNum-activeNum)

    with np.errstate(divide='ignore', invalid='ignore'):
        activeRatio = np.true_divide(activePercentage,inactivePercentage)
        activeRatio[~np.isfinite(activeRatio)] = 0
        activeRatio[np.isnan(activeRatio)] = 0
    df1 = pd.DataFrame(activeRatio)

    return df1

def serve_csv(dataframe):
    buffer = io.StringIO()
    dataframe.to_csv(buffer,encoding='utf-8')
    buffer.seek(0)
    return send_file(buffer,
                 attachment_filename="test.csv",
                 mimetype='text/csv')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
