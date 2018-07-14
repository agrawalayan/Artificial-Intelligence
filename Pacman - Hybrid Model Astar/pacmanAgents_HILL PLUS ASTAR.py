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
    def __init__(self):
        self.ACTION_SEQUENCE = 5
        self.RANDOMNESS = 50

    def registerInitialState(self, state):
        self.actionList = []
        for i in range(0,self.ACTION_SEQUENCE):
            self.actionList.append(Directions.STOP)                                         #initializing actionList
        return 
    '''
    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write your algorithm Algorithm instead of returning Directions.STOP
        print state.getGhostPositions()
        print state.getCapsules()
        print state.getPacmanPosition()
        print state.getCapsules()
        print state.getPellets()
        print "---------------------"
    '''
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










        
        self.possible = state.getAllPossibleActions()                                       #all the possible actions for pacman
        for i in range(0,len(self.actionList)):
            self.actionList[i] = self.possible[random.randint(0,len(self.possible)-1)]
        score_check = self.scoreEvaluation(state)                                                #storing the score of root state to compare later
        temp_action_sequence = self.actionList[:]                                           #storing the list in a temporary action sequence
        forward_model = 1
        while(forward_model != 0):
            tempState = state
            for i in range(len(temp_action_sequence)):
                next_successor = tempState.generatePacmanSuccessor(temp_action_sequence[i]) #generating the next successor
                if(next_successor == None):                                                 #checking for None state
                    forward_model = 0
                    break
                elif(next_successor.isWin()):                                               #condition for terminal state
                    break

                elif(next_successor.isLose()):                                              #condition for terminal state
                    break

                else:
                   tempState = next_successor
            if (forward_model == 0):                                                        #if None statethan return the best scoreEvaluation 
                if (self.scoreEvaluation(tempState) >= score_check):
                    self.actionList = temp_action_sequence[:]
                break
            if (self.scoreEvaluation(tempState) >= score_check):
                score_check = self.scoreEvaluation(tempState)
                self.actionList = temp_action_sequence[:]

            else:
                return self.AStarAgent(tempState)
            
            for i in range(len(temp_action_sequence)):
                random_number = random.randint(1,100)                                       #generate a number randomly from 1-100
                if (random_number >= self.RANDOMNESS):
                    temp_action_sequence[i] = self.possible[random.randint(0,len(self.possible)-1)] #mutate each action
                else:
                    temp_action_sequence[i] = self.actionList[i]                            #do not mutate that action


        return self.actionList[0]                                                           #return the 1st action of best sequence

    def AStarAgent(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        root_scoreEvaluation = self.scoreEvaluation(state)                       #Calculating the score of the root node of tree, as part of heuristic calculation
        successors = []                                                     #Currently successors is initialized to empty list
        scored = []                                                         #storing successors when the generatePacmanSuccessor returns None
        forward_model = 1
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
            if (forward_model == 0):
                break
            #successors.index(min(successors))
            successors.sort()
            cost, node, action, depth  = successors.pop(0)
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
                        forward_model = 0
                        break
                    else:
                        #COST = depth - (scoreEvaluation(node) - root_scoreEvaluation)
                        cost = (depth + 1) - (self.scoreEvaluation(node) - root_scoreEvaluation)
                        #If valid successor append it to the end of list, also Append the action of 1st parent(alternative to backtracing) and depth as per its parent
                        successors.append((cost, next_successor, action, depth + 1))
        
        scored = [(self.scoreEvaluation(state), action) for cost, state, action, depth in successors]
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

