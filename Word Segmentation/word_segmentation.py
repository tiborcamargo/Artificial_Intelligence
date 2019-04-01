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

class SegmentationProblem():
	def __init__(self, query, unigramCost):
		self.query = query
		self.unigramCost = unigramCost
	
	def isState(self, state):
		""" 
		One should implement a verification of state here, but I haven't done 
		"""
		return 
	
	def initialState(self):
		""" 
		Return the initial state of the problem 	
		"""
		return (self.query,)
	
	def actions(self, state):
		""" 
		Method that returns all actions that can be applied into one stat
		"""
		word = state[-1]
		if state == self.initialState():
			actions = [i+1 for i in range(len(word)-1)]
		else:
			actions = [i+1 for i in range(len(word))]
		return actions
	
	def nextState(self, state, action):
		""" 
		Method that returns the next state after an action has been taken 
		"""
		word = state[-1]
		next_state = state[:-1] + (word[:action], word[action:])
		return next_state
	
	def isGoalState(self, state):
		""" 
		Method that verifies if the current state is the goal state 	
		"""
		return state[-1] == ''
	
	def stepCost(self, state, action):
		"""
		Method that returns the cost of taking an action	
		"""
		next_state = self.nextState(state, action)
		if state == self.initialState():
			return self.unigramCost(next_state[0])
		else:
			return self.unigramCost(next_state[len(next_state)-2])

def segmentWords(query, unigramCost):
	"""
	Given a query, return the query with the whitespaces into proper place
	Ex: query = 'hellohowareyoutoday', segmentWords(query, unigramCost) = 'hello how are you today'
	
	Args:
		query (str): a query that will be segmented with proper whitespaces
		unigramCost (unigramCost): a function that receives a string and outputs it's value in a corpus
		where the least values represents the most common words
	"""
	
	problem = SegmentationProblem(query, unigramCost)
	goal = utilities.uniformCostSearch(problem)
	result = ' '.join(goal.state)[:-1]
	
	return result
	
def main():
	""" 
	"""
	unigramCost, _, _  =  utilities.getRealCosts()
	print('###################################')
	print('word_segmentation.py initialization')
	print('###################################\n')
	
	query1 = 'doesitworkseverytimeidontknow'
	resulSegment = segmentWords(query1, unigramCost)
	print('Your query is: {}'.format(query1))
	print('Your segmentation is: {}'.format(resulSegment))
	print('\n###################################\n')
	query2 = 'thisisanotherexamplewithabiggerstringnotsofast'
	resulSegment = segmentWords(query2, unigramCost)
	print('Your query is: {}'.format(query2))
	print('Your segmentation is: {}'.format(resulSegment))
	print('\n###################################')
	print('word_segmentation.py is done')
	print('###################################')
	
	
	# resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
	# print(resultInsert)
	
if __name__ == '__main__':
    main()
