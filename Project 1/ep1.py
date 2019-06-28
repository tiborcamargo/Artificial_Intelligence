"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Tibor Zequini Boglár de Camargo
  NUSP : 9302312

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        return 
    
    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        return (self.query,)

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
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
        """ Metodo que implementa teste de meta """
#         print(state)
        return state[-1] == ''

    def stepCost(self, state, action):
        '''
        O problema está aqui!
        '''
        next_state = self.nextState(state, action)
        if state == self.initialState():
            return self.unigramCost(next_state[0])
        else:
            return self.unigramCost(next_state[len(next_state)-2])

def segmentWords(query, unigramCost):

    problem = SegmentationProblem(query, unigramCost)
    goal = util.uniformCostSearch(problem)
    result = ' '.join(goal.state)[:-1]
     
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    return result

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost
class VowelInsertionProblem(util.Problem):
    
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
    goal = util.uniformCostSearch(problem)
    if goal == None:
        return ''
    else:
        result = ' '.join(goal.state[1:])
    return result

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    

    # resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    # print(resultInsert)

if __name__ == '__main__':
    main()
