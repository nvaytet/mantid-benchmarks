class Element():

    def __init__(self, algorithm=None, parent=None, level=0):
        self.algorithm = algorithm
        self.parent = parent
        self.children = []
        self.level = level
        return

    def append_child(self, child=None):
        self.children.append(child)
        return

def recursive_print(element):
    print((' ' * (element.level*4)) + element.algorithm.name() + \
          ": " + str(element.algorithm.executionDuration()) + "s")
    for c in element.children:
        recursive_print(c)

class Tree():

    def __init__(self,history=None):

        self.elements = []
        self.maxlevel = 0
        level = 0;
        for h in history.getChildHistories():
            self.elements.append(Element(algorithm=h, level=0))

        loop=True
        while(loop):
            no_new_elements = True
            level += 1
            elem_list = []
            for e in self.elements:
                elem_list.append(e)
            for e in elem_list:
                try:
                    if len(e.children) == 0:
                        for h in e.algorithm.getChildHistories():
                            self.elements.append(Element(algorithm=h, level=level, parent=e))
                            e.append_child(self.elements[-1])
                            no_new_elements = False
                except AttributeError:
                    pass
            if no_new_elements:
                loop = False
        return

    def view(self):
        for e in self.elements:
            if e.level == 0:
                recursive_print(e)
        return
