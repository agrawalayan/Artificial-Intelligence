# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class CompetitionAgent(Agent):
    '''
    print state.getGhostPositions()
    print state.getCapsules()
    print state.getPacmanPosition()
    print state.getCapsules()
    print state.getPellets()
    print "---------------------"
    '''
    
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, state):
        successors = []                                                     #Currently successors is initialized to empty list
        root_score = self.scoreEvaluation(state)
        scored = []                                                         #storing successors when the generatePacmanSuccessor returns None
        self.forward_model = 1
        #print "BFS Called"
        print state.getCapsules()
        print state.getPellets()
        print "---------------------"
        legal = state.getLegalPacmanActions()
        for action in legal:
            next_successor = state.generatePacmanSuccessor(action)
            if (next_successor.getScore() < state.getScore()):
                next_successor = self.AStarAgent(next_successor, action, next_successor.getScore())
                #print "Back to BFS - 1"
                print "Get Score -- 1", next_successor
                print "Get Score -- 2", state
            successors.append((next_successor,action))
        #continue till the states are present in successor. This will generate the simulating path for pacman
        while(successors):
            if (self.forward_model == 0):
                break
            node, action = successors.pop(0)                                #BFS implements Queue Data Structure(FIFO) --> poping the first element from the list
            if (node.isWin()):                                              #condition if Pacman Reached Win state (virtually simulating path)
                return action
            elif (node.isLose()):
                continue                                                    #eliminating the lose nodes
            #continue to find the legal action and the successor state till the win state is not reached
            else:
                legal = node.getLegalPacmanActions()
                for next_action in legal:
                    next_successor = node.generatePacmanSuccessor(next_action)
                    if (next_successor == None):                            #condition for checking the return state by generatePacmanSuccessor function 
                        self.forward_model = 0
                        break
                    elif (next_successor.isWin()):                                              #condition if Pacman Reached Win state (virtually simulating path)
                        return action
                    elif (next_successor.isLose()):
                        continue                                                    #eliminating the lose nodes
                    else:
                        if (next_successor.getScore() < node.getScore()):
                            print "Get Score -- 3", next_successor
                            print "Get Score -- 4", node
                            next_successor = self.AStarAgent(next_successor, next_action, next_successor.getScore())
                            #print "Back to BFS - 2"
                        successors.append((next_successor,action))
            
        #If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        scored = [(self.scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        for pair in scored:
            if pair[0] == bestScore:
                # returning the 1st best action
                bestActions = pair[1]
                break
        return bestActions



    
    def AStarAgent(self, state, action, scoreAtThatState):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        #print "In Astar"
        root_scoreEvaluation = self.scoreEvaluation(state)      #Calculating the score of the root node of tree, as part of heuristic calculation
        successors = []                                                     #Currently successors is initialized to empty list
        scored = []                                                         #storing successors when the generatePacmanSuccessor returns None
        #get the initial legal states and the successors
        #legal = state.getLegalPacmanActions()
        depth = 1
        #initial_successor = state.generatePacmanSuccessor(action)
        cost = depth - (self.scoreEvaluation(state) - root_scoreEvaluation)
        successors.append((cost, state , action, depth))
        #continue till the states are present in successor. This will generate the simulating path for pacman
        while(successors):
            #pop the element from successor having the least(minimum) cost and store in variable. Element poped will be in the form of tuble. Seperate the tuple elements
            #Get the state with the least cost
            if (self.forward_model == 0):
                break
            #successors.index(min(successors))
            successors.sort()
            cost, node, action, depth  = successors.pop(0)
            if (node.isWin()):                                              #Condition if Pacman Reached Win state (virtually simulating path)
                print "Reached win state"
                return node
            #elif (node.isLose()):
            #    print "Reached Loose state"
            #    continue
            #continue to find the legal action and the successor state till the win state is not reached
            else:
                legal = node.getLegalPacmanActions()
                for next_action in legal:
                    next_successor = node.generatePacmanSuccessor(next_action)
                    if (next_successor == None):                            #condition for checking the return state by generatePacmanSuccessor function
                        self.forward_model = 0
                        break
                    else:
                        if (next_successor.getScore() > scoreAtThatState):
                            return next_successor
                        #COST = depth - (scoreEvaluation(node) - root_scoreEvaluation)
                        cost = (depth + 1) - (self.scoreEvaluation(node) - root_scoreEvaluation)
                        #If valid successor append it to the end of list, also Append the action of 1st parent(alternative to backtracing) and depth as per its parent
                        successors.append((cost, next_successor, action, depth + 1))
        
        scored = [(self.scoreEvaluation(state), state) for cost, state, action, depth in successors]
        #If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        if(scored):
            #print "returning back to BFS - 1"
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestState = pair[1]
                    break
            return bestState
        else:
            #print "returning back to BFS - 2"
            return state                                         #to avoid the case if no elements in successor


    def scoreEvaluation(self, state):
        return state.getScore() + [0,-1000][state.isLose()] + [0,1000][state.isWin()]

