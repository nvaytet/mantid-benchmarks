from graphviz import Graph

class Node():
    def __init__(self, info=[]):
        self.parent = None
        self.children = []
        self.info = info
    
    def to_dot(self, nameFunc=lambda x: str(x[0]), displayFunc=lambda x: str(x[1]), cond=lambda x: False):
        tree = Graph(comment='History tree')
        if cond(self.info[1]):
            tree.node(nameFunc(self.info), displayFunc(self.info), style='filled',fillcolor='red')
        else:
            tree.node(nameFunc(self.info), displayFunc(self.info))
        def to_dot_int(tree, mytree, parentName, nameFunc, displayFunc, cond):
            for tr in mytree.children:
                if tr.info[0] != parentName:
                    if cond(tr.info[1]):
                        tree.node(nameFunc(tr.info), displayFunc(tr.info), style='filled',fillcolor='red')
                    else:
                        tree.node(nameFunc(tr.info), displayFunc(tr.info))
                    tree.edge(tr.info[0], parentName)
                to_dot_int(tree, tr, nameFunc(tr.info), nameFunc, displayFunc, cond)
        
        to_dot_int(tree, self, nameFunc(self.info), nameFunc, displayFunc, cond)
        return tree
        
    def to_list(self):
        res = []
        def to_list_int(node, lst):
            lst.append(node)
            for nd in node.children:
                to_list_int(nd, lst)
        to_list_int(self, res)
        return res
    # TODO apply different functions
    def append(self, tree):
        tree.parent = self
        self.children.append(tree)
    
    def find_all(self, cond):
        def find_all_int(node, cond, res):
            if cond(node.info):
                res.append(node)
            for nd in node.children:
                find_all_int(nd, cond, res)
        result = []
        find_all_int(self, cond, result)
        return result
    
    def find_in_depth(self, cond):
        def find_in_depth_int(node, cond, res):
            if cond(node.info):
                res[0] = node
                for nd in node.children:
                    find_in_depth_int(nd, cond, res)
        result = [None]
        find_in_depth_int(self, cond, result)
        return result[0]
    
    def find_first(self, cond):
        def find_first_int(node, cond, res):
            if res:
                return
            else:
                if cond(node.info):
                    res.append(node)
                    return
                for nd in node.children:
                    find_first_int(nd, cond, res)
        result = []
        find_first_int(self, cond, result)
        return result[0]
