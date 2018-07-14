from Tkinter import *
from random import *

GRID_LAYOUT_BACK_FRAME = "#27354c"
EMPTY_CELL_LAYOUT = "#43ad7d"
NUMBER_TEXT_COLOR = {2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", 32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", 512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR = {2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2",32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2",512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"
FONT = ("Times New Roman", 40)
HEIGHT = 600
WIDTH = 600
ROW = 4
COLUMN = 4
#GLOBAL_LIST = [None]*(ROW*COLUMN)
PADDING = 2




class Game_2048(Frame):   # Frame is the base class

    def __init__(self):
        Frame.__init__(self) # Frame is the name of class and in that __init__ is the constructor
        self.grid()
        self.master.title("2048 Game")
        self.keyboard_keys = {KEY_UP : self.up , KEY_DOWN: self.down , KEY_LEFT: self.left , KEY_RIGHT : self.right}
        self.master.bind("<Key>", self.key)
        self.grid_numbers = []
        self.grid_layout()
        self.new_game()
        

        self.mainloop()

    def grid_layout(self):
        frame = Frame(master = None, bg = GRID_LAYOUT_BACK_FRAME, width = WIDTH, height = HEIGHT)
        frame.grid()

        for i in range(ROW):
            grid_row = []
            for j in range(COLUMN):
                cell = Frame(master = frame, bg = EMPTY_CELL_LAYOUT, width = WIDTH/ROW, height = HEIGHT/COLUMN)
                cell.grid(row = i, column = j, padx = PADDING, pady = PADDING)
                label = Label(master = cell, text="", bg=EMPTY_CELL_LAYOUT, justify=CENTER, font = FONT, width=4, height=2)
                label.grid()
                grid_row.append(label)
            self.grid_numbers.append(grid_row)

    def new_game(self):
        self.matrix = []
        for i in range(ROW):
                self.matrix.append([0]*COLUMN)
        self.start_game()
        self.display_board()

    def start_game(self):
        random_cell = randint(0, ROW*COLUMN - 1)
        row = random_cell/ROW
        column = random_cell%COLUMN
        self.matrix[row][column] = 2

    def key(self,event):
        self.key_pressed = repr(event.char)
        self.update_on_key_press()
    
    def update_on_key_press(self):
        self.add()
        

    def add(self):
        if self.key_pressed in self.keyboard_keys:
            self.matrix = self.keyboard_keys[self.key_pressed]()
            self.random_mat_generator()
            self.display_board()
            
        for i in range(ROW):
            for j in range(COLUMN):
                if (self.matrix[i][j] == 2048):
                    self.grid_numbers[0][0].configure(text="You", bg=EMPTY_CELL_LAYOUT)
                    self.grid_numbers[0][1].configure(text="WIN", bg=EMPTY_CELL_LAYOUT)
                    return
        

    def up(self):
        print "Up"
        shifted_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        row_count = [0]*ROW
        dummy_column = [0]*COLUMN
        shifting_done = [0]*COLUMN
        for i in range(ROW):
            for j in range(COLUMN):
                if (self.matrix[i][j] > 1):
                    count+=1
                    if (count == 1):
                        shifted_matrix[0][j] = self.matrix[i][j]
                        dummy_column[j] = 1
                        

                    if ((count > 1) and (dummy_column[j] == 1) and (shifting_done[j] == 0) and (shifted_matrix[row_count[j]][j] == self.matrix[i][j])):
                        shifted_matrix[row_count[j]][j] = shifted_matrix[row_count[j]][j] + self.matrix[i][j]
                        shifting_done[j] = 1

                    else:
                        if ((count > 1) and (dummy_column[j] == 1) and ((shifted_matrix[row_count[j]][j] != self.matrix[i][j]) or (shifting_done[j] == 1 and (shifted_matrix[row_count[j]][j] == self.matrix[i][j])))):
                            row_count[j] = row_count[j] + 1
                            shifted_matrix[row_count[j]][j] = self.matrix[i][j]

                    if ((count > 1) and (dummy_column[j] != 1)):
                        shifted_matrix[0][j] = self.matrix[i][j]
                        dummy_column[j] = 1
                    
        return shifted_matrix
                            
                        

    def down(self):
        print "Down"
        shifted_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        row_count = [ROW - 1]*ROW
        dummy_column = [0]*COLUMN
        shifting_done = [0]*COLUMN
        for i in range(ROW - 1, -1, -1):
            for j in range(COLUMN - 1, -1, -1):
                if (self.matrix[i][j] > 1):
                    count+=1
                    if (count == 1):
                        shifted_matrix[ROW - 1][j] = self.matrix[i][j]
                        dummy_column[j] = 1
                        

                    if ((count > 1) and (dummy_column[j] == 1) and (shifting_done[j] == 0) and(shifted_matrix[row_count[j]][j] == self.matrix[i][j])):
                        shifted_matrix[row_count[j]][j] = shifted_matrix[row_count[j]][j] + self.matrix[i][j]
                        shifting_done[j] = 1

                    else:
                        if ((count > 1) and (dummy_column[j] == 1) and ((shifted_matrix[row_count[j]][j] != self.matrix[i][j]) or (shifting_done[j] == 1 and (shifted_matrix[row_count[j]][j] == self.matrix[i][j])))):
                            row_count[j] = row_count[j] - 1
                            shifted_matrix[row_count[j]][j] = self.matrix[i][j]

                    if ((count > 1) and (dummy_column[j] != 1)):
                        shifted_matrix[ROW - 1][j] = self.matrix[i][j]
                        dummy_column[j] = 1
                    
        return shifted_matrix

        
    def left(self):
        print "Left"
        shifted_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        column_count = [0]*COLUMN
        dummy_column = [0]*ROW
        shifting_done = [0]*ROW
        for j in range(COLUMN):
            for i in range(ROW - 1, -1, -1):
                if (self.matrix[i][j] > 1):
                    count+=1
                    if (count == 1):
                        shifted_matrix[i][0] = self.matrix[i][j]
                        dummy_column[i] = 1
                        

                    if ((count > 1) and (dummy_column[i] == 1) and (shifting_done[i] == 0) and(shifted_matrix[i][column_count[i]] == self.matrix[i][j])):
                        shifted_matrix[i][column_count[i]] = shifted_matrix[i][column_count[i]] + self.matrix[i][j]
                        shifting_done[i] = 1

                    else:
                        if ((count > 1) and (dummy_column[i] == 1) and ((shifted_matrix[i][column_count[i]] != self.matrix[i][j]) or (shifting_done[i] == 1 and (shifted_matrix[i][column_count[i]] == self.matrix[i][j])))):
                            column_count[i] = column_count[i] + 1
                            shifted_matrix[i][column_count[i]] = self.matrix[i][j]

                    if ((count > 1) and (dummy_column[i] != 1)):
                        shifted_matrix[i][0] = self.matrix[i][j]
                        dummy_column[i] = 1
                    
        return shifted_matrix

        
    def right(self):
        print "Right"
        shifted_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        column_count = [COLUMN - 1]*COLUMN
        dummy_column = [0]*ROW
        shifting_done = [0]*ROW
        for j in range(COLUMN - 1, -1, -1):
            for i in range(ROW):
                if (self.matrix[i][j] > 1):
                    count+=1
                    if (count == 1):
                        shifted_matrix[i][COLUMN - 1] = self.matrix[i][j]
                        dummy_column[i] = 1
                        

                    if ((count > 1) and (dummy_column[i] == 1) and (shifting_done[i] == 0) and(shifted_matrix[i][column_count[i]] == self.matrix[i][j])):
                        shifted_matrix[i][column_count[i]] = shifted_matrix[i][column_count[i]] + self.matrix[i][j]
                        shifting_done[i] = 1

                    else:
                        if ((count > 1) and (dummy_column[i] == 1) and ((shifted_matrix[i][column_count[i]] != self.matrix[i][j]) or (shifting_done[i] == 1 and (shifted_matrix[i][column_count[i]] == self.matrix[i][j])))):
                            column_count[i] = column_count[i] - 1
                            shifted_matrix[i][column_count[i]] = self.matrix[i][j]

                    if ((count > 1) and (dummy_column[i] != 1)):
                        shifted_matrix[i][COLUMN - 1] = self.matrix[i][j]
                        dummy_column[i] = 1
                    
        return shifted_matrix

    def random_mat_generator(self):
        random_cell = randint(0, ROW*COLUMN - 1)
        row = random_cell/ROW
        column = random_cell%COLUMN
        if self.matrix[row][column] == 0:
            self.matrix[row][column] = 2
        else:
            for i in range(ROW):
                for j in range(COLUMN):
                    if self.matrix[i][j] == 0:
                        self.random_mat_generator()
                        return
                        

    def display_board(self):
        for i in range(ROW):
            for j in range(COLUMN):
                cell_number = self.matrix[i][j]
                if cell_number == 0:
                    self.grid_numbers[i][j].configure(text="", bg=EMPTY_CELL_LAYOUT)
                else:
                    self.grid_numbers[i][j].configure(text=str(cell_number), bg=CELL_COLOR[cell_number], fg = NUMBER_TEXT_COLOR[cell_number])


playgame = Game_2048()
