import utilities

#################################################################################################
# 	This class creates a representation of the Word Segmentation problem.						#
# 	Suppose you want to segment the string 'hellohowareyoutoday' into the string     		  	#
# 	'hello how are you today'                                                       			#
#																								#
# 	We can represent each state as a tuple of strings, where a comma represents					#
# 	a whitespace between strings, for example: query = 'hellohowareyoutoday'					#
# 	state_1 = (query,) => ('hellohowareyoutoday',)												#
#																								#
# 	The actions we can take is to insert a comma after a letter in the last element 			#
# 	of the tuple, so if we apply the action 1 to the initial_state, we'll have:					#
# 	state_2 = ('h', 'ellohowareyoutoday')														#	
#																								#
# 	And if we apply the action 2 to the state state_2 we'll have								#
# 	state_3 = ('h', 'el', 'lohowareyoutoday') 													#
# 	and so on.																					#
#																								#
# 	The criteria we're using to stop our search is finding the string '' as the 				#
# 	last element of the tuple, because when we found this leaf in our search					#
# 	it will be exactly as our desired result, and the cost will be optimal. 					#
#################################################################################################

class VowelInsertionProblem():
    
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        raise NotImplementedError

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        return ('-BEGIN-',) + tuple(self.queryWords,)

    def actions(self, state):
        import itertools
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        
        sets = []
        for word in state[1:]:
            sets.append(set([x for x in self.possibleFills(word)]))

        actions = list(itertools.product(*sets))

        return actions
    
    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        next_state = ('-BEGIN-',) + action
        return next_state
    
    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        actions = self.actions(state)
        return len(actions) == 0

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        cost = 0
        for i in range(len(action)-1):
            cost += self.bigramCost(action[i], action[i+1])
        return cost


def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
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
	
	
	# resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
	# print(resultInsert)
	
if __name__ == '__main__':
    main()
