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

    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.pelletsLeft = len(state.getPellets())
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, state):
        successors = []                                                     
        scored = [] 
        legal = state.getLegalPacmanActions()       
        for action in legal:
            next_successor = state.generatePacmanSuccessor(action)
            x,y = next_successor.getPacmanPosition()
            if ((next_successor.getScore() > state.getScore()) or ((x,y) in state.getCapsules())):
                successors.append((next_successor,action))
        if (not successors):
            return self.AStarAgent(state)
        scored = [(self.scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

        
    def AStarAgent(self, state):
        
        root_scoreEvaluation = self.scoreEvaluation(state)                       #Calculating the score of the root node of tree, as part of heuristic calculation
        successors = []                                                     #Currently successors is initialized to empty list
        scored = []                                                         
        #get the initial legal states and the successors
        legal = state.getLegalPacmanActions()
        depth = 1
        for action in legal:
            initial_successor = state.generatePacmanSuccessor(action)
            #COST = depth - (scoreEvaluation(path) - root_scoreEvaluation)
            cost = depth - (self.scoreEvaluation(initial_successor) - root_scoreEvaluation)
            successors.append((cost, initial_successor , action, depth))
        #continue till the states are present in successor. This will generate the simulating path for pacman
        while(successors):
            #pop the element from successor having the least(minimum) cost and store in variable. Element poped will be in the form of tuble. Seperate the tuple elements
            #Get the state with the least cost
            cost, node, action, depth  = successors.pop(successors.index(min(successors)))
            if (node.isWin()):                                              #Condition if Pacman Reached Win state (virtually simulating path)
                return action
            elif (node.isLose()):
                continue
            #continue to find the legal action and the successor state till the win state is not reached
            else:
                legal = node.getLegalPacmanActions()
                for next_action in legal:
                    next_successor = node.generatePacmanSuccessor(next_action)
                    if (next_successor == None):                            #condition for checking the return state by generatePacmanSuccessor function
                        scored.append((self.scoreEvaluation(node), action))
                    else:
                        #COST = depth - (scoreEvaluation(node) - root_scoreEvaluation)
                        cost = (depth + 1) - (self.scoreEvaluation(node) - root_scoreEvaluation)
                        #If valid successor append it to the end of list, also Append the action of 1st parent(alternative to backtracing) and depth as per its parent
                        successors.append((cost, next_successor, action, depth + 1))
        
        #If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        if(scored):
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        else:
            return Directions.STOP                                          #to avoid the case if no elements in successor


    def scoreEvaluation(self, state):
        return state.getScore() + [0,-1000][state.isLose()] + [0,1000][state.isWin()]

