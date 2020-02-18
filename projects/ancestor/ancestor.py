class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def earliest_ancestor(ancestors, starting_node):

    #Generate Graph
    family_tree={}
    for family in ancestors:
        if family_tree.get(family[1],None):
            family_tree[family[1]].add(family[0])
        else:
            family_tree[family[1]]={family[0]}
    # print(family_tree)
    q=Queue()
    #Create Queue
    #Add starting_node to Queue
    #While Queue not empty
    #Find parents
    #Return oldest ancestor
test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 1)
