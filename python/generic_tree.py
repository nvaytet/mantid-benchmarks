from graphviz import Graph
import copy


class Node():
    def __init__(self, info=[]):
        self.parent = None
        self.level = 0
        self.children = []
        self.info = info
    
    def to_dot(self, nameFunc=lambda x: str(x[0]), displayFunc=lambda x: str(x[1]), cond=lambda x: False):
        tree = Graph(comment='History tree')
        if cond(self.info):
            tree.node(nameFunc(self.info), displayFunc(self.info), style='filled',fillcolor='red')
        else:
            tree.node(nameFunc(self.info), displayFunc(self.info))
        def to_dot_int(tree, mytree, parentName, nameFunc, displayFunc, cond):
            for tr in mytree.children:
                if tr.info[0] != parentName:
                    if cond(tr.info):
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

    def append(self, tree):
        tree.parent = self
        tree.level = self.level + 1
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

    def clone(self):
        def clone_int(nd_new, nd_old):
            for ch in nd_old.children:
                nd_new.append(Node(copy.deepcopy(ch.info)))
            for i in range(len(nd_old.children)):
                clone_int(nd_new.children[i], nd_old.children[i])

        root = Node(copy.deepcopy(self.info))
        clone_int(root, self)
        return root

    def apply(self, func):
        def apply_int(nd, func):
            nd.info = func(nd.info)
            for ch in nd.children:
                apply_int(ch, func)
        root = self.clone()
        apply_int(root, func)
        return root

    def apply_pairwise(self, other, check, func):
        root = self.clone()
        lst1 = root.to_list()
        lst2 = other.to_list()
        for i in range(len(lst1)):
            if not check(lst1[i].info, lst2[i].info):
                raise RuntimeError("Check failed for pairwise tree operation.")
            lst1[i].info = func(lst1[i].info, lst2[i].info)
        return root

    def apply_from_head_childs(self, func):
        def apply_from_head_childs_int(nd, func):
            nd.info = func(nd.info, [ch.info for ch in nd.children])
            for ch in nd.children:
                apply_from_head_childs_int(ch, func)

        root = self.clone()
        apply_from_head_childs_int(root, func)
        return root


def apply_multiple_trees(trees, check, func):
    root = trees[0].clone()
    lst = root.to_list()
    lists = [x.to_list() for x in trees]
    for i in range(len(lst)):
        if not check([x[i].info for x in lists]):
            raise RuntimeError("Check failed for bulk trees operation.")
        lst[i].info = func([x[i].info for x in lists])
    return root
