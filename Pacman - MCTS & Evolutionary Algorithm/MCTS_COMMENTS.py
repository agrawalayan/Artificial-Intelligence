
'''
class Node():
    def __init__(self, state, parent = None):
        self.visit = 0
        self.reward = 0
        self.legal_actions = []
        self.state = state
        self.parent = parent
        self.children = []
        self.forward_model = 1
        
    def getLegalMoves(self):
        self.legal_actions = self.state.getLegalPacmanActions()
        return self.legal_actions

    def getChildren(self, action):
        
        #self.children = []
        while (self.forward_model != 0):
            child = self.state.generatePacmanSuccessor(actions)
            if (child == None):
                self.forward_model = 0
                break
            elif(child.isWin()):
                break
            elif(child.isLose()):
                break
            else:
                self.children.append((child,actions))

                
                




            
class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def __init__(self):
        self.RANDOM_ROLLOUT = 5

    def registerInitialState(self, state):
        return;

    def getAction(self, state):
    # GetAction Function: Called with every frame
        node = Node(state)
        forward_model = 1
        tempState = state
        while (forward_model != 0):
            tempNode = Node(tempState)
            next_node = self.tree_policy(tempNode)
            if (next_node == None):
                forward_model = 0
                break
   
    def tree_policy(node):
	while node.forward_model == 1:
            legal_actions = node.getLegalMoves()
	    if (legal_actions):
		next_node = self.expand(node, legal_actions)
		legal_actions.pop(0)
		return next_node
	    elif random.uniform(0,1)<.5:
		node=BESTCHILD(node,SCALAR)
	    else:
		if node.fully_expanded()==False:	
		    return EXPAND(node)
		else:
		    node=BESTCHILD(node,SCALAR)
	return node

    def expand(node, legal_actions):
	node.getChildren(legal_actions[0])
	new_state=node.state.next_state()
	while new_state in tried_children:
		new_state=node.state.next_state()
	node.add_child(new_state)
	return node.children[-1]
'''
            '''
            legal_actions = tempNode.getLegalMoves()
            for actions in legal_actions:
                child = self.state.generatePacmanSuccessor(actions)
                if (child == None):
                    forward_model = 0
                    break
                elif(child.isWin()):
                    break
                elif(child.isLose()):
                    break
                else:
                    self.children.append((child,actions))
            if (forward_model == 0):
                break
            '''
    
        
    '''

    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        forward_model = 1
        
        while(forward_model != 0):
            state_selection = []
            successors = []                                         #successors is tuple of (state,action,Q,n,legal_actions,index_to_visit)
            legal_actions = state.getLegalPacmanActions()
            for action in legal:
                successors.append((state.generatePacmanSuccessor(action),action))
            for states,action in range(len(successors)):
                tempState = states
                for i in range(self.RANDOM_ROLLOUT):
                    next_actions = tempState.getLegalPacmanActions()
                    tempState = tempState.generatePacmanSuccessor(next_actions[random.randint(0,len(next_actions)-1)])
                score_check = scoreEvaluation(tempState)
                state_selection.append((states, action, self.UCT_formula(score_check), 1, legal_actions = [], index_to_visit = 0))

    return states from states_selection(max(state_selection[2]))
    
    def UCT_formula(self,score_check)






    class State():
	NUM_TURNS = 10	
	GOAL = 0
	MOVES=[2,-2,3,-3]
	MAX_VALUE= (5.0*(NUM_TURNS-1)*NUM_TURNS)/2
	num_moves=len(MOVES)
	def __init__(self, value=0, moves=[], turn=NUM_TURNS):
		self.value=value
		self.turn=turn
		self.moves=moves
	def next_state(self):
		nextmove=random.choice([x*self.turn for x  in self.MOVES])
		next=State(self.value+nextmove, self.moves+[nextmove],self.turn-1)
		return next
	def terminal(self):
		if self.turn == 0:
			return True
		return False
	def reward(self):
		r = 1.0-(abs(self.value-self.GOAL)/self.MAX_VALUE)
		return r
	def __hash__(self):
		return int(hashlib.md5(str(self.moves).encode('utf-8')).hexdigest(),16)
	def __eq__(self,other):
		if hash(self)==hash(other):
			return True
		return False
	def __repr__(self):
		s="Value: %d; Moves: %s"%(self.value,self.moves)
		return s
	

class Node():
	def __init__(self, state, parent=None):
		self.visits=1
		self.reward=0.0	
		self.state=state
		self.children=[]
		self.parent=parent	
	def add_child(self,child_state):
		child=Node(child_state,self)
		self.children.append(child)
	def update(self,reward):
		self.reward+=reward
		self.visits+=1
	def fully_expanded(self):
		if len(self.children)==self.state.num_moves:
			return True
		return False
	def __repr__(self):
		s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)
		return s
		


def UCTSEARCH(budget,root):
	for iter in range(int(budget)):
		if iter%10000==9999:
			logger.info("simulation: %d"%iter)
			logger.info(root)
		front=TREEPOLICY(root)
		reward=DEFAULTPOLICY(front.state)
		BACKUP(front,reward)
	return BESTCHILD(root,0)

def TREEPOLICY(node):
	#a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
	while node.state.terminal()==False:
		if len(node.children)==0:
			return EXPAND(node)
		elif random.uniform(0,1)<.5:
			node=BESTCHILD(node,SCALAR)
		else:
			if node.fully_expanded()==False:	
				return EXPAND(node)
			else:
				node=BESTCHILD(node,SCALAR)
	return node

def EXPAND(node):
	tried_children=[c.state for c in node.children]
	new_state=node.state.next_state()
	while new_state in tried_children:
		new_state=node.state.next_state()
	node.add_child(new_state)
	return node.children[-1]

#current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
def BESTCHILD(node,scalar):
	bestscore=0.0
	bestchildren=[]
	for c in node.children:
		exploit=c.reward/c.visits
		explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))	
		score=exploit+scalar*explore
		if score==bestscore:
			bestchildren.append(c)
		if score>bestscore:
			bestchildren=[c]
			bestscore=score
	if len(bestchildren)==0:
		logger.warn("OOPS: no best child found, probably fatal")
	return random.choice(bestchildren)

def DEFAULTPOLICY(state):
	while state.terminal()==False:
		state=state.next_state()
	return state.reward()

def BACKUP(node,reward):
	while node!=None:
		node.visits+=1
		node.reward+=reward
		node=node.parent
	return

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='MCTS research code')
	parser.add_argument('--num_sims', action="store", required=True, type=int)
	parser.add_argument('--levels', action="store", required=True, type=int, choices=range(State.NUM_TURNS))
	args=parser.parse_args()
	
	current_node=Node(State())
	for l in range(args.levels):
		current_node=UCTSEARCH(args.num_sims/(l+1),current_node)
		print("level %d"%l)
		print("Num Children: %d"%len(current_node.children))
		for i,c in enumerate(current_node.children):
			print(i,c)
		print("Best Child: %s"%current_node.state)
		
		print("--------------------------------")	
        
    '''


'''



