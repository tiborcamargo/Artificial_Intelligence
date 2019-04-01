import utilities

#################################################################################################
# 		This class creates a representation of the Vower Insertion problem.		#
#################################################################################################

class VowelInsertionProblem():
    
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ State verification, didnt implement because I quite dont need it"""
        raise NotImplementedError

    def initialState(self):
        """ Retuns the initial state  """
        return ('-BEGIN-',) + tuple(self.queryWords,)

    def actions(self, state):
        import itertools
        """ Returns all given actions you can take given the actual state """
        
        sets = []
        for word in state[1:]:
            sets.append(set([x for x in self.possibleFills(word)]))

        actions = list(itertools.product(*sets))

        return actions
    
    def nextState(self, state, action):
        """ Given an action and your actual state, returns the next state after applying this action """
        next_state = ('-BEGIN-',) + action
        return next_state
    
    def isGoalState(self, state):
        """ Returns if current state is your goal state """
        actions = self.actions(state)
        return len(actions) == 0

    def stepCost(self, state, action):
        """ Return cost for the action """
        cost = 0
        for i in range(len(action)-1):
            cost += self.bigramCost(action[i], action[i+1])
        return cost


def insertVowels(queryWords, bigramCost, possibleFills):
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    goal = utilities.uniformCostSearch(problem)
    if goal == None:
        return ''
    else:
        result = ' '.join(goal.state[1:])
    return result

	
def main():
	""" 
	"""
	_, bigramCost, possibleFills  =  utilities.getRealCosts()
	print('###################################')
	print('vowel_insertion.py initialization')
	print('###################################\n')
	
	query1 = 'wld lk t hv mr lttrs'
	resulSegment = insertVowels(query1.split(), bigramCost, possibleFills)
	print('Your query is: {}'.format(query1))
	print('Your resul is: {}'.format(resulSegment))
	print('\n###################################\n')
	query2 = 'ths tsk s hrd ngh lrdy'
	resulSegment = insertVowels(query2.split(), bigramCost, possibleFills)
	print('Your query is: {}'.format(query2))
	print('Your resul is: {}'.format(resulSegment))
	print('\n###################################')
	print('vowel_insertion.py is done')
	print('###################################')
	

if __name__ == '__main__':
    main()
