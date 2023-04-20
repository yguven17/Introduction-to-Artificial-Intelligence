# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import math

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

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = newFood.asList()
        ghostPositions = successorGameState.getGhostPositions()
        score = successorGameState.getScore()

        if len(foodList) == 0:
            return score

        minFoodDistance = min([manhattanDistance(newPos, food) for food in foodList])
        score += 10 * minFoodDistance ** -1
        minGhostDistance = min([manhattanDistance(newPos, ghost) for ghost in ghostPositions])

        if minGhostDistance <= 2 and newScaredTimes[0] == 0:
            return -99999
        elif newScaredTimes[0] > 0:
            score += 100 * minGhostDistance ** -1

        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, bestAction = self.max_value(gameState, 1)
        return bestAction

    def valueChecker(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState), 0
        elif agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        value, bestAction = -math.inf, ""

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)

            tempValue, tempAction = self.valueChecker(successor, depth, 1)

            if tempValue > value:
                value, bestAction = max(value, tempValue), action

        return value, bestAction

    def min_value(self, gameState, depth, agentIndex):
        value, bestAction = math.inf, ""

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex + 1 != gameState.getNumAgents():
                tempValue, tempAction = self.valueChecker(successor, depth, agentIndex + 1)
            else:
                tempValue, tempAction = self.valueChecker(successor, depth + 1, 0)

            value, bestAction = min(value, tempValue), action

        return value, bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = -math.inf, math.inf
        value, bestAction = self.max_value(gameState, 1, alpha, beta)
        return bestAction

    def valueChecker(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState), 0
        elif agentIndex == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        value, bestAction = -math.inf, ""

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)

            tempValue, tempAction = self.valueChecker(successor, depth, 1, alpha, beta)

            if tempValue > value:
                value, bestAction = max(value, tempValue), action

            if value > beta:
                return value, bestAction

            alpha = max(alpha, value)

        return value, bestAction

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        value, bestAction = math.inf, ""

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            numberOfGhosts = gameState.getNumAgents() - 1

            if agentIndex != numberOfGhosts:
                tempValue, tempAction = self.valueChecker(successor, depth, agentIndex + 1, alpha, beta)
            else:
                tempValue, tempAction = self.valueChecker(successor, depth + 1, 0, alpha, beta)

            value, bestAction = min(value, tempValue), action

            if value < alpha:
                return value, bestAction

            beta = min(beta, value)

        return value, bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        value, bestAction = self.max_value(gameState, 1)
        return bestAction

    def valueChecker(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState), 0
        elif agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        value, bestAction = -math.inf, ""

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)

            tempValue, tempAction = self.valueChecker(successor, depth, 1)
            value += tempValue

            if tempValue > value:
                value, bestAction = max(value, tempValue), action

        return value, bestAction

    def min_value(self, gameState, depth, agentIndex):
        value, bestAction = math.inf, ""

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex + 1 != gameState.getNumAgents():
                tempValue, tempAction = self.valueChecker(successor, depth, agentIndex + 1)
            else:
                tempValue, tempAction = self.valueChecker(successor, depth + 1, 0)

            value, bestAction = min(value, tempValue), action

        return value, bestAction


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # Useful information you can extract from a GameState (pacman.py)

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList = newFood.asList()
    ghostPositions = currentGameState.getGhostPositions()
    powerCapsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    if len(foodList) == 0:
        return score

    minFoodDistance = min([manhattanDistance(newPos, foods) for foods in foodList])
    score += 10 * minFoodDistance ** -1
    minGhostDistance = min([manhattanDistance(newPos, ghosts) for ghosts in ghostPositions])

    if minGhostDistance <= 2 and newScaredTimes[0] == 0:
        return -99999

    if newScaredTimes[0] > 0:
        score += 100 * minGhostDistance ** -1

    if len(powerCapsules) != 0:
        minCapsulesDistance = min([manhattanDistance(newPos, capsules) for capsules in powerCapsules])
        if minCapsulesDistance > 0:
            score += minCapsulesDistance ** -1 * 20 * minCapsulesDistance ** -1

    return score


# Abbreviation
better = betterEvaluationFunction
