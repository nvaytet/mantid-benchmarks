import re
from generic_tree import *
from dictionary_tree import *

def parseLine(line):
    res = re.split(">>|:|<>", line)
    return {"thread_id" : res[0], "name" : res[1], "start" : int(res[2]), "finish" : int(res[3])}

def fromFile(fileName):
    res = []
    header = ""
    with open(fileName) as inp:
        for line in inp:
            if "START_POINT:" in line:
                header = line.strip("\n")
                continue
            res.append(parseLine(line))
    return header, res

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def toTrees(records):
    recs = sorted(records, key = cmp_to_key(lambda x, y: x["start"] - y["start"] if x["start"] != y["start"] else y["finish"] - x["finish"]))
    def rec_to_node(r, counter):
        return Node([r["name"] + " " + str(counter), r["start"], r["finish"], counter ])

    heads = []
    counter = 0
    for rec in recs:
        head = None
        for hd in heads:
            if rec["start"] >= hd.info[1] and rec["finish"] <= hd.info[2]:
                head = hd
                break

        if head is None:
            heads.append(rec_to_node(rec, counter))
        else:
            parent = head.find_in_depth(cond=lambda x: x[1] <= rec["start"] and rec["finish"] <= x[2])
            parent.append(rec_to_node(rec, counter))
        counter += 1
    return heads


def to_dct_tree(node):
    def to_dct_tree_int(node, dct, parentName):
        for nd in node.children:
            name = nd.info[0]
            dur = nd.info[2] - nd.info[1]
            dct[parentName][1].update({name : [dur, {}]})
            to_dct_tree_int(nd, dct[parentName][1], name)
    dctT = {node.info[0] : [node.info[2] - node.info[1], {}]}
    to_dct_tree_int(node, dctT, node.info[0])
    return dctT

def loadFile(fileName):
    header, records = fromFile(fileName)
    trees = toTrees(records)
    return header, to_dct_tree(trees[0])
