from search import *
from operator import itemgetter
from itertools import islice

class State:

    def __init__(self, i, w) :
        self.weight = w
        self.items = i

    def add(self, no):
        #global capa
        #global items
        if not item in self.items and capa >= self.weight + items[no][0]:
            self.items[no] = items[no]
            self.weight += items[no][0]
            return True

        return False

    def remove(self, no):
        if no in self.items:
            self.weight -= self.items[no][0]
            del self.items[no]
            return True

        return False

    def replace(self, old, new):
        #global capa
        #global items
        
        if not old in self.items or new in self.items or old == new:
            return False
        
        if self.weight - items[old][0] + items[new][0] <= capa:
            self.remove(old) 
            self.add(new)
        
        return True

class Knapsack(Problem):

    def __init__(self, initial, goal=None):
        self.initial = initial; self.goal = goal
        
    def successor(self, state):
        for item in items:
            newState = State(state.items.copy(), state.weight)
            if newState.add(item):
                yield (0,  newState)
        
        for item in state.items:
            newState = State(state.items.copy(), state.weight)
            if newState.remove(item):
                yield (0, newState)

        for old in state.items:
            for new in items:
                newState = State(state.items.copy(), state.weight)
                if newState.replace(old, new) :
                    yield (0, newState)

         
    def goal_test(self, state):
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        return state.weight 
    

def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = max(list(current.expand()), key= lambda x: x.value())
        if current.value() > best.value():
            best = current
    return best


def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = random.choice(list(islice(sorted(list(current.expand()), key= lambda x: x.value()), 5)))
        if current.value() > best.value():
            best = current
    return best


 
f = open(sys.argv[1], 'r')

n = int(f.readline())

items = {}

for i in range(n):
    line = f.readline()
    split = line.strip().split()
    items[int(split[0])] = (int(split[1]), int(split[2]))

capa = int(f.readline())

current_weight = 0
init_items = {}

for item in sorted(items.items(), key=itemgetter(1)):
    if(current_weight + item[1][0] <= capa): 
        current_weight += item[1][0]
        init_items[item[0]] = item[1]
    else:
        break

init = State(init_items, current_weight)

problem = Knapsack(init)

print(randomized_maxvalue(problem).value())
