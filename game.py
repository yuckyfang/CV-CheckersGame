import numpy as np
from numpy import *
import cv2
import random
from copy import deepcopy
import matplotlib.pyplot as plt

def getPositions():
     
    #reads image and gets w x h 
#     fname = input('pic?')
#     fname = 'checkerboardWPieces5.jpg'
    fname = str(input("file name?"))
    img = cv2.imread(fname)
#     plt.imshow(img)
    width, height = img.shape[:2]
#     print(width, height) 
     
    num_grids = 6
     
    #detect red in image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)       
    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)  
    # upper mask (170-180)
    lower_red = np.array([160,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red) 
    # join my masks
    mask = (mask0+mask1)/2
    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    #cv2.imshow('hsv1', output_img)
    # or your HSV image
#     output_hsv = hsv.copy()
#     output_hsv[np.where(mask==0)] = 0
#     cv2.imshow('hsv', output_hsv)
     
    #store red circles, green circles, and blank spaces in matrix 
    img1 = cv2.medianBlur(output_img,5)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)    
    circles1 = cv2.HoughCircles(gray1, cv2.HOUGH_GRADIENT, 1, 1, param1 = 30, param2 =width/num_grids-18, minRadius=8, maxRadius=22)
    circles1 = np.uint16(np.around(circles1))
    #print(circles)
    red_piece_centroids = [] #stores center of each detected circle 
    for i in circles1[0,:]:
        cv2.circle(img1, (i[0], i[1]), i[2], (0,255,0),2) #draw outer circle 
        cv2.circle(img1, (i[0], i[1]), 2, (0,255,0),3) #draws center of circle
        red_piece_centroids.append((i[0], i[1]))
#     print(red_piece_centroids)
     
     
    '''#draws horizontal and vertical lines
    lineThickness = 3
    for i in range(0,num_grids+1):
        cv2.line(img, (int(width/num_grids)*i, height), (int(width/num_grids)*i, 0), (0,255,0), lineThickness)
        cv2.line(img, (0, int(height/num_grids)*i), (width, int(height/num_grids)*i), (0, 255, 0), lineThickness)
    plt.imshow(img) 
    plt.show()
    '''
     
    #before I learned to use matrices 
    #stores bottom left corner of each grid 
    col_corners=[]
    row_corners=[]
    for i in range(7):
        col_corners.append(width/num_grids*i)
        row_corners.append(height/num_grids*i)
    #print(col_corners)
    corners=[]
    for r in range(len(row_corners)):
        for c in range(len(col_corners)):
            corners.append((col_corners[c], row_corners[r]))
    #print(corners)
     
      
    #stores center point of grids
    center_points = []
    for row in range(len(row_corners)-1):
        for col in range(len(col_corners)-1):
            midpt_r = (row_corners[col]+row_corners[col+1])/2
            midpt_c = (col_corners[row]+col_corners[row+1])/2
             
            center_points.append((midpt_r, midpt_c))
    #print(center_points)
     
    #returns image of detected circles     
    img = cv2.medianBlur(img,5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 1, param1 = 30, param2 =width/num_grids-18, minRadius=8, maxRadius=22)
    circles = np.uint16(np.around(circles))
    #print(circles)
    piece_centroids = [] #stores center of each detected circle 
    for i in circles[0,:]:
        cv2.circle(img, (i[0], i[1]), i[2], (0,255,0),2) #draw outer circle 
        cv2.circle(img, (i[0], i[1]), 2, (0,255,0),3) #draws center of circle
        piece_centroids.append((i[0], i[1]))
#     print(piece_centroids)
     
    #after I learned matrices 
    #returns an array of 1s and 0s indicating current positions
    current_positions = []
    for i in range(len(center_points)):
        current_positions.append(-1)    
        for c in piece_centroids:
            diff_x = abs(center_points[i][0]-c[0])
            diff_y = abs(center_points[i][1]-c[1])
            #checks if there's a checker piece there 
            if diff_x < 10 and diff_y < 10:
                current_positions[i]=1
            for j in red_piece_centroids:
                diff_redx = abs(c[0] - j[0] * 1.0)
#                 print(diff_redx)
                diff_redy = abs(c[1] - j[1] * 1.0)
#                 print(diff_redy)
                #checks whether it's a red piece 
                if diff_redx < 10 and diff_redy <10 and diff_x <10 and diff_y <10: #diff might be diff when using 8 x 8  
                    current_positions[i]=0
                    break
    matrix = np.reshape(current_positions, (num_grids,num_grids))
#     print(matrix)
     
#     cv2.imshow('red',img1)
#     cv2.imshow('detected circles', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
     
    return matrix


BOARD_SIZE = 6

NUM_PLAYERS = 6

DEPTH_LIMIT = 7

# the players array extends to many other arrays in the program

# in these arrays, 0 will refer to black and 1 to white

PLAYERS = ["You", "Frankie"]



class Game:

    def __init__(self, player=0):
        
        self.board = Board()
        
        
        
        # refers to how many pieces that play

        self.remaining = [NUM_PLAYERS, NUM_PLAYERS]

        # default player is black

        self.player = player

        self.turn = 0

    def run(self):

        while not (self.gameOver(self.board)):
            

            self.board.drawBoardState()

            print("Current Player: "+PLAYERS[self.turn])

            if (self.turn == self.player):

                # get player's move
                if self.turn==0:
                    self.board.setDefaultBoard()
    #                 self.boardState = getPositions()
    #                 self.board = self.boardState
                    self.board.drawBoardState()
                    self.turn = 1
                    
                if self.turn ==1:
#                     legal = self.board.calcLegalMoves(self.turn) #returns array of legal moves 
#                     if (len(legal) > 0):
#     
#                 #        choice = random.randint(0,len(legal)-1)
#     
#                 #        move = legal[choice]
#     
#                         move = self.getMove(legal)
#                         
#     
#                         self.makeMove(move)
#                         legal = self.board.calcLegalMoves(self.turn)
# 
# 
#                     print("Valid Moves: ")
#     
#                     for i in range(len(legal)):
#     
#                         print(str(i+1)+": ",end='')
#     
#                         print(str(legal[i].start)+" "+str(legal[i].end))
#                         
#                     
#     
#                     if (len(legal)>0):
#     
#                         # no need for AI if there's only one choice!
#     
#                         if (len(legal)==1):
#     
#                             choice = legal[0]
#     
#                         else:
    
                            state = AB_State(self.board, self.turn, self.turn)
    
    
                            choice = self.alpha_beta(state)
    
    
                            self.makeMove(choice)
    
    
                            print("Computer chooses ("+str(choice.start)+", "+str(choice.end)+")")
    
                # switch player after move
        

           

                

                            self.turn = 1-self.turn

        print("Game OVER")

        print("You Captured: "+str(NUM_PLAYERS-self.remaining[1]))

        print("Frankie Captured: "+str(NUM_PLAYERS-self.remaining[0]))

        score = self.calcScore(self.board)

        print("Your Score: "+str(score[0]))

        print("Frankie's Score: "+str(score[1]))

        if (score[0] > score[1]):

              print("You win!")

        elif (score[1] > score[0]):

              print("Frankie wins!")

        else:

            print("It's a tie!")

        self.board.drawf()



    def makeMove(self, move):



        self.board.boardMove(move, self.turn)

        if move.jump:

            # decrement removed pieces after jump

            self.remaining[1-self.turn] -= len(move.jumpOver)

            print("Removed "+str(len(move.jumpOver))+" "+PLAYERS[1-self.turn]+" pieces")

  

    def getMove(self, legal):

        move = -1

        # repeats until player picks move on the list

        while move not in range(len(legal)):

            # List valid moves:

            print("Valid Moves: ")

            for i in range(len(legal)):

                print(str(i+1)+": ",end='')

                print(str(legal[i].start)+" "+str(legal[i].end))

            usr_input = input("Pick a move: ")

            # stops error caused when user inputs nothing

            move = -1 if (usr_input == '')  else (int(usr_input)-1)

            if move not in range(len(legal)):

                print("Illegal move")

        print("Legal move")

        return (legal[move])

        

    # returns a boolean value determining if game finished

    def gameOver(self, board):

        # all pieces from one side captured

        if (len(board.currPos[0]) == 0 or len(board.currPos[1]) == 0):

            return True

        # no legal moves available, stalemate

        elif (len(board.calcLegalMoves(0)) == 0 and len(board.calcLegalMoves(1)) == 0):

            return True

        else:

            # continue onwards

            return False

            

    #calculates the final score for the board

    def calcScore(self, board):

        score = [0,0]

        # black pieces

        for cell in range(len(board.currPos[0])):

            # black pieces at end of board - 2 pts

            if (board.currPos[0][cell][0] == 0):

                score[0] += 2

            # black pieces not at end - 1 pt

            else:

                score[0] += 1

        # white pieces

        for cell in range(len(board.currPos[1])):

            # white pieces at end of board - 2 pts

            if (board.currPos[1][cell][0] == BOARD_SIZE-1):

                score[1] += 2

            # white pieces not at end - 1 pt

            else:

                score[1] += 1

        return score

        

    # state = board, player

    def alpha_beta(self, state):

        result = self.max_value(state, -999, 999, 0)

        print("Total nodes generated: "+str(result.nodes))

        print("Max depth: "+str(result.max_depth))

        print("Max Val Cutoffs: "+str(result.max_cutoff))

        print("Min Val Cutoffs: "+str(result.min_cutoff))

        return result.move

   

   # returns max value and action associated with value

    def max_value(self, state, alpha, beta, node):

      # if terminalTest(state)

      actions = state.board.calcLegalMoves(state.player)

      num_act = len(actions)

      # v <- -inf

      # self, move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff

      v = AB_Value(-999, None, node, 1, 0, 0)

      # depth cutoff

      if (node == DEPTH_LIMIT):

         v.move_value = self.evaluation_function(state.board, state.origPlayer)

   #      print("Depth Cutoff. Eval value: "+str(v.move_value))

         return v      

      if (len(actions)==0):

         # return Utility(state)

         score = self.calcScore(state.board)

         if (score[state.origPlayer] > score[1-state.origPlayer]):

            v.move_value = 100 + (2*score[state.origPlayer]-score[1-state.origPlayer])

   #         print("(max) Terminal Node Score: "+str(v.move_value))

         else:

            v.move_value = -100 + (2*score[state.origPlayer]-score[1-state.origPlayer])

   #         print("(max) Terminal Node Score: "+str(v.move_value))            

         return v

      for a in actions:

         newState = AB_State(deepcopy(state.board), 1-state.player, state.origPlayer)

         # RESULT(s,a)

         newState.board.boardMove(a, state.player)

         new_v = self.min_value(newState, alpha, beta, node+1)

         # compute new values for nodes and cutoffs in recursion

         if (new_v.max_depth > v.max_depth):

             v.max_depth = new_v.max_depth         

         v.nodes += new_v.nodes

         v.max_cutoff += new_v.max_cutoff

         v.min_cutoff += new_v.min_cutoff

         # v <- Max(v, MIN_VALUE(RESULT(s,a), alpha, beta))

         if (new_v.move_value > v.move_value):

            v.move_value = new_v.move_value

            v.move = a

         if (v.move_value >= beta):

            v.max_cutoff += 1

            return v

         if (v.move_value > alpha):

            alpha = v.move_value

      return v



   # returns min value

    def min_value(self, state, alpha, beta, node):

      #if terminalTest(state)

      actions = state.board.calcLegalMoves(state.player)

      num_act = len(actions)

      # v <- inf

      # self, move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff

      v = AB_Value(999, None, node, 1, 0, 0)

      # depth cutoff

      if (node == DEPTH_LIMIT):

         v.move_value = self.evaluation_function(state.board, state.player)

   #      print("Depth Cutoff. Eval value: "+str(v.move_value))

         return v

      if (len(actions)==0):

         # return Utility(state)

         score = self.calcScore(state.board)

         if (score[state.origPlayer] > score[1-state.origPlayer]):

            v.move_value = 100 + (2*score[state.origPlayer]-score[1-state.origPlayer])

    #        print("(min) Terminal Node Score: "+str(v.move_value))            

         else:

            v.move_value = -100 + (2*score[state.origPlayer]-score[1-state.origPlayer])

    #        print("(min) Terminal Node Score: "+str(v.move_value))

         return v     

      for a in actions:

         newState = AB_State(deepcopy(state.board), 1-state.player, state.origPlayer)

         eval = self.evaluation_function(self.board, self.turn)

    #     print("Current Evaluation: "+str(eval))

         # RESULT(s,a)

         newState.board.boardMove(a, state.player)

         new_v = self.max_value(newState, alpha, beta, node+1)

         # compute new values for nodes and cutoffs in recursion

         if (new_v.max_depth > v.max_depth):

             v.max_depth = new_v.max_depth

         v.nodes += new_v.nodes

         v.max_cutoff += new_v.max_cutoff

         v.min_cutoff += new_v.min_cutoff

         # v <- Min(v, MAX_VALUE(RESULT(s,a), alpha, beta))

         if (new_v.move_value < v.move_value):

            v.move_value = new_v.move_value

            v.move = a

         if (v.move_value <= alpha):

            v.min_cutoff += 1

            return v

         if (v.move_value < beta):

            beta = v.move_value

      return v



    # returns a utility value for a non-terminal node

    # f(x) = 5(player piece in end)+3(player not in end)-7(opp in end)-3(opp not in end)

    def evaluation_function(self, board, currPlayer):

        blk_far, blk_home_half, blk_opp_half = 0,0,0

        wt_far, wt_home_half, wt_opp_half = 0,0,0 

        # black's pieces

        for cell in range(len(board.currPos[0])):

            # player pieces at end of board

            if (board.currPos[0][cell][0] == BOARD_SIZE-1):

                blk_far += 1

            # player pieces in opponents end

            # change to "print 'yes' if 0 < x < 0.5 else 'no'"

            elif (BOARD_SIZE/2 <= board.currPos[0][cell][0] < BOARD_SIZE):

                blk_opp_half += 1

            else:

                blk_home_half += 1

        # white's pieces

        for cell in range(len(board.currPos[1])):

            # opp pieces at end of board 

            if (board.currPos[1][cell][0] == 0):

                wt_far += 1

            # opp pieces not at own end

            elif (0 <= board.currPos[1][cell][0] < BOARD_SIZE/2):

                wt_opp_half += 1

            else:

                wt_home_half += 1

        white_score = (7 * wt_far) + (5 * wt_opp_half)+ (3 * wt_home_half)

        black_score = (7 * blk_far) + (5 * blk_opp_half)+ (3 * blk_home_half)

        if (currPlayer == 0):

            return (black_score - white_score)

        else:

            return (white_score - black_score)       

                 

# wrapper for alpha-beta info

# v = [move_value, move, max tree depth, # child nodes, # max/beta cutoff, # min/alpha cutoff]

class AB_Value:

    def __init__(self, move_value, move, max_depth, child_nodes, max_cutoff, min_cutoff):

        self.move_value = move_value

        self.move = move

        self.max_depth = max_depth

        self.nodes = child_nodes

        self.max_cutoff = max_cutoff

        self.min_cutoff = min_cutoff

         



# wrapper for state used in alpha-beta

class AB_State:

   def __init__(self, boardState, currPlayer, originalPlayer):

      self.board = boardState

      self.player = currPlayer

      self.origPlayer = originalPlayer

      

class Move:

    def __init__(self, start, end, jump=False):

            self.start = start

            self.end = end # tuple (row, col)

            self.jump = jump # bool

            self.jumpOver = [] # array of pieces jumped over

    

class Board:

    def __init__(self, board=[], currBlack=[], currWhite=[]):

        if (board!=[]):

            self.boardState = board     

        else:

            self.setDefaultBoard()

        self.currPos = [[],[]]

        if (currBlack != []):

            self.currPos[0] = currBlack

        else:

            self.currPos[0] = self.calcPos(0)

        if (currWhite != []):

            self.currPos[1] = currWhite

        else:

            self.currPos[1] = self.calcPos(1)     
#         print(self.currPos)     

    def boardMove(self, move_info, currPlayer):

        move = [move_info.start, move_info.end]

  #      print(move)

  #      self.drawBoardState()

        remove = move_info.jumpOver

        jump = move_info.jump      

        # start by making old space empty

        self.boardState[move[0][0]][move[0][1]] = -1

        # then set the new space to player who moved

        self.boardState[move[1][0]][move[1][1]] = currPlayer

        if jump:

            #remove jumped over enemies

            for enemy in move_info.jumpOver:

                self.boardState[enemy[0]][enemy[1]] = -1

        # update currPos array

        # if its jump, the board could be in many configs, just recalc it

        if jump:

            self.currPos[0] = self.calcPos(0)

            self.currPos[1] = self.calcPos(1)

        # otherwise change is predictable, so faster to just set it

        else:

            self.currPos[currPlayer].remove((move[0][0], move[0][1]))

            self.currPos[currPlayer].append((move[1][0], move[1][1]))

  #      print(self.currPos[currPlayer])



    def calcLegalMoves(self, player): # int array  -> [0] reg, [1] jump

        legalMoves = []

        hasJumps = False

        # next goes up if black or down if white

        next = -1 if player == 0 else 1

        boardLimit = 0 if player == 0 else BOARD_SIZE-1

        # cell refers to a position tuple (row, col)

        for cell in self.currPos[player]:
            
            if (cell[0] == boardLimit):

                continue

            # diagonal right, only search if not at right edge of board

            if (cell[1]!=BOARD_SIZE-1):

                #empty, regular move

                if (self.boardState[cell[0]+next][cell[1]+1]==-1 and not hasJumps):

                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]+1)) 

                    legalMoves.append(temp)

                # has enemy, can jump it?

                elif(self.boardState[cell[0]+next][cell[1]+1]==1-player):

                    jumps = self.checkJump((cell[0],cell[1]), False, player)

                    if (len(jumps)!=0):

                        # if first jump, clear out regular moves

                        if not hasJumps:

                            hasJumps = True

                            legalMoves = []

                        legalMoves.extend(jumps)

            # diagonal left, only search if not at left edge of board

            if (cell[1]!=0):

                if(self.boardState[cell[0]+next][cell[1]-1]==-1 and not hasJumps):

                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]-1)) 

                    legalMoves.append(temp)                    

                elif(self.boardState[cell[0]+next][cell[1]-1]==1-player):

                    jumps = self.checkJump((cell[0],cell[1]), True, player)

                    if (len(jumps)!=0):

                        if not hasJumps:

                            hasJumps = True

                            legalMoves = []                        

                        legalMoves.extend(jumps)
                        
                        

        return legalMoves



    # enemy is the square we plan to jump over

    # change later to deal with double jumps

    def checkJump(self, cell, isLeft, player):

        jumps = []

        next = -1 if player == 0 else 1

        # check boundaries!

        if (cell[0]+next == 0 or cell[0]+next == BOARD_SIZE-1):

            return jumps

        #check top left

        if (isLeft):

            if (cell[1]>1 and self.boardState[cell[0]+next+next][cell[1]-2]==-1):

                temp = Move(cell, (cell[0]+next+next, cell[1]-2), True)

                temp.jumpOver = [(cell[0]+next,cell[1]-1)]

                # can has double jump?

                helper = temp.end

                if (temp.end[0]+next > 0 and temp.end[0]+next < BOARD_SIZE-1):

                    #enemy in top left of new square?

                    if (temp.end[1]>1 and self.boardState[temp.end[0]+next][temp.end[1]-1]==(1-player)):

                        test = self.checkJump(temp.end, True, player)

                        if (test != []):

                            dbl_temp = deepcopy(temp) #deepcopy needed?



                            dbl_temp.end = test[0].end 

                            dbl_temp.jumpOver.extend(test[0].jumpOver)

                            jumps.append(dbl_temp)                        

                    # top right?

                    if (temp.end[1]<BOARD_SIZE-2 and self.boardState[temp.end[0]+next][temp.end[1]+1]==(1-player)):

                        test = self.checkJump(temp.end, False, player)                    

                        if (test != []):

                            dbl_temp = deepcopy(temp) #deepcopy needed?

                            dbl_temp.end = test[0].end 

                            dbl_temp.jumpOver.extend(test[0].jumpOver)

                            jumps.append(dbl_temp)                                 

                jumps.append(temp)

        else:

        #check top right

            if (cell[1]<BOARD_SIZE-2 and self.boardState[cell[0]+next+next][cell[1]+2]==-1):

                # ([original cell, new cell], enemy cell])

                temp = Move(cell, (cell[0]+next+next, cell[1]+2), True)

                temp.jumpOver = [(cell[0]+next,cell[1]+1)]

                # can has double jump?

                if (temp.end[0]+next > 0 and temp.end[0]+next < BOARD_SIZE-1):

                    #enemy in top left of new square?

                    if (temp.end[1]>1 and self.boardState[temp.end[0]+next][temp.end[1]-1]==(1-player)):

                        test = self.checkJump(temp.end, True, player)

                        if (test != []):

                            dbl_temp = deepcopy(temp) #deepcopy needed?

                            dbl_temp.end = test[0].end 

                            dbl_temp.jumpOver.extend(test[0].jumpOver)

                            jumps.append(dbl_temp)                                 

                    # top right?

                    if (temp.end[1]<BOARD_SIZE-2 and self.boardState[temp.end[0]+next][temp.end[1]+1]==(1-player)):

                        test = self.checkJump(temp.end, False, player) 

                        if (test != []):

                            dbl_temp = deepcopy(temp) #deepcopy needed?

                            dbl_temp.end = test[0].end 

                            dbl_temp.jumpOver.extend(test[0].jumpOver)

                            jumps.append(dbl_temp)                              

                jumps.append(temp)                

    # uncomment this when its time to try double jumps

     #   print("Jumps:")

     #   for mov in jumps:

     #       print(str(mov.start)+" "+str(mov.end)+" Jump over: "+str(mov.jumpOver))

        return jumps

    

    def calcPos(self, player):

        pos = []

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                if (self.boardState[row][col]==player):

                    pos.append((row,col))

        return pos

         

    def drawBoardState(self):

        for colnum in range(BOARD_SIZE):

            print(str(colnum)+" ",end="")

        print("")

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                if (self.boardState[row][col] == -1):

                    print("+ ",end='')

                elif (self.boardState[row][col] == 1):

                    print("G ",end='')

                elif (self.boardState[row][col] == 0):

                    print("R ",end='')

            print(str(row))



    def setDefaultBoard(self):
        # reset board
        if BOARD_SIZE == 6 and NUM_PLAYERS == 6:               
            self.boardState = getPositions()
           
#         if BOARD_SIZE == 8 and NUM_PLAYERS == 12: 
#             self.boardState = [
#     
#                 [-1,1,-1,1,-1,1,-1,1],
#     
#                 [1,-1,1,-1,1,-1,1,-1],
#     
#                 [-1,1,-1,1,-1,1,-1,1],
#     
#                 [-1,-1,-1,-1,-1,-1,-1,-1],
#     
#                 [-1,-1,-1,-1,-1,-1,-1,-1],
#     
#                 [0,-1,0,-1,0,-1,0,-1],
#     
#                 [-1,0,-1,0,-1,0,-1,0],
#     
#                 [0,-1,0,-1,0,-1,0,-1]
#     
#             ]
#         elif BOARD_SIZE == 6 and NUM_PLAYERS == 6: 
#             self.boardState = [
# 
#                 [1,-1,1,-1,1,-1],
#     
#                 [-1,-1,-1,-1,-1,1],
#     
#                 [1,-1,-1,-1,1,-1],
#     
#                 [-1,0,-1,0,-1,-1],
#     
#                 [-1,-1,0,-1,-1,-1],
#     
#                 [-1,0,-1,0,-1,0],
# 
#             ]

def main():
    print("You go first")

#     print("Who goes first? ")
#  
#     print("(0) You")
#  
#     print("(1) Robot Frankie")
#  
#     playr = int(input("Enter 0 or 1:"))
#  
#     while not (playr == 0 or playr == 1):
#  
#         playr = int(input("Invalid Choice, please try again: "))
 
    test = Game(0)

    test.run()
    
        

main() 

'''image = cv2.imread("checkerboard.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Over the Clouds", image)
cv2.imshow("Over the Clouds - gray", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
