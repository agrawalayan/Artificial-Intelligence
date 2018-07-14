import sys
# BFS - Breadth First Algorithm
# DFS - Depth First Algorithm
print "Inplementing Breadth First Algorithm & Depth First Algorithm - Puzzle 8"
#incr_list =[]
goal_state = [3,0,2,6,1,7,4,8,5]

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
    temp_element = temp_state[pos]
    temp_state[pos] = temp_state[pos-3]
    temp_state[pos-3] = temp_element

    return temp_state

def move_down(pos,temp_state):
    temp_element = temp_state[pos]
    temp_state[pos] = temp_state[pos+3]
    temp_state[pos+3] = temp_element
    return temp_state

def move_left(pos,temp_state):
    temp_element = temp_state[pos]
    temp_state[pos] = temp_state[pos-1]
    temp_state[pos-1] = temp_element
    return temp_state

def move_right(pos,temp_state):
    temp_element = temp_state[pos]
    temp_state[pos] = temp_state[pos+1]
    temp_state[pos+1] = temp_element
    return temp_state

class Modules:
    
    def __init__(self,initial_state):
        self.initial_state = initial_state


    def bfs(self,start_state,goal_state):
        temp_list = []
        temp_list.append(start_state)
        
        for next_state in range(2):
            
            puzzle_8_step(temp_list[next_state])

            if (temp_list[next_state] == goal_state):
                print "Found"
                return

            not_found_state = temp_list[next_state][:]

            blank_tile = blank_tile_pos(not_found_state)

            if (blank_tile > 2):
                new_state = move_up(blank_tile,not_found_state)
                temp_list.append(new_state)
                print "Not Found State",not_found_state
                print temp_list
                
            if (blank_tile < 6):
                new_state = move_down(blank_tile,not_found_state)
                temp_list.append(new_state)
                print "Not Found State",not_found_state
                print temp_list
                
                
            if (blank_tile != 0 or blank_tile != 3 or blank_tile!= 6):
                new_state = move_left(blank_tile,not_found_state)
                temp_list.append(new_state)
                print "Not Found State",not_found_state
                print temp_list
                
            if (blank_tile != 2 or blank_tile != 5 or blank_tile!= 8):
                new_state = move_right(blank_tile,not_found_state)
                temp_list.append(new_state)
                print "Not Found State",not_found_state
                print temp_list
    
def main(filename):
    initial_state = readfile(filename)
    print "---------------Initial State---------------"
    
    algorithm_call = Modules(initial_state)
    start_state = readfile(filename)
    algorithm_call.bfs(start_state,goal_state)
    

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
            

    
