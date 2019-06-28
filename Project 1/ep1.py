import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ State verification method"""
        return 
    
    def initialState(self):
        """ Initial position method """
        return (self.query,)

    def actions(self, state):
        """ Implementation of valid actions given a state """
        word = state[-1]
        if state == self.initialState():
            actions = [i+1 for i in range(len(word)-1)]
        else:
            actions = [i+1 for i in range(len(word))]
        return actions
    
    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        word = state[-1]
        next_state = state[:-1] + (word[:action], word[action:])
        return next_state
    
    def isGoalState(self, state):
        """ Verifying if given state is a goal state """
#         print(state)
        return state[-1] == ''

    def stepCost(self, state, action):
        next_state = self.nextState(state, action)
        if state == self.initialState():
            return self.unigramCost(next_state[0])
        else:
            return self.unigramCost(next_state[len(next_state)-2])

def segmentWords(query, unigramCost):
    problem = SegmentationProblem(query, unigramCost)
    goal = util.uniformCostSearch(problem)
    result = ' '.join(goal.state)[:-1]
    return result
############################################################
# Part 2: Vowel insertion problem under a bigram cost
class VowelInsertionProblem(util.Problem):
    
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Verification if given state is a state """
        raise NotImplementedError

    def initialState(self):
        """ Returns initial state """
        return ('-BEGIN-',) + tuple(self.queryWords,)

    def actions(self, state):
        import itertools
        """ Given a state, return valid actions """
        
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
        """ Verification if given state is a goal state """
        actions = self.actions(state)
        return len(actions) == 0

    def stepCost(self, state, action):
        """ Cost function implementation """
        cost = 0
        for i in range(len(action)-1):
            cost += self.bigramCost(action[i], action[i+1])
        return cost


def insertVowels(queryWords, bigramCost, possibleFills):
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    goal = util.uniformCostSearch(problem)
    if goal == None:
        return ''
    else:
        result = ' '.join(goal.state[1:])
    return result

############################################################


def getRealCosts(corpus='corpus.txt'):
    """ Returns the cost functions unigram, bigram and possible fills given the corpus """    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)

if __name__ == '__main__':
    main()
