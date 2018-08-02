#!/usr/bin/env python2
from socketIO_client import SocketIO
import random
import sys
import time

my_board = []

socketIO = None

def updateBoard(data):
    """ Server inform me that board has been updated
    """
    my_board = data['board']
    print('Board updated')

def makeAMove(data):
    """ Send to server my move
    """
    print(data['message'])
    board = data['board']
    computer = data['player']
    
    row, col = getComputerMove(board, computer)

    my_move = {'row': row, 'col': col}
 

    socketIO.emit('mymove', {'rowIdx': my_move['row'], 'colIdx': my_move['col']})

def end(data):
    """ Game is over!
    """
    print('Game is over !')
    print('Winner is: ' + str(data['winner']))
    print('Player 1 number: ' + str(data['player1']))
    print('Player 2 number: ' + str(data['player2']))

def print_error(data):
    print('Error: ' + str(data))

# ##################################################################
# AI Code ##########################################################
"""
Constant Variable
"""
WIN = 9999
LOSE = -9999

BETA_MAX = 12345
ALPHA_MIN = -12345
DEPTH = 4
MAX_TIME_THINKING = 5

CONST_SOLANMATLUOT = 0
CONST_HIEUSONUOCDI = 4
CONST_STABILITY_BENVUNG = 5
CONST_SUBSCORE = 0
CONST_STABILITYSCORE = 1
CONST_numerBoundary = 0

SQUARE_WEIGHTS = [
     [50, -8, 8, 6, 6, 8, -8, 50],
    [-8, -20,  -1,  -1,  -1,  -1, -20, -8],
    [8, -1, 5, 1, 1, 5, -1, 8],
    [6, -1, 1, 2, 2, 1, -1, 6],
    [ 6, -1, 1, 2, 2, 1, -1, 6],
    [8, -1, 5, 1, 1, 5, -1, 8],
    [-8, -20, -1, -1, -1, -1, -20, -8],
    [50, -8, 8, 6, 6, 8, -8, 50]
]



"""
Main Functions
"""
def getComputerMove(board, computerTile):

    start_time = time.time()
    

    moves = getValidMoves(board, computerTile)

    for x,y in moves[:4]:
        if isOnCorner(x,y)== True:
            return (x,y)
    
    dupeBoard = getBoardCopy(board)
    

    soNuocDiConLai = MAX_SoNuocDiConLai(dupeBoard, computerTile)


    if soNuocDiConLai > 20:
        bestMove=alphabeta_searcher(DEPTH, TongHopAllLuongGia, computerTile, dupeBoard, start_time, soNuocDiConLai)
    elif soNuocDiConLai <= 35 and soNuocDiConLai >= 15:
        bestMove=alphabeta_searcher(DEPTH+2, TongHopAllLuongGia, computerTile, dupeBoard, start_time, soNuocDiConLai)
    else:
        bestMove=alphabeta_searcher(DEPTH+6, TongHopAllLuongGia, computerTile, dupeBoard, start_time, soNuocDiConLai)
   
    return bestMove


def final_value(player, board):
#
    result = getScore(board, player)
    if result < 0:
        return (LOSE+result)
    elif result > 0:
        return (WIN+result)
    return result

def alphabeta(player, board, alpha, beta, depth, TongHopAllLuongGia, start_time, soNuocDiConLai):
    
    if depth == 0 or soNuocDiConLai == 0:
        return TongHopAllLuongGia(board, player), None
    if soNuocDiConLai < 20:
        CONST_HIEUSONUOCDI = 2
        CONST_STABILITY_BENVUNG = 10
        CONST_SUBSCORE = 0
        CONST_STABILITYLITYSCORE = 0.5


    def value(board, alpha, beta):
         return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, TongHopAllLuongGia, start_time, soNuocDiConLai-1)[0]
             
    moves = getValidMoves(board, player)

    for x,y in moves[:4]:
        if isOnCorner(x,y)== True:
            return -alpha,(x,y)
    
    if moves==[]:
        
        moves_opp = getValidMoves(board, opponent(player))
        if moves_opp==[]:
            return final_value(player, board), None
        return value(board, alpha, beta), None

    if moves==[]:
        best_move=[]
    else:
        best_move=moves[0]
    for [x,y] in moves:
        if alpha >= beta or time.time()- start_time > MAX_TIME_THINKING :
             break
        dupeBoard= getBoardCopy(board)
        makeMove(dupeBoard, player, x, y)
        val = value(dupeBoard, alpha, beta)
        
        #import pdb; pdb.set_trace()
        if val > alpha:
            alpha = val
            best_move = (x,y)
    return alpha, best_move

def alphabeta_searcher(depth, TongHopAllLuongGia, player, board, start_time, soNuocDiConLai):
    return alphabeta(player, board, ALPHA_MIN, BETA_MAX, depth, TongHopAllLuongGia, start_time, soNuocDiConLai)[1]

def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def MAX_SoNuocDiConLai(board, computerTile):
    soQuanCoDaDanh = 0
    for b in board:
        soQuanCoDaDanh += b.count(1)
        soQuanCoDaDanh += b.count(2)

    return (MAX_MOVES - soQuanCoDaDanh)

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    a = []
    b = []

    for [x,y] in [[0,0],[0,7],[7,7],[7,0],[0,2],[2,0],[5,0],[0,5],[2,7],[7,2],[5,7],[7,5]]:
        if isValidMove(board, tile, x, y) != False:
                a.append([x, y])
    for [x,y] in [[0,1],[0,3],[0,4],[0,6],[1,0],[1,2],[1,3],[1,4],[1,5],[1,7],
                  [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[3,0],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],
                  [4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],
                  [6,0],[6,2],[6,3],[6,4],[6,5],[6,7],[7,1],[7,3],[7,4],[7,6],[1,1],[1,6],[6,1],[6,6]]:
        if isValidMove(board, tile, x, y) != False:
            b.append([x, y])


    random.shuffle(a)
    random.shuffle(b)

    validMoves = a+b
    return validMoves

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard

def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([-1] * 8)

    return board

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def MAX_SoNuocDiConLai(board, computerTile):
    soQuanCoDaDanh = 0
    for b in board:
        soQuanCoDaDanh += b.count(1)
        soQuanCoDaDanh += b.count(2)

    return (64 - soQuanCoDaDanh)
    

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != -1 or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 1:
        otherTile = 2
    else:
        otherTile = 1

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = -1 # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def opponent(player):
    return 1 if player==2 else 2

"""
Luong Gia 1
"""
def weighted_score(board, computerTile):
    opp = opponent(computerTile)
    total = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == computerTile:
                total += SQUARE_WEIGHTS[x][y]
            elif board[x][y]==opp:
                total-=SQUARE_WEIGHTS[x][y]
    return total

"""
Luong gia 2
"""
def forfeit_MatLuot(board, computerTile, depth, subScore):
     if depth>2:#chi xai ham nay 2 lan
        return 0 
     opp = opponent(computerTile) #doi qua quan doi phuong
     countForfeit_lan1 = 0
     possibleOpp = getValidMoves(board, opp) #lay all nc di cua doi phuong
     if possibleOpp==[]:#neu doi phuong eo danh dc, bi mat luot
         countForfeit_lan1=1
         possibleMyTurn = getValidMoves(board, computerTile)#no bi skip, thi gio coi minh danh dc ko
         if possibleMyTurn==[]: #neu minh cung eo danh dc, theo luat thi gameover tai day.    
             #xem minh dang hon diem no ko
             if subScore>0:#minh se thang
                 return (WIN +subScore)#quat ngay va luon nc nay
             else:
                 return (LOSE+subScore) #dung danh nc nay
         else:#minh van danh dc, sau khi no bi skip
             for [x,y] in possibleMyTurn: #check tiep trong nhung nc m danh dc
                  tempBoard = getBoardCopy(board)# dung board phu, luu nc danh nay vao ban co
                  makeMove(tempBoard, computerTile, x, y)#thuc hien nc danh vao board phu
                  subSocreLan2= getScore(tempBoard, computerTile)
                  countForfeit_lan2 = forfeit_MatLuot(tempBoard, computerTile, depth+1, subSocreLan2)#tiep tuc ktra Ham luong gia nay them 1 lan nua
                  return (countForfeit_lan1+countForfeit_lan2)
     else:#no van co nc de danh
         return 0#ham luong gia nay bang 0

"""
Luong gia 3
"""
def getScore(board, computerTile):
    xscore = 0
    oscore = 0
    #import pdb;pdb.set_trace()
    for x in range(8):
        for y in range(8):
            if board[x][y] == 1:
                xscore += 1
            if board[x][y] == 2:
                oscore += 1
    score = xscore - oscore

    return score if computerTile==1 else (-score)# tra ve hieu cua score phe minh, vs phe doi phuong

"""
Luong gia 4
"""
def mobility(board, computerTile):
      opp = opponent(computerTile) #doi qua quan doi phuong
      possibleOpp = getValidMoves(board, opp) #lay all nc di cua doi phuong
      possibleMy = getValidMoves(board, computerTile)
      return (len(possibleMy)-len(possibleOpp))


"""
luong gia 5
"""
def isFlip(board, xTile, yTile, table):#ktra xem 1 square co the bi lat (flip) ko.
    tile = board[xTile][yTile]# xac dinh loai quan cua o can ktra (figure out what's the kind of checking tile)
    opp=opponent(tile)

    hasSpaceSide1  = False
    hasUnsafeSide1 = False
    hasSpaceSide2  = False
    hasUnsafeSide2 = False

    # Check the horizontal line through the disc.
    for y1 in range(yTile):#checking on the left
        if hasSpaceSide1==True:
            break
        elif (board[xTile][y1]!=opp and board[xTile][y1]!=tile):#empty square
            hasSpaceSide1=True
        elif (board[xTile][y1]==opp and table[xTile][y1]==False):
            hasUnsafeSide1=True


    for y2 in range(yTile+1,8):#checking on the right
        if hasSpaceSide2==True:
            break
        elif (board[xTile][y2]!=opp and board[xTile][y2]!=tile):#empty square
            hasSpaceSide2=True
        elif (board[xTile][y2]==opp and table[xTile][y2]==False):
            hasUnsafeSide2=True

    if ((hasSpaceSide1  and hasSpaceSide2 ) or
        (hasSpaceSide1  and hasUnsafeSide2) or
        (hasUnsafeSide1 and hasSpaceSide2 )):
        return True
     # Check the vertical line through the disc.
    hasSpaceSide1  = False
    hasUnsafeSide1 = False
    hasSpaceSide2  = False
    hasUnsafeSide2 = False

    for x1 in range(xTile):
        if hasSpaceSide1==True:
            break
        elif (board[x1][yTile]!=opp and board[x1][yTile]!=tile):#empty square
            hasSpaceSide1=True
        elif (board[x1][yTile]==opp and table[x1][yTile]==False):
            hasUnsafeSide1=True
    for x1 in range(xTile+1,8):
        if hasSpaceSide2==True:
            break
        elif (board[x1][yTile]!=opp and board[x1][yTile]!=tile):#empty square
            hasSpaceSide2=True
        elif (board[x1][yTile]==opp and table[x1][yTile]==False):
            hasUnsafeSide2=True
    if ((hasSpaceSide1  and hasSpaceSide2 ) or
        (hasSpaceSide1  and hasUnsafeSide2) or
        (hasUnsafeSide1 and hasSpaceSide2 )):
        return True
    #Check the Northwest-Southeast diagonal line through the disc.
    hasSpaceSide1  = False
    hasUnsafeSide1 = False
    hasSpaceSide2  = False
    hasUnsafeSide2 = False
    i=xTile-1
    j=yTile-1
    while (i>=0 and j>=0 and hasSpaceSide1==False):
        if (board[i][j]!=opp and board[i][j]!=tile):
            hasSpaceSide1=True
        elif (board[i][j]==opp and table[i][j]==False):
            hasUnsafeSide1=True
        i-=1
        j-=1
    i=xTile+1
    j=yTile+1
    while (i<8 and j<8 and hasSpaceSide2==False):
        if (board[i][j]!=opp and board[i][j]!=tile):
            hasSpaceSide2=True
        elif (board[i][j]==opp and table[i][j]==False):
            hasUnsafeSide2=True
        i+=1
        j+=1
    if ((hasSpaceSide1  and hasSpaceSide2 ) or
        (hasSpaceSide1  and hasUnsafeSide2) or
        (hasUnsafeSide1 and hasSpaceSide2 )):
        return True
    #Check the Northeast-Southwest diagonal line through the disc.
    hasSpaceSide1  = False
    hasUnsafeSide1 = False
    hasSpaceSide2  = False
    hasUnsafeSide2 = False
    i=xTile-1
    j=yTile+1
    while (i>=0 and j<8 and hasSpaceSide1==False):
        if (board[i][j]!=opp and board[i][j]!=tile):
            hasSpaceSide1=True
        elif (board[i][j]==opp and table[i][j]==False):
            hasUnsafeSide1=True
        i-=1
        j+=1
    i=xTile+1
    j=yTile-1
    while (i<8 and j>=0 and hasSpaceSide2==False):
        if (board[i][j]!=opp and board[i][j]!=tile):
            hasSpaceSide2=True
        elif (board[i][j]==opp and table[i][j]==False):
            hasUnsafeSide2=True
        i+=1
        j-=1
    if ((hasSpaceSide1  and hasSpaceSide2 ) or
        (hasSpaceSide1  and hasUnsafeSide2) or
        (hasUnsafeSide1 and hasSpaceSide2 )):
        return True
    return False
#end ham isFlip

def stabilityFlip(board, computerTile):
    table = []
    for i in range(8):
        table.append([False] * 8)
    
    opp=opponent(computerTile)
    changed = True
    while changed:#neu co 1 cai tro thanh Ben Vung, thi co the tac dong den cac o con lai, nen can ktra lai
        changed=False
        for i in range(8):
            for j in range(8):
                if ( (board[i][j]== computerTile or board[i][j]==opp) and table[i][j]==False and isFlip(board, i, j, table)==False):
                    table[i][j]=True
                    changed=True
                    #print board
    
    count_com=0
    count_opp=0
    for i in range(8):
            for j in range(8):
                if board[i][j]==computerTile:
                    if table[i][j]==True:
                        count_com+=1
                elif board[i][j]==opp:
                    if table[i][j]==True:
                        count_opp+=1
    return (count_com-count_opp)

"""
luong gia 6
"""

def numberBoundary(dupeBoard, player):
    boundaryBoard =[]     
    for i in range(10):
        if(i == 0 or i == 9):
            boundaryBoard.append(['x']*10)
        else:
            boundaryBoard.append(['x',' ',' ',' ',' ',' ',' ',' ',' ','x'])

    for x in range(1,9):
        for y in range(1,9):
           boundaryBoard[x][y] = dupeBoard[x-1][y-1]
    number_mine = 0
    number_opp = 0
    for i in range(1,9):
        for j in range(1,9):
            if( (boundaryBoard[i][j] == player) and (boundaryBoard[i+1][j]==' ' or boundaryBoard[i-1][j]==' ' or boundaryBoard[i][j+1]==' ' or boundaryBoard[i][j-1]==' ') or boundaryBoard[i-1][j+1]==' ' or boundaryBoard[i+1][j+1]==' ' or boundaryBoard[i-1][j-1]==' ' or boundaryBoard[i+1][j-1]==' '):
                number_mine +=1
            elif ( (boundaryBoard[i][j] ==opponent(player)) and (boundaryBoard[i+1][j]==' ' or boundaryBoard[i-1][j]==' ' or boundaryBoard[i][j+1]==' ' or boundaryBoard[i][j-1]==' ') or boundaryBoard[i-1][j+1]==' ' or boundaryBoard[i+1][j+1]==' ' or boundaryBoard[i-1][j-1]==' ' or boundaryBoard[i+1][j-1]==' '):
                number_opp +=1
    return (number_mine - number_opp)

def TongHopAllLuongGia(dupeBoard, computerTile):
    #subScore=getScore(dupeBoard, computerTile) #ham luong gia 3, tinh hieu so diem
    stabilityScore = weighted_score(dupeBoard, computerTile) #ham luong gia 1, xai bang trong so, neu chi xai ham nay thi may van kha stupid, dang goc cho doi phuong an
    #soLanMatLuot=forfeit_MatLuot(dupeBoard, computerTile, 1, subScore)#ham luong gia 2, tinh so lan mat luot cua doi phuong

    hieuSonuocDi = mobility(dupeBoard, computerTile)#luong gia 4

    stability_benVung = stabilityFlip(dupeBoard, computerTile)
    
    #numberBoundary_Score = numberBoundary(dupeBoard, computerTile)


    score_phoiHop= CONST_HIEUSONUOCDI*hieuSonuocDi + CONST_STABILITY_BENVUNG*stability_benVung + CONST_STABILITYSCORE*stabilityScore
    
    return score_phoiHop


# ##################################################################

token = raw_input('Enter your token: ')

socketIO = SocketIO('localhost', 8080, params={'token': token})
#socketIO.connect('/play')
socketNS = '/play'

# Define callback to updated event
socketIO.on('updated', updateBoard, socketNS)

# Define callback to yourturn event
socketIO.on('yourturn', makeAMove, socketNS)

# Define callback to end event
socketIO.on('end', end, socketNS)

# Define callback to errormessage event
socketIO.on('errormessage', print_error, socketNS)

socketIO.wait()
