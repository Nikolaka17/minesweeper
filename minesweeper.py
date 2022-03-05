import random
import sys

"""TODO:
        Add pygame ui
        Add computer vision functionality
        Implement more solving algorithms
"""
#class for game to take place
class field:
    #constructor
    def __init__(self, size=10, bombs=10, mode = "auto"):
        #sets attributes
        self.size = size
        self.bombs = bombs
        self.working = [] #what is know of the field
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(-2)
            self.working.append(temp)
        self.answer = self.working #the entirety of the field
        self.counter = 0 #checks for a stalemate where the rules don't work
        self.map = [] #map of the probability of each square being a bomb
        for i in range(size):
            holder = []
            for j in range(size):
                holder.append(1)
            self.map.append(holder)

        #places bombs on board
        bomb_locations = []
        while (len(bomb_locations) < self.bombs):
            x = random.randint(0,9)
            y = random.randint(0,9)
            if not ([y,x] in bomb_locations):
                bomb_locations.append([y,x])
        for bomb in bomb_locations:
            self.answer[bomb[0]][bomb[1]] = -1

        #places numbers on non bomb spaces
        for row in range(len(self.answer)):
            for column in range(len(self.answer)):
                if self.answer[row][column] != -1:
                    surrounding = find_around(row, column, self.answer)
                    self.answer[row][column] = surrounding.count(-1)
        
        #make action based off of mode
        if mode == "auto":
            auto()
        elif mode == "manual":
            manual()
        elif mode == "cv":
            pass


        #update probability of each square
        def update_prob_map(self):
            for y in range(self.size):
                for x in range(self.size):
                    if self.working[y][x] != -1 and self.working[y][x] != -2 and self.working[y][x] != 0:
                        around = find_around(y,x,self.working)
                        around_chord = [y,x,self.working]
                        val = (self.working[y][x]-around.count(-1))/(around.count(-2))
                        for i in range(len(around)):
                            if around[i] == -2:
                                self.map[around_chord[i][0]][around_chord[i][1]] *= val
                    else:
                        self.map[y][x] = 1
        

        #finds values of adjacent squares
        def find_around(self,y, x, board):
            result = []
            if not(y == 0):
                if not(x == 0):
                    result.append(board[y-1][x-1])
                if not(x == len(board)-1):
                    result.append(board[y-1][x+1])
                result.append(board[y-1][x])
            if not(y==len(board )-1):
                if not(x==0):
                    result.append(board[y+1][x-1])
                if not(x==len(board)-1):
                    result.append(board[y+1][x+1])
                result.append(board[y+1][x])
            if not(x==0):
                result.append(board[y][x-1])
            if not(x==len(board)-1):
                result.append(board[y][x+1])
            return result


        #find chords of all adjacent squares
        def find_around_chords(self,y, x, board):
            result = []
            if not(y == 0):
                if not(x == 0):
                    result.append([y-1,x-1])
                if not(x == len(board)-1):
                    result.append([y-1,x+1])
                result.append([y-1,x])
            if not(y==len(board )-1):
                if not(x==0):
                    result.append([y+1,x-1])
                if not(x==len(board)-1):
                    result.append([y+1,x+1])
                result.append([y+1,x])
            if not(x==0):
                result.append([y,x-1])
            if not(x==len(board)-1):
                result.append([y,x+1])
            return result


        #applies rules of the game to quares
        def work_space(self,y,x):
            around_chords = find_around_chords(y,x, self.working)
            around = find_around(y,x,self.working)

            #if all the mines around it are flagged, dig remaining surrounding squares
            if self.working[y][x] == around.count(-1):
                for space in around_chords:
                    if self.working[space[0]][space[1]] == -2:
                        dig(space[0], space[1]) 
                self.counter = 0

            #if the square has the same amount of bombs remaining around it as undug spaces, flag remaining surrounding squares
            if around.count(-2) == self.working[y][x] - around.count(-1):
                for i in range(len(around)):
                    if around[i] == -2:
                        flag(around_chords[i][0], around_chords[i][1])
                self.counter = 0


        #dig at the space provided
        def dig(self,y,x):
            if self.working[y][x] == -2:
                self.working[y][x] = self.answer[y][x]
                if self.working[y][x] == 0:
                    for space in find_around_chords(y,x):
                        dig(space[0],space[1])
                print(self)
                if self.working[y][x] == -1:
                    end()
        

        #what the computer does to auto solve the game
        def auto(self):
            while True:
                for row in self.working:
                    for column in self.working:
                        work_space(row, column)
                        self.counter += 1
                full = []
                for lst in self.working:
                    for item in row:
                        full.append[item]
                if full.count(-1) == self.bombs:
                    for i in range(self.size):
                        for j in range(self.size):
                            if self.working[i][j] == -2:
                                dig(i,j)
                if self.counter >= len(self.working ** 2): #sees if rules don't work for any square
                    update_prob_map()
                    lowest_chord = [0,0]
                    for y in range(self.size):
                        for x in range(self.size):
                            if self.working[y][x] == -2:
                                if self.map[y][x] < self.map[lowest_chord[0],lowest_chord[1]]:
                                    lowest_chord = [y,x]
                    dig(lowest_chord[0],lowest_chord[1])
                check_win()
        

        #allows the user to play themselves
        def manual(self):
            print(self)
            move_type = ""
            while True:
                move_type = ""
                while move_type != "1" and move_type != "2" and move_type != "dig" and move_type != "flag":
                    move_type = str(input("What would you like to do?\n1. dig\n2. flag\n"))
                move_x = ""
                while move_x not in str(range(self.size + 1)):
                    move_x = str(input("What is the x position of the space? (pick a number between 1 and %s)\n"%(str(self.size))))
                move_y = ""
                while move_y not in str(range(self.size + 1)):
                    move_y = str(input("What is the y position of the space? (pick a number between 1 and %s)\n"%(str(self.size))))
                if move_type == "1" or move_type == "dig":
                    dig(int(move_y)-1, int(move_x)-1)
                if move_type == "2" or move_type == "flag":
                    flag(int(move_y)-1, int(move_x)-1)


        #flag at the space given
        def flag(self,y,x):
            if self.working[y][x] == -1:
                unflag(y,x)
            else:
                all = []
                for lst in self.working:
                    for value in lst:
                        all.append(value)
                if all.count(-1) != self.bombs:
                    self.working[y][x] = -1
                    print(self)
                else:
                    print("Out of flags")

     
        #remove flag from space given
        def unflag(self, y, x):
            if self.working[y][x] == -1:
                self.working[y][x] = -2
                print(self)
            else:
                print("no flag at position")


        #sets up the array for printing
        def __repr__(self):
            prn = ""
            new_list = []
            for i in range(len(self.working)):
                temp = []
                for val in self.working[i]:
                    if val == -2:
                        temp.append("-")
                    elif val == -1:
                        temp.append("*")
                    elif val == 0:
                        temp.append(" ")
                    else:
                        temp.append(str(val))
                new_list.append(temp)
            for val in new_list:
                for var in val:
                    prn += var
                    prn += " "
            return prn


        #find squares that are -2
        def find_undug(self):
            result = []
            for row in self.working:
                for column in self.working:
                    if self.working[row][column] == -2:
                        result.append([row,column])
            return result


        #checks if the game is won
        def check_win(self):
            all = []
            for lst in self.working:
                for value in lst:
                    all.append(value)
            if -2 not in all:
                win()


        #what to do if the game is won
        def win(self):
            print("Game won, congrats")
            sys.exit()
        

        #what to do if the game is lost
        def end(self):
            print("Mine dug, game over.")
            sys.exit()