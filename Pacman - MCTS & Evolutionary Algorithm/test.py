class Node():
    def __init__(self, state, parent = None):
        self.visit = 1
        self.reward = 0
        self.legal_actions = []
        self.state = state
        self.parent = parent
    def getLegalMoves(self):
        print "hi"
    def child(self, child_state):
        child = Node(child_state, self)
        print self.parent

        
class MCTSAgent():
    # Initialization Function: Called one time when the game starts
    def __init__(self):
        self.RANDOM_ROLLOUT = 5

    def registerInitialState(self, state):
        
        return;

    
    def getAction(self, state):
    # GetAction Function: Called with every frame
        node = Node(state)
        print node.visit 
        forward_model = 1
        node.getLegalMoves()
        #node.child(node,2)
        print node
        #while (forward_model != 0):
         #   next_node = self.tree_policy(node)


if __name__ == "__main__":
    mcts = MCTSAgent()
    mcts.getAction(4)
