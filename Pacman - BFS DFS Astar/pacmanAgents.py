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
from heuristics import scoreEvaluation
import random

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

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, state):
        nonetype_flag = 0                   # used to set the flag when None type is returned from getPacmanSuccessor
        successors = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            successors.append((state.generatePacmanSuccessor(action),action))
        while(successors):
            if (nonetype_flag == 1):
                break                       #break while loop
            path, action = successors.pop(0)
            if (path.isWin()):
                print "Reached win state"
                return action
            legal = path.getLegalPacmanActions()
            for next_action in legal:
                next_successor = path.generatePacmanSuccessor(next_action)
                if (next_successor == None):
                    nonetype_flag = 1
                    break
                successors.append((next_successor,action))

        # If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        if(successors):
            scored = [(scoreEvaluation(state), action) for state, action in successors]
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        return Directions.STOP
class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        nonetype_flag = 0                   # used to set the flag when None type is returned from getPacmanSuccessor
        successors = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            successors.append((state.generatePacmanSuccessor(action),action))
        while(successors):
            if (nonetype_flag == 1):
                break                       #break while loop
            path, action = successors.pop(-1)
            if (path.isWin()):
                return action
            legal = path.getLegalPacmanActions()
            for next_action in legal:
                next_successor = path.generatePacmanSuccessor(next_action)
                if (next_successor == None):
                    nonetype_flag = 1
                    break
                successors.append((next_successor,action))

        # If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        if (successors):
            scored = [(scoreEvaluation(state), action) for state, action in successors]
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        return Directions.STOP
        
        

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        
        # TODO: write A* Algorithm instead of returning Directions.STOP
        root_scoreEvaluation = scoreEvaluation(state)
        nonetype_flag = 0                   # used to set the flag when None type is returned from getPacmanSuccessor
        successors = []
        legal = state.getLegalPacmanActions()
        depth = 1
        for action in legal:
            initial_successor = state.generatePacmanSuccessor(action)
            cost = depth - (scoreEvaluation(initial_successor) - root_scoreEvaluation)
            successors.append((cost,initial_successor , action, depth))
        while(successors):
            if (nonetype_flag == 1):
                break                       #break while loop
            #successors.sort()
            #successors.reverse()
            cost, path, action, depth  = successors.pop(successors.index(min(successors)))
            if (path.isWin()):
                print "Reached win state"
                return action
            legal = path.getLegalPacmanActions()
            for next_action in legal:
                next_successor = path.generatePacmanSuccessor(next_action)
                if (next_successor == None):
                    nonetype_flag = 1
                    break
                cost = (depth+1) - (scoreEvaluation(path) - root_scoreEvaluation)
                successors.append((cost, next_successor, action, depth + 1))

        # If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        if(successors):
            scored = [(scoreEvaluation(state), action) for cost, state, action, depth in successors]
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        return Directions.STOP
        '''
        nonetype_flag = 0               # used to set the flag when None type is returned from getPacmanSuccessor
        root_scoreEvaluation = scoreEvaluation(state)
        graph = {}
        parent_node = 0                 #Initializing starting node as 0
        to_be_parent_nodes = []
        child_node = 0
        child_nodes = []
        child_index = 0
        graph[parent_node] = []
        successors = []
        new_nodes = []
        heuristic_cost = []
        depth = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            child_node = child_node + 1
            graph[parent_node].append(child_node)
            child_nodes.append(child_node)
            to_be_parent_nodes.append(child_node)
            successors.append((state.generatePacmanSuccessor(action),action))
            new_nodes.append(state.generatePacmanSuccessor(action))
        while(new_nodes):
            if (nonetype_flag == 1):
                break                       #break while loop
            # Calculate the state with the least cost
            # (depth - (scoreEvaluation(path) - root_scoreEvaluation))
            for state in new_nodes:
                depth = self.backtracing(graph, child_nodes[child_index])
                child_index = child_index + 1
                heuristic_cost.append(depth - (scoreEvaluation(state) - root_scoreEvaluation))
            minimum_cost = min(heuristic_cost)
            pop_node = heuristic_cost.index(minimum_cost)
            next_node, action = successors.pop(pop_node)
            if (next_node.isWin()):
                print "Reached Win State"
                return action
            heuristic_cost.pop(pop_node)
            legal = next_node.getLegalPacmanActions()
            new_nodes =[]
            parent_node = to_be_parent_nodes.pop(pop_node)
            graph[parent_node] = []
            for next_action in legal:
                next_successor = next_node.generatePacmanSuccessor(next_action)
                if (next_successor == None):
                    nonetype_flag = 1
                    break
                child_node = child_node + 1
                graph[parent_node].append(child_node)
                child_nodes.append(child_node)
                to_be_parent_nodes.append(child_node)
                successors.append((next_successor,action))
                new_nodes.append(next_successor)
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        for pair in scored:
            if pair[0] == bestScore:
                # returning the 1st best action
                bestActions = pair[1]
                break
        return bestActions

    # depth calculation
    def backtracing(self,graph, node_count, depth = 1):
        for key in graph:
            if node_count in graph[key]:
                if (key == 0):
                    return depth
                else:
                    node_count = int(key)
                    depth = depth +1
                    return self.backtracing(graph, node_count,depth)
    
        ''' 
