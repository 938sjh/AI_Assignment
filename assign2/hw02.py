from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
    """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
    """
    ####################### Write Your Code Here ################################
    def Action(self, gameState):
        def pacman_max(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = float("-inf") 
            
            for action in state.getLegalActions(0):
                new_state = state.generateSuccessor(0, action)
                value = max(value, ghost_min(new_state, depth, state.getNumAgents()-1))
            
            return value

        def ghost_min(state, depth, agent_index):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = float("inf")

            for action in state.getLegalActions(agent_index):
                new_state = state.generateSuccessor(agent_index, action)
                
                if(agent_index > 1):
                    value = min(value, ghost_min(new_state, depth, agent_index - 1))
                else:
                    value = min(value, pacman_max(new_state, depth + 1))

            return value
       
        result_action = None
        value = float("-inf")

        
        for action in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(0, action)
            temp_value = ghost_min(new_state, 0, gameState.getNumAgents()-1)

            if temp_value > value:
                value = temp_value
                result_action = action

        return result_action

    ############################################################################

class AlphaBetaAgent(AdversialSearchAgent):
    """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
     """
    def Action(self, gameState):
    ####################### Write Your Code Here ################################
    
        def pac_max(state, depth, a, b):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = float("-inf")

            for action in state.getLegalActions(0):
                new_state = state.generateSuccessor(0, action)

                value = max(value, ghost_min(new_state, depth, state.getNumAgents()-1, a, b))
                if value >= b:
                    return value
                a = max(a, value)
        
            return value


        def ghost_min(state, depth, agent_index, a, b):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = float("inf")

            for action in state.getLegalActions(agent_index):
                new_state = state.generateSuccessor(agent_index, action)

                if agent_index > 1:
                    value = min(value, ghost_min(new_state, depth, agent_index - 1, a, b))
                else:
                    value = min(value, pac_max(new_state, depth + 1, a, b))
                if value <= a:
                    return value
                b = min(b, value)
            return value

        result_action = None
        value = float("-inf")
        a = float("-inf")
        b = float("inf")

        for action in gameState.getLegalActions(0):
            temp_value = ghost_min(gameState.generateSuccessor(0, action), 0, gameState.getNumAgents()-1, a, b)
            if temp_value > value:
                value = temp_value
                result_action = action
        
        return result_action

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
    """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
    """
    def Action(self, gameState):
    ####################### Write Your Code Here ################################
        def pac_max(state,depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = float("-inf")
            
            for action in state.getLegalActions(0):
                new_state = state.generateSuccessor(0, action)
                value = max(value, ghost_min(new_state, depth, state.getNumAgents()-1))

            return value

        def ghost_min(state, depth, agent_index):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value_sum = 0
            cnt = 0

            for action in state.getLegalActions(agent_index):
                new_state = state.generateSuccessor(agent_index, action)
                cnt += 1
                
                if agent_index > 1:
                    value_sum += ghost_min(new_state, depth, agent_index - 1)
                else:
                    value_sum += pac_max(new_state, depth + 1)
            
            return float(value_sum) / cnt

        result_action = None
        value = float("-inf")
        
        for action in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(0, action)
            temp_value = ghost_min(new_state, 0, gameState.getNumAgents()-1)

            if temp_value > value:
                value = temp_value
                result_action = action

        return result_action

    ############################################################################
