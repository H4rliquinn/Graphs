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
        if not family_tree.get(family[0],None):
            family_tree[family[0]]={}
    #Create Queue
    q=Queue()
    #Create Results set
    family=[]
    #Add starting_node to Queue
    q.enqueue((starting_node,0))
    family.append([starting_node])
    #While Queue not empty
    while q.size()>0:
        child=q.dequeue()
        #Find parents
        for parent in family_tree[child[0]]:
            new_gen=child[1]+1
            q.enqueue((parent,new_gen))
            if len(family)==new_gen+1:
                family[new_gen].append(parent)
            else:
                family.append([parent])
    #Return oldest ancestor
    methuselah=min(family[-1])
    if methuselah==starting_node:
        return -1
    else:
        return min(family[-1])

