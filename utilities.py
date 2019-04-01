from node import Node

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""
    def __init__(self, key, items=(),): 
        self.key = key
        self.items = []    # a heap of (score, counter, item) pairs
        self.count = 0
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queue."""
        m_tuple = (self.key(item),self.count, item)
        self.count += 1
        heapq.heappush(self.items, m_tuple)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[2]
    
    def top(self): return self.items[0][2]

    def __len__(self): return len(self.items)

def informed_search(problem, f):
    """Informed search using as a key of the Priority Queue f"""

    initialNode = Node(problem.initialState(), 0)
    frontier= PriorityQueue(f, [initialNode])
    reached = dict()
    reached[initialNode.state] = initialNode.cost
    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node
        for action in problem.actions(node.state):
            state = problem.nextState(node.state, action)
            cost = problem.stepCost(node.state, action) + node.cost
            if state not in reached or  cost < reached[state] :
                reached[state] = cost
                frontier.add(Node(state, cost, node, action))
    return None

def uniformCostSearch(problem):
    """ Implementa busca de custo uniforme no problema problem

        A funcao :func:'uniformCostSearch' recebe um problema problem e
        retorna None se o problema não contiver solucao, caso contrario
        retorna um no busca contendo um estado meta do problema.

        :param problem: Objeto da classe Problem descrita no enunciado
        :type problem: <class 'Problem'>
        :return solution: Um no de busca atualizado com a solucao ou None c.c.
        :rtype: <class 'Node'> or <class 'NoneType'>

        :Example:

        
        >>> goal = uniformCostSearch(problem)
        >>> goal.state
        (1,2,3,4,5,6,7,8,0)
        >>> goal.parent
        <__main__.node object at 0x7f29fbc301d0>
    """
    return informed_search(problem,lambda node: node.cost)
