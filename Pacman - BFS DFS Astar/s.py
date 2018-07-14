class BFSAgent():
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, i = 1):
        while(1):
            if (i == 1):
                print "Hello"
                i = 2
            else:
                print "Bye"
                self.getAction()

agent = BFSAgent()
agent.getAction()
                
