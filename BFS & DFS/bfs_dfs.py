import sys
# BFS - Breadth First Algorithm
# DFS - Depth First Algorithm
print "Inplementing Breadth First Algorithm & Depth First Algorithm - Puzzle 8"
#incr_list =[]
goal_state = [0,1,2,3,4,5,6,7,8]

def puzzle_8_step(state):
    for i in range(0,9,3):
        print "-------------"
        print "|", state[i], "|", state[i+1], "|", state[i+2], "|"

    print "-------------"

def blank_tile_pos(state):
    pos = 0
    for i in range(9):
        if (state[i] == 0):
            pos = i
            return pos
    return pos

def move_up(pos,temp_state):
    print "Moving Up"
    new_state = temp_state[:]
    temp_element = new_state[pos]
    new_state[pos] = new_state[pos-3]
    new_state[pos-3] = temp_element
    
    return new_state

def move_down(pos,temp_state):
    print "Moving Down"
    new_state = temp_state[:]
    temp_element = new_state[pos]
    new_state[pos] = new_state[pos+3]
    new_state[pos+3] = temp_element
    
    return new_state

def move_left(pos,temp_state):
    print "Moving Left"
    new_state = temp_state[:]
    temp_element = new_state[pos]
    new_state[pos] = new_state[pos-1]
    new_state[pos-1] = temp_element
    
    return new_state

def move_right(pos,temp_state):
    print "Moving Right"
    new_state = temp_state[:]
    temp_element = new_state[pos]
    new_state[pos] = new_state[pos+1]
    new_state[pos+1] = temp_element
    
    return new_state

class Modules:
    
    def __init__(self,initial_state):
        self.initial_state = initial_state


    def bfs(self,start_state,goal_state):
        states_list =[]

        temp_list = start_state[:]
        print "Temp List", temp_list

        states_list.append(temp_list)
        print "States List",states_list 

        for next_state in range(50):

            not_found_state = states_list[next_state][:]
            print "Not Found State",not_found_state 

            puzzle_8_step(not_found_state)

            if (not_found_state == goal_state):
                print "Found"
                return

            

            blank_tile = blank_tile_pos(not_found_state)
            print "Blank Tile", blank_tile

            if (blank_tile > 2):
                new_state = move_up(blank_tile,not_found_state)
                states_list.append(new_state)
                print "Not Found State",not_found_state
                print states_list
                
            if (blank_tile < 6):
                new_state = move_down(blank_tile,not_found_state)
                states_list.append(new_state)
                print "Not Found State",not_found_state
                print states_list
                
                
            if (blank_tile != 0 or blank_tile != 3 or blank_tile!= 6):
                new_state = move_left(blank_tile,not_found_state)
                states_list.append(new_state)
                print "Not Found State",not_found_state
                print states_list
                
            if (blank_tile != 2 or blank_tile != 5 or blank_tile!= 8):
                new_state = move_right(blank_tile,not_found_state)
                states_list.append(new_state)
                print "Not Found State",not_found_state
                print states_list
    
def main(filename):
    initial_state = readfile(filename)
    print "---------------Initial State---------------"
    
    algorithm_call = Modules(initial_state)
    algorithm_call.bfs(initial_state,goal_state)
    

def readfile(filename):
    FILE_OBJECT = open(filename)
    data = FILE_OBJECT.read()
    start_state = []

    for i in range(len(data)):
        if (data[i] == "\n") or (data[i] == " "):
            pass
        else:
            start_state.append(int(data[i]))
    return start_state        


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print "Please input the start state filename as an argument", sys.exc_info()[0]
            

    
