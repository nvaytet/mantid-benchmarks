from graphviz import Graph
import numpy as np
import copy

def recWidthDctInt(algHistory, dct, parentName, countList):
    for h in algHistory:
        countList.append(1);
        name = str(h.name()) + str(len(countList))
        dur = h.executionDuration()
        dct[parentName][1].update({name : [dur, {}]})
        recWidthDctInt(h.getChildHistories(),dct[parentName][1], name, countList)
        
def recWidthDct(algHistory):
    dct = {"root" : [0.0, {}]}
    countList = []
    recWidthDctInt(algHistory, dct, "root", countList)
    return dct;

def extractChilds(dctTreeOrig):
    dctTree = copy.deepcopy(dctTreeOrig)
    for key, val in dctTree.items():
        for chKey, chVal in val[1].items():
            val[0] -= chVal[0]
        extractChilds(val[1])
    return dctTree

def toDotInt(tree, dctTree, parentName):
    for key, val in dctTree.items():
        if key != parentName:
            tree.node(key, key + '\n' + str(val[0]))
            tree.edge(key, parentName)
        toDotInt(tree, val[1], key)
    
def toDot(dctTree):
    tree = Graph(comment='History tree')
    tree.node("root", "root")
    toDotInt(tree, dctTree, "root")
    return tree

def extractElement(dctTreeOrig, name, num):
    dctTree = copy.deepcopy(dctTreeOrig)
    for key, val in dctTree.items():
        if name == key:
            val[0] -= num
            return
        extractElement(val[1], name, num)
    return dctTree
        
def listWidthOrderInt(dctTree, res): # unwind tree to list in the width first order [(key, node)]
    for key, val in dctTree.items():
        res.append([key, val])
        listWidthOrderInt(val[1], res)
        
def listWidthOrder(dctTree):
    res = []
    listWidthOrderInt(dctTree, res)
    return res

def extractElemenwise(dctTreeOrig, dctTree2): # more or less effective realisation
    dctTree1 = copy.deepcopy(dctTreeOrig)
    lst1 = listWidthOrder(dctTree1)
    lst2 = listWidthOrder(dctTree2)
    for i in range(len(lst1)):
        lst1[i][1][0] -= lst2[i][1][0]
    return dctTree1

def applyElementwise(dctTreeOrig, dctTree2, func):
    dctTree1 = copy.deepcopy(dctTreeOrig)
    lst1 = listWidthOrder(dctTree1)
    lst2 = listWidthOrder(dctTree2)
    for i in range(len(lst1)):
        lst1[i][1][0] = func(lst1[i][1][0], lst2[i][1][0])
    return dctTree1

def applyScalar(dctTreeOrig, scalar, func):
    dctTree = copy.deepcopy(dctTreeOrig)
    lst = listWidthOrder(dctTree)
    for i in range(len(lst)):
        lst[i][1][0] = func(lst[i][1][0], scalar)
    return dctTree

def applyFunc(dctTreeOrig, func):
    dctTree = copy.deepcopy(dctTreeOrig)
    lst = listWidthOrder(dctTree)
    for i in range(len(lst)):
        lst[i][1][0] = func(lst[i][1][0])
    return dctTree

def fitModel(dctDctTree, func): #dictionary with key as numbet of threads and val as tree
    first = False
    res = {}
    xVals = []
    for key, val in dctDctTree.items():
        xVals.append(key)
        if not first:
            res = applyFunc(val, lambda x: [x])
            first = True
        else:
            res = applyElementwise(res, val, lambda x, y: x + [y])
    res = applyFunc(res, lambda y: func(np.array(xVals), np.array(y)))
    return res