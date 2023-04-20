# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def searchAlgorithm(problem, input1 ,input2 ):

    visitedSets = set()

    if input1 == "dfs":
        type = util.Stack()
        type.push((problem.getStartState(), []))
    elif input1 == "bfs":
        type = util.Queue()
        type.push((problem.getStartState(), []))
    elif input1 == "ucs" or input1 == "astar":
        type == util.PriorityQueue()
        type.push((problem.getStartState(), []), 0)

    while not type.isEmpty():
        typeState, actions = type.pop()

        if typeState in visitedSets:
            continue

        visitedSets.add(typeState)

        if problem.isGoalState(typeState):
            return actions

        if input1 == "dfs" or input1 == "bfs":
            for succState, actState, stepState in problem.getSuccessors(typeState):
                if succState not in visitedSets:
                    type.push((succState, actions + [actState]))
        elif input1 == "ucs":
            for succState, actState, stepState in problem.getSuccessors(typeState):
                if succState not in visitedSets:
                    type.push((succState, actions + [actState]),
                    stepState + problem.getCostOfActions(actions))
        elif input1 == "astar":
            for succState, actState, stepState in problem.getSuccessors(typeState):
                if succState not in visitedSets:
                    type.push((succState, actions + [actState]),
                    stepState + problem.getCostOfActions(actions) +
                    input2(succState, problem=problem))
    util.raiseNotDefined()

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    ##print("Start:", problem.getStartState())
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))

    ##searchAlgorithm(problem, dfs,0)

    stack = util.Stack()
    visitedSets = set()
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        stackState, actions = stack.pop()

        if stackState in visitedSets:
            continue

        visitedSets.add(stackState)

        if problem.isGoalState(stackState):
            return actions

        for succState, actState, stepState in problem.getSuccessors(stackState):
            if succState not in visitedSets:
                stack.push((succState, actions + [actState]))
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    ##print("Start:", problem.getStartState())
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))

    ##searchAlgorithm(problem, "bfs",0)

    visitedSets = set()
    queue = util.Queue()
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():
        queueState, actions = queue.pop()

        if queueState in visitedSets:
            continue

        visitedSets.add(queueState)

        if problem.isGoalState(queueState):
            return actions

        for succState, actState, stepState in problem.getSuccessors(queueState):
            if succState not in visitedSets:
                queue.push((succState, actions + [actState]))
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    ##print("Start:", problem.getStartState())
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))

    ##searchAlgorithm(problem, "ucs",0)

    visitedSets = set()
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), []), 0)

    while not priorityQueue.isEmpty():
        pqueueState, actions = priorityQueue.pop()

        if pqueueState in visitedSets:
            continue

        visitedSets.add(pqueueState)

        if problem.isGoalState(pqueueState):
            return actions

        for succState, actState, stepState in problem.getSuccessors(pqueueState):
            if succState not in visitedSets:
                priorityQueue.push(
                    (succState, actions + [actState]),
                    stepState + problem.getCostOfActions(actions))
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    ##print("Start:", problem.getStartState())
    ##print("Is the start a goal?", problem.isGoalState(problem.getStartState()))

    # searchAlgorithm(problem, "astar", heuristic=nullHeuristic)

    visitedSets = set()
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), []), 0)

    while not priorityQueue.isEmpty():
        pqueueState, actions = priorityQueue.pop()

        if pqueueState in visitedSets:
            continue

        visitedSets.add(pqueueState)

        if problem.isGoalState(pqueueState):
            return actions

        for succState, actState, stepState in problem.getSuccessors(pqueueState):
            if succState not in visitedSets:
                priorityQueue.push(
                    (succState, actions + [actState]),
                    stepState + problem.getCostOfActions(actions) +
                    heuristic(succState, problem=problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
