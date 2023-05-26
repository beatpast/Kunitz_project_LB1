#!/usr/bin/python
import sys
import math

def get_hmm(filename):
    ''' Input: file containing 3 columns: $1 contains UniprotID, 
    $2 E-vlaue (domain evalue) of the hmmsearch and $3 '0' negatives OR '1' positives.
    It returns the f_list containing the best evalue and the kind of the the sequence (0 or 1) '''
    f_list=[]
    d={}
    with open(filename) as f:
        for line in f:
            v=line.rstrip().split()
            d[v[0]]=d.get(v[0],[])
            d[v[0]].append([ float(v[1]),int(v[2]), v[0] ]) # eval, kind, ID
            # print(d[v[0]])
        for ids in d.keys():
        # we might get many hits for one single uniprot ID but we 
        # only keep the one with the lowest e-value
            d[ids].sort()
            f_list.append(d[ids][0])
        return f_list  # = data

def get_conf_mtrx(data,threashold):
    '''Calculates the confusion matrix from a list of lists (data) containing one list for each seuqence: containing: e-value,  kind: either 1 = positive or 0 = negative and ID. This file is used to calculate the confusion matrix. threashold = the selected threshold to calculate the values that are above and below the threshold [[TP, FP], [FN, TN]]'''
    cm = [[0.0,0.0],[0.0,0.0]] #building zero matrix first
    n = 0
    m = 0
    eval = 0
    kind = 1
    for i in data: # for every list in 'data'
        if i[eval]<th and i[kind]==1: # lower than threshold and true positive, 1
            cm[0][0] += 1
        if i[eval]>=th and i[kind]==1: # false negative
            cm[1][0] += 1
            n +=1
           # if n < 10:
                #print(i[2], 'FN') # to save the ID  of the FN
        if i[eval]<th and i[kind]==0: # true negative
            cm[0][1] += 1
            m += 1
            #if m < 10:
               # print(i[2], 'FP') # to save ID of the FP
        if i[eval]>=th and i[kind] ==0:
            cm[1][1] += 1
    return cm

def accuracy(m): 
    '''Takes the confusion matrix as input and calculates the accuracy
    (TP + TN) / (TP + FP + FN + TN) if denominator is zero the result must be set to 0'''
    if cm[0][0] == 0: return 0
    return float(m[0][0]+m[1][1])/(sum(m[0])+sum(m[1]))

def matthew_cc(m):
    '''Takes the confusion matrix as input and returns the Matthews correlation coefficient'''
    d=(m[0][0]+m[1][0])*(m[0][0]+m[0][1])*(m[1][1]+m[1][0])*(m[1][1]+m[0][1])
    if d == 0: d = 1
    return float((m[0][0]*m[1][1]-m[0][1]*m[1][0])/math.sqrt(d))

def tpr(cm):
    ''' returns the true positive rate'''
    if cm[0][0] == 0: return 0
    return cm[0][0]/(cm[0][0]+cm[1][0])

def fpr(cm):
    ''' returns the false positive rate'''
    if cm[0][1] == 0: return 0
    return cm[0][1]/(cm[0][1]+cm[1][1])

#def tnr(cm):
    #''' returns the true negative rate'''
   # if cm[1][1] == 0: return 0
   # return cm[1][1]/(cm[1][1]+cm[0][1])

#def ppv(cm):
    #'''returns the positive predictive value = tp/ (tp + fp) = n of tp / all positive calls'''
    #if cm[0][0] == 0: return 0
    #return cm[0][0]/(cm[0][0]+cm[0][1])

#def npv(cm):
   # '''returns the negative predictive value = tn/ (tn + fn) = n of tn / all negative calls'''
   # if cm[1][1] == 0: return 0
   # return cm[1][1]/(cm[1][1]+cm[1][0])

if __name__== "__main__":
    filename=sys.argv[1]
    #th=float(sys.argv[2])
    data = get_hmm(filename)
   # provides 200 diff e-vla threasholds
    tpr_list = []
    fpr_list = []
    for i in range(30):
        th = 10 ** -i
        cm = get_conf_mtrx(data, th)
        tpr_value = tpr(cm)
        fpr_value= fpr(cm)
        tpr_list.append(tpr_value)
        fpr_list.append(fpr_value)
        #print('Threshold:',th,'\nACC:', accuracy(cm),'\nMatthews:',matthew_cc(cm), "\nTPR:", tpr(cm), '\nFPR:', fpr(cm), '\nTNR:', tnr(cm), '\nPositivePredVal:', ppv(cm), '\nNegPredVal:', npv(cm), "\nThe Matrix:", cm,)
    print("fpr_list:", fpr_list)
    print("tpr_list:", tpr_list)
