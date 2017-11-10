from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """

    # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)
    #multiple min layers (one for each ghost) for every max layer
    def recurse(state, depth, agentIndex): #return (value, move) pair
      if agentIndex == state.getNumAgents():
        agentIndex = 0
      if agentIndex == 0:
        depth -= 1

      legalMoves = state.getLegalActions(agentIndex)
      if state.isWin() or state.isLose() or len(legalMoves)==0:
        return (state.getScore(), Directions.STOP)
      if depth==0:
        return (self.evaluationFunction(state), Directions.STOP)
      
      all_scores_moves = []
      for nextMove in legalMoves:
        nextState = state.generateSuccessor(agentIndex, nextMove)
        all_scores_moves.append((recurse(nextState, depth, agentIndex+1)[0], nextMove)) #loop through all agents thus agentIndex+1
      if agentIndex == 0:
        opt_score = max(all_scores_moves)[0]
      else:
        opt_score = min(all_scores_moves)[0]

      bestIndices = [index for index in range(len(all_scores_moves)) if all_scores_moves[index][0] == opt_score]
      chosenIndex = random.choice(bestIndices)
      return all_scores_moves[chosenIndex]

    score, action = recurse(gameState, self.depth+1, self.index) #since decrement depth at the start where agentIndex=0
    #print score
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (our solution is 49 lines of code, but don't worry if you deviate from this)
    #BASED ON PSEUDOCODE FROM HERE: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    def recurse(state, depth, agentIndex, alpha, beta): #return (value, move) pair
      if agentIndex == state.getNumAgents():
        agentIndex = 0
      if agentIndex == 0:
        depth -= 1

      legalMoves = state.getLegalActions(agentIndex)
      if state.isWin() or state.isLose() or len(legalMoves)==0:
        return (state.getScore(), Directions.STOP)
      if depth==0:
        return (self.evaluationFunction(state), Directions.STOP)
      
      all_scores_moves = []
      if agentIndex == 0:
        thres = float('-inf')
        chosen_move = Directions.STOP
        for nextMove in legalMoves:
          nextState = state.generateSuccessor(agentIndex, nextMove)
          score_next_move = recurse(nextState, depth, agentIndex+1, alpha, beta)[0]
          if score_next_move > thres:
            thres = score_next_move
            chosen_move = nextMove
          alpha = max(alpha, thres)

          if beta <= alpha:
            return (alpha, nextMove)
        return (thres, chosen_move)

      else:
        thres = float('inf')
        chosen_move = Directions.STOP
        for nextMove in legalMoves:
          nextState = state.generateSuccessor(agentIndex, nextMove)
          score_next_move = recurse(nextState, depth, agentIndex+1, alpha, beta)[0]
          if score_next_move < thres:
            thres = score_next_move
            chosen_move = nextMove
          beta = min(beta, thres)
          if beta <= alpha:
            return (beta, nextMove)
        return (thres, chosen_move)

      # bestIndices = [index for index in range(len(all_scores_moves)) if all_scores_moves[index][0] == opt_score]
      # chosenIndex = random.choice(bestIndices)
      # return all_scores_moves[chosenIndex]

    score, action = recurse(gameState, self.depth+1, self.index, float('-inf'), float('inf')) #since decrement depth at the start where agentIndex=0
    print score
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
    def recurse(state, depth, agentIndex): #return (value, move) pair
      if agentIndex == state.getNumAgents():
        agentIndex = 0
      if agentIndex == 0:
        depth -= 1

      legalMoves = state.getLegalActions(agentIndex)
      if state.isWin() or state.isLose() or len(legalMoves)==0:
        return (state.getScore(), Directions.STOP)
      if depth==0:
        return (self.evaluationFunction(state), Directions.STOP)
      
      all_scores_moves = []
      for nextMove in legalMoves:
        nextState = state.generateSuccessor(agentIndex, nextMove)
        all_scores_moves.append((recurse(nextState, depth, agentIndex+1)[0], nextMove)) #loop through all agents thus agentIndex+1
      if agentIndex == 0:
        opt_score = max(all_scores_moves)[0]
        bestIndices = [index for index in range(len(all_scores_moves)) if all_scores_moves[index][0] == opt_score]
        chosenIndex = random.choice(bestIndices)
        return all_scores_moves[chosenIndex]
      else: #random move
        random_action = random.choice(all_scores_moves)[1]      
        expected_score = sum([item[0] for item in all_scores_moves])/len(all_scores_moves)
        return expected_score, random_action


    score, action = recurse(gameState, self.depth+1, self.index) #since decrement depth at the start where agentIndex=0
    return action
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
    Adding the following consideration to evaluationFunction:
    - minimum scared time of all the existing ghosts: the larger the better
    - total number of food left: negative coefficient so that pacman eats the food right away
    - total number of capsules left: large negative coefficient so that pacman prioritizes eating this
    - distance to the closest scared ghost: negative coefficient/inverse so that pacman rushes the closest ghost
    - distance to the closest food: negative coefficient/ inverse so that pacman would try to come closer to it and eat it quickly 
    I have experimented with many different combinations of coefficients and alternated between using negative coefficient (-) and inverse (1/)
  """

  # BEGIN_YOUR_CODE (our solution is 26 lines of code, but don't worry if you deviate from this)
  currPos = currentGameState.getPacmanPosition()
  currentFood = currentGameState.getFood()
  n_food = sum(map(sum, currentFood))
  currentCapsules = currentGameState.getCapsules()
  n_capsules = len(currentCapsules)
  currentGhostStates = currentGameState.getGhostStates()
  currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
  all_dist_to_ghost = [manhattanDistance(currPos, ghostState.configuration.pos) for ghostState in currentGhostStates]
  min_dist_to_ghost = min(all_dist_to_ghost)
  min_dist_to_food = min(map(lambda f: manhattanDistance(currPos, f), currentFood))
  #min_dist_to_capsules = min(map(lambda c: manhattanDistance(currPos, c), currentCapsules))

  score = currentGameState.getScore() - 3* n_food - 20*n_capsules \
                                      + 1/min_dist_to_food + 2/min_dist_to_ghost - min_dist_to_ghost/min(min(currentScaredTimes)+0.5, 15)
  # if min(currentScaredTimes) > 15:
  #   score = score - min_dist_to_ghost*5/(min(currentScaredTimes)+1)
  # else:
  #   score = score + min_dist_to_ghost*10/(min(currentScaredTimes)+1)
  return score
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction
