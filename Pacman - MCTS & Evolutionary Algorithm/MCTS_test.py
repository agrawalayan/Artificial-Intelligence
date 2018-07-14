class Node():
    def __init__(self, state, parent = None, action = None):
        self.reward = []
        self.number_of_visit = []
        self.unexplored_actions = state.getLegalPacmanActions()
        self.parent = parent
        self.action = action

class MCTSAction(Agent)
    def __init__(self):
        self.RANDOM_ROLLOUT = 5
        self.CONSTANT = 1

    def registerInitialState(self, state):
        return

    def getAction(self, state):
        #legal_actions = state.getLegalPacmanActions()
        node = Node(state)
        self.forward_model = 1
        tempState = state
        while(self.forward_model != 0):
            next_node = self.tree_policy(node, state)
            delta = self.default_policy(next_node, state)
            self.backup(next_node, delta)

        return ()



    def tree_policy(self, node, state):
        while(self.forward_model != 0):
            if (node.unexplored_actions > 0):
                return self.expand(node, state)
            else:
                node = self.select(node)
        
        return node
                
                
    def expand(self, node, state):
        action = random.choice(node.unexplored_actions)
        child = state.generatePacmanSuccessor(action)
        node.unexplored_actions.pop(node.index(action))
        next_node = Node(child)
        next_node.unexplored_actions = child.getLegalPacmanActions()
        next_node.parent = node
        next_node.action = action
        return next_node

    def select(self, node, CONSTANT = 1):
        

    def default_policy(self, node, state):
        tempState = state
        back_actions = []
        while(node.parent != None):
            back_actions.append(node.action)
            node = node.parent
        for i in range(len(back_actions)):
            action = back_action.pop(-1)
            tempState = tempState.generatePacmanSuccessor(action)
        for i in range(self.RANDOM_ROLLOUT):
            legal_moves = tempState.getLegalPacmanActions()
            action = random.choice(legal_moves)
            tempState = tempState.generatePacmanSuccessor(action)
        reward = normalizedScoreEvaluation(tempState)
        return reward
            
    def backup(self, node, reward):
        while (node.parent != None):
            node.number_of_visit = node.number_of_visit + 1
            node.reward = node.reward + reward
            node = node.parent
        


