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
from heuristics import *
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

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def __init__(self):
        self.ACTION_SEQUENCE = 5
        self.RANDOMNESS = 50

    def registerInitialState(self, state):
        self.actionList = []
        for i in range(0,self.ACTION_SEQUENCE):
            self.actionList.append(Directions.STOP)                                         #initializing actionList
        return 
    # TODO: write Hill Climber Algorithm instead of returning Directions.STOP

    def getAction(self, state):
        self.possible = state.getAllPossibleActions()                                       #all the possible actions for pacman
        for i in range(0,len(self.actionList)):
            self.actionList[i] = self.possible[random.randint(0,len(self.possible)-1)]
        score_check = scoreEvaluation(state)                                                #storing the score of root state to compare later
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
                if (scoreEvaluation(tempState) >= score_check):
                    self.actionList = temp_action_sequence[:]
                break
            if (scoreEvaluation(tempState) >= score_check):
                score_check = scoreEvaluation(tempState)
                self.actionList = temp_action_sequence[:]


            for i in range(len(temp_action_sequence)):
                random_number = random.randint(1,100)                                       #generate a number randomly from 1-100
                if (random_number >= self.RANDOMNESS):
                    temp_action_sequence[i] = self.possible[random.randint(0,len(self.possible)-1)] #mutate each action
                else:
                    temp_action_sequence[i] = self.actionList[i]                            #do not mutate that action


        return self.actionList[0]                                                           #return the 1st action of best sequence



class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def __init__(self):
        self.ACTION_SEQUENCE = 5
        self.POPULATION_SIZE = 8
        self.CROSS_OVER = 70
        self.CHILD_CROSS_OVER_FORMATION = 50
        self.MUTATE = 10

    def registerInitialState(self, state):
        self.actionList = []
        for i in range(self.ACTION_SEQUENCE):
            self.actionList.append(Directions.STOP)
        return

    def last_state(self,state):
        last_state_of_every_sequence = []
        for i in range(self.POPULATION_SIZE):
            last_state_of_every_sequence.append(state)
        return last_state_of_every_sequence
            
    def initialize_parents(self,state):
        population = []
        self.possible = state.getAllPossibleActions()
        for i in range(self.POPULATION_SIZE):
            for j in range(0,len(self.actionList)):
                self.actionList[j] = self.possible[random.randint(0,len(self.possible)-1)];
            population.append(self.actionList)
        return population



    def fitness_calculation(self, population, last_state_of_every_sequence):
        fitness_of_population = []


        for i in range(self.POPULATION_SIZE):
            last_state_of_population = last_state_of_every_sequence[i]
	    fitness_score = scoreEvaluation(last_state_of_population)
            fitness_of_population.append((fitness_score,population[i]))

        return fitness_of_population
        

    def rank_chromosome(self, fitness_of_population):
        fitness_of_population.sort()
        fitness_of_population.reverse()
        rank = 1
        chromosomes_rank_fitness = []
        for i in range(self.POPULATION_SIZE):
            chromosomes_rank_fitness.append((rank, fitness_of_population[i][1]))
            rank+=1
        return chromosomes_rank_fitness

    
    def generate_next_population(self, chromosomes_rank_fitness):
        next_generation = []
        parent_selection = [0,0]
        for j in range(self.POPULATION_SIZE/2):
            
            for k in range(2): 
                rank_proportinality_selection = random.randint(1, 36)
                if ( 28 < rank_proportinality_selection <= 36):
                    parent_selection[k] = chromosomes_rank_fitness[0][1]
                elif ( 21 < rank_proportinality_selection <= 28):
                    parent_selection[k] = chromosomes_rank_fitness[1][1]
                elif ( 15 < rank_proportinality_selection <= 21):
                    parent_selection[k] = chromosomes_rank_fitness[2][1]
                elif ( 10 < rank_proportinality_selection <= 15):
                    parent_selection[k] = chromosomes_rank_fitness[3][1]
                elif ( 6 < rank_proportinality_selection <= 10):
                    parent_selection[k] = chromosomes_rank_fitness[4][1]
                elif ( 3 < rank_proportinality_selection <= 6):
                    parent_selection[k] = chromosomes_rank_fitness[5][1]
                elif ( 1 < rank_proportinality_selection <= 3):
                    parent_selection[k] = chromosomes_rank_fitness[6][1]
                elif ( 0 < rank_proportinality_selection <= 1):
                    parent_selection[k] = chromosomes_rank_fitness[7][1]

            
            
            if (random.randint(1,100) <= self.CROSS_OVER):
                child_1, child_2 = self.crossover(parent_selection)
                
            else:
                child_1 = parent_selection[0]
                child_2 = parent_selection[1]
            next_generation.append(child_1)
            next_generation.append(child_2)

    
        return next_generation

    def crossover(self, parent_selection):
        child_1 = []
        child_2 = []
        for i in range(self.ACTION_SEQUENCE):
            if random.randint(1, 100) <= self.CHILD_CROSS_OVER_FORMATION:
                child_1.append(parent_selection[0][i])
                child_2.append(parent_selection[1][i])
            else:
                child_1.append(parent_selection[1][i])
                child_2.append(parent_selection[0][i])

        return child_1, child_2
        
    def mutate(self, next_generation):
        for children in next_generation:
                if random.randint(1, 100) <= self.MUTATE:
                    children[random.randint(0, len(children)-1)] = random.choice(self.possible)
        return next_generation


    def getAction(self, state):
        last_state_of_every_sequence = self.last_state(state)                               #used to store the last state after generatePacmanSuccessor, useful for score
        forward_model = 1
        scored = []
        population = self.initialize_parents(state)
        tempState = state
        self.prev_population = population[:][:]
        self.prev_last_state_of_every_sequence = last_state_of_every_sequence[:]


        while(forward_model != 0):

            for i in range(self.POPULATION_SIZE):
                tempState = state
                for j in range(self.ACTION_SEQUENCE):
                    next_successor = tempState.generatePacmanSuccessor(population[i][j])
                    if(next_successor == None):
                        forward_model = 0
                        break 
                    if(next_successor.isWin()):
                        break  
                    if(next_successor.isLose()):
                        break  
                    else:
                       tempState = next_successor
                last_state_of_every_sequence[i] = tempState
                if (forward_model == 0):
                    break
            if (forward_model == 0):
                break
            
            fitness_of_population = self.fitness_calculation(population, last_state_of_every_sequence)
            chromosomes_rank_fitness = self.rank_chromosome(fitness_of_population)
            next_generation = self.generate_next_population(chromosomes_rank_fitness)
            population = self.mutate(next_generation)
            self.prev_population = population[:][:]
            self.prev_last_state_of_every_sequence = last_state_of_every_sequence[:]

        #if new population remains incomplete and None is returned, consider old population
        if (forward_model == 0):
            population = self.prev_population[:][:]
            last_state_of_every_sequence = self.prev_last_state_of_every_sequence[:]

        #calculate the best of all in the population set
        fitness_of_last_population = []
        for i in range(self.POPULATION_SIZE):
            last_state_of_population = last_state_of_every_sequence[i]
	    fitness_score = scoreEvaluation(last_state_of_population)
            fitness_of_last_population.append(fitness_score)
        Max_score = max(fitness_of_last_population)
        
        sequence_index = fitness_of_last_population.index(Max_score)
        finding_first_action = population[sequence_index]
        return finding_first_action[0]



class Node():
    def __init__(self, state, parent = None, action = None):
        self.reward = 0
        self.number_of_visit = 0
        self.unexplored_actions = state.getLegalPacmanActions()
        self.parent = parent
        self.children = []
        self.action = action

class MCTSAgent(Agent):
    def __init__(self):
        self.RANDOM_ROLLOUT = 5
        self.CONSTANT = 1

    def registerInitialState(self, state):
        return

    def getAction(self, state):
        node = Node(state)
        self.forward_model = 1
        self.flag = 0
        while(self.forward_model != 0):
            self.flag = 0
            next_node = self.tree_policy(node, state)
            if (self.forward_model == 0):
                break
            if (self.flag == 1):
                continue
            delta = self.default_policy(next_node, state)
            if (self.forward_model == 0):
                break
            if (self.flag == 1):
                continue
            self.backup(next_node, delta)
        most_visited_times = 0
        best_node = node
        for i in range(len(node.children)):
            child_node = node.children[i]
            if (child_node.number_of_visit > most_visited_times):
                most_visited_times = child_node.number_of_visit
                best_node = child_node
        return best_node.action



    def tree_policy(self, node, state):
        while(self.forward_model != 0):
            if (len(node.unexplored_actions) > 0):
                return self.expand(node, state)
            else:
                prev_node = node
                node = self.select(node)
                if node is prev_node:
                    break
        return node
                
                
    def expand(self, node, state):
        tempNode = node
        tempState = state
        back_actions = []
        allNodes = []
        while(node.parent != None):
            back_actions.append(node.action)
            allNodes.append(node)
            node = node.parent
        for i in range(len(back_actions)):
            reverse_action = back_actions.pop(-1)
            reverse_node = allNodes.pop(-1)
            child = tempState.generatePacmanSuccessor(reverse_action)
            if (child == None):
                self.forward_model = 0
                return
            elif(child.isWin() + child.isLose() == 1):
                reward = normalizedScoreEvaluation(state, child)
                self.backup(reverse_node, reward)
                self.flag = 1
                return reverse_node
            else:
                tempState = child
        
        action = random.choice(tempNode.unexplored_actions)
        explore_child = tempState.generatePacmanSuccessor(action)
        if (explore_child == None):
            self.forward_model = 0
            return
        elif(explore_child.isWin() + explore_child.isLose() == 1):
            reward = normalizedScoreEvaluation(state, explore_child)
            self.backup(tempNode, reward)
            self.flag = 1
            return tempNode
        else:
            tempNode.unexplored_actions.pop(tempNode.unexplored_actions.index(action))
            next_node = Node(explore_child, tempNode, action)
            tempNode.children.append(next_node)
            return next_node

    def select(self, node):
        UCT_max = 0
        best_node = node
        for i in range(len(node.children)):
            child_node = node.children[i]
            #if (child_node.number_of_visit == 0):
                #child_node.number_of_visit = 1
            UCT_score = (child_node.reward/child_node.number_of_visit) + self.CONSTANT*math.sqrt(2*math.log(node.number_of_visit)/child_node.number_of_visit)
            if UCT_score > UCT_max:
                UCT_max = UCT_score
                best_node = child_node
        return best_node
            

    def default_policy(self, node, state):
        tempNode = node
        tempState = state
        back_actions = []
        allNodes = []
        while(node.parent != None):
            back_actions.append(node.action)
            allNodes.append(node)
            node = node.parent
        for i in range(len(back_actions)):
            action = back_actions.pop(-1)
            reverse_node = allNodes.pop(-1)
            child = tempState.generatePacmanSuccessor(action)
            if (child == None):
                self.forward_model = 0
                return
            elif(child.isWin() + child.isLose() == 1):
                reward = normalizedScoreEvaluation(state, child)
                self.backup(reverse_node, reward)
                self.flag = 1
                return reward
            else:
                tempState = child
        for i in range(self.RANDOM_ROLLOUT):
            legal_actions = tempState.getLegalPacmanActions()
            action = random.choice(legal_actions)
            child = tempState.generatePacmanSuccessor(action)
            if (child == None):
                self.forward_model = 0
                break
            elif(child.isWin() + child.isLose() == 1):
                reward = normalizedScoreEvaluation(state, child)
                self.backup(tempNode, reward)
                self.flag = 1
                return reward
            else:
                tempState = child
        reward = normalizedScoreEvaluation(state, tempState)
        return reward
            
    def backup(self, node, reward):
        while True:
            node.number_of_visit = node.number_of_visit + 1
            node.reward = node.reward + reward
            if (node.parent == None):
                break
            node = node.parent 





class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        root_scoreEvaluation = scoreEvaluation(state)                       #Calculating the score of the root node of tree, as part of heuristic calculation
        successors = []                                                     #Currently successors is initialized to empty list
        scored = []                                                         #storing successors when the generatePacmanSuccessor returns None
        win_states = []                                                     #appending win state in list, taking the best of all win state
        #get the initial legal states and the successors
        legal = state.getLegalPacmanActions()
        depth = 1
        for action in legal:
            initial_successor = state.generatePacmanSuccessor(action)
            #COST = depth - (scoreEvaluation(path) - root_scoreEvaluation)
            cost = depth - (scoreEvaluation(initial_successor) - root_scoreEvaluation)
            successors.append((cost, initial_successor , action, depth))
        #continue till the states are present in successor. This will generate the simulating path for pacman
        while(successors):
            #pop the element from successor having the least(minimum) cost and store in variable. Element poped will be in the form of tuble. Seperate the tuple elements
            #Get the state with the least cost
            cost, node, action, depth  = successors.pop(successors.index(min(successors)))
            if (node.isWin()):                                              #Condition if Pacman Reached Win state (virtually simulating path)
                win_states.append((node,action))                            #appending the win state and finding for more better win state
                print "Reached win state"
                #return action
            elif (node.isLose()):
                continue
            #continue to find the legal action and the successor state till the win state is not reached
            else:
                legal = node.getLegalPacmanActions()
                for next_action in legal:
                    next_successor = node.generatePacmanSuccessor(next_action)
                    if (next_successor == None):                            #condition for checking the return state by generatePacmanSuccessor function
                        scored.append((scoreEvaluation(node), action))
                    else:
                        #COST = depth - (scoreEvaluation(node) - root_scoreEvaluation)
                        cost = (depth + 1) - (scoreEvaluation(node) - root_scoreEvaluation)
                        #If valid successor append it to the end of list, also Append the action of 1st parent(alternative to backtracing) and depth as per its parent
                        successors.append((cost, next_successor, action, depth + 1))
        
        if(win_states):
            bestScore = max(win_states)[0]
            for pair in win_states:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        
        #If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        elif(scored):
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        else:
            return Directions.STOP                                          #to avoid the case if no elements in successor



class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, state):
        successors = []                                                     #Currently successors is initialized to empty list
        scored = []                                                         #storing successors when the generatePacmanSuccessor returns None
        win_states = []                                                     #appending win state in list, taking the best of all win state
        #get the initial legal states and the successors
        legal = state.getLegalPacmanActions()       
        for action in legal:
            successors.append((state.generatePacmanSuccessor(action),action))
        #continue till the states are present in successor. This will generate the simulating path for pacman
        while(successors):
            node, action = successors.pop(0)                                #BFS implements Queue Data Structure(FIFO) --> poping the first element from the list
            if (node.isWin()):                                              #condition if Pacman Reached Win state (virtually simulating path)
                win_states.append((scoreEvaluation(node),action))           #appending the win state and finding for more better win state
                #continue
            elif (node.isLose()):
                continue                                                    #eliminating the lose nodes
            #continue to find the legal action and the successor state till the win state is not reached
            else:
                legal = node.getLegalPacmanActions()
                for next_action in legal:
                    next_successor = node.generatePacmanSuccessor(next_action)
                    if (next_successor == None):                            #condition for checking the return state by generatePacmanSuccessor function 
                        scored.append((scoreEvaluation(node),action))
                    else:
                        successors.append((next_successor,action))          #If valid successor append it to the end of list, also Append the action of 1st parent(alternative to backtracing)

        
        if(win_states):
            bestScore = max(win_states)[0]
            for pair in win_states:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        #If not reaching a terminal state, return the action leading to the node with
        #the best score and no children based on the heuristic function (scoreEvaluation)
        elif(scored):
            bestScore = max(scored)[0]
            for pair in scored:
                if pair[0] == bestScore:
                    # returning the 1st best action
                    bestActions = pair[1]
                    break
            return bestActions
        else:
            return Directions.STOP
