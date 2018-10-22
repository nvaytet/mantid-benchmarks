class Element():

    def __init__(self, algorithm=None, parent=None, level=0):
        self.algorithm = algorithm
        self.parent = parent
        self.children = []
        self.level = level
        self.raw_duration = 0.0
        return

    def append_child(self, child=None):
        self.children.append(child)
        return

def recursive_print(element, file=None):
    string = (' ' * (element.level*4)) + element.algorithm.name() + \
          " " + str(element.level) + " " + str(element.algorithm.executionDuration()) + \
          " " + str(element.raw_duration) +"\n"
    if file:
        file.write(string)
    else:
        print(string)
    for c in element.children:
        recursive_print(c, file)

class Tree():

    def __init__(self,history=None):

        self.elements = []
        self.maxlevel = 0
        self.history = history
        self.raw_sum = 0.0
        level = 1;
        for h in self.history.getChildHistories():
            self.elements.append(Element(algorithm=h, level=level))

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

        # Compute raw durations
        for e in self.elements:
            duration_in_children = 0.0
            for c in e.children:
                duration_in_children += c.algorithm.executionDuration()
            e.raw_duration = e.algorithm.executionDuration() - duration_in_children
            self.raw_sum += e.raw_duration

        return

    def view(self,fname=None):

        header = self.history.name() + " 0 " + \
                 str(self.history.executionDuration()) + " " + \
                 str(self.history.executionDuration() - self.raw_sum)
        if fname:
            f = open(fname,'w')
            f.write(header+'\n')
        else:
            f = None
            print(header)

        for e in self.elements:
            if e.level == 1:
                recursive_print(e, f)
        return
