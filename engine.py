import chess
import chess.svg
import chess.pgn
import chess.polyglot
import random
import time
import datetime
from IPython.display import SVG, clear_output, display


board = chess.Board()
SVG(chess.svg.board(board=board,size=500))
movehistory =[]

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

def evaluate_board3(board):
    
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_fivefold_repetition() or board.can_claim_draw() or board.is_insufficient_material():
        return 0    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
    
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KING, chess.BLACK)])
    
    eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq+random.randint(0, 4)
    if board.turn:
        return eval
    else:
        return -eval

def evaluate_board1(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_fivefold_repetition() or board.can_claim_draw() or board.is_insufficient_material():
        return 0    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
    #print("material= "+ str(material))
    eval = material+random.randint(0, 9)
    #print("evaluation = "+ str(eval))
    if board.turn:
        return -eval
    else:
        return eval

def evaluate_board2(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    elif board.is_fivefold_repetition():
        return 0
    elif board.can_claim_draw():
        return 0
    elif board.is_insufficient_material():
        return 0    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
    #print("material= "+ str(material))
    eval = material+random.randint(0, 9)
    #print("evaluation = "+ str(eval))
    if board.turn:
        return eval
    else:
        return -eval

#No depth 
def player1(board):
        bestMove = chess.Move.null()
        bestValue = -99999
        for move in board.legal_moves:
            #print(str(bestValue))
            board.push(move)
            boardValue = evaluate_board1(board)
            if boardValue > bestValue:
                #print(str(boardValue) +">" + str(bestValue))
                bestValue = boardValue;
                bestMove = move
            board.pop()
        movehistory.append(bestMove)
        return bestMove.uci()
    
#Minimax added  
def player2(board):
        start= time.time()
        bestMove= minimax(board, 3)[1]
        end= time.time()
        print("Total time thiking= "+ str(end-start))
        movehistory.append(bestMove)
        return bestMove.uci()

#Square-Piece Tables added
#Negamax and Quiescence Added
def player4(board):
    start= time.time()
    alpha = -100000
    beta = 100000
    bestValue = -99999
    bestMove = chess.Move.null()
    depth = 3
    bestMove= alphabeta2(alpha, beta, depth, board)[1]
    end= time.time()
    print("Total time thiking= "+ str(end-start))
    movehistory.append(bestMove) 
    return bestMove.uci()
        
  
  
def minimax(board, depth):
    if depth==0:
        return [evaluate_board1(board), None]
    else:
        if board.turn == chess.WHITE:
            bestscore=-99999
            bestmove= None
            for move in board.legal_moves:
                newboard=board.copy()
                newboard.push(move)
                score_and_move= minimax(newboard, depth-1)
                score = score_and_move[0]
                if score> bestscore: #white is max
                    bestscore = score
                    bestmove=move
            return [bestscore,bestmove]
        else:
            bestscore=99999
            bestmove=None
            for move in board.legal_moves:
                newboard=board.copy()
                newboard.push(move)
                score_and_move= minimax(newboard, depth-1)
                score = score_and_move[0]
                if score < bestscore: #black is min 
                    bestscore = score
                    bestmove = move
            return [bestscore,bestmove]
        
def alphabeta(alpha, beta, depth, board):
    if( depth == 0 ):
        return quiesce(alpha, beta, board)
    bestmove=None 
    for move in board.legal_moves:
        board.push(move)   
        score = alphabeta(-beta, -alpha, depth - 1, board)[0]*-1
        board.pop()
        if(score >= beta):
            bestmove=move
            return [beta, bestmove] #fail hard beta-cutoff
        if(score > alpha):
            bestmove=move
            alpha = score   
    return [alpha, bestmove] #alpha acts like max in MiniMax

#Using Square-Piece Tables
def alphabeta2(alpha, beta, depth, board):
    if( depth == 0 ):
        return quiesce2(alpha, beta, board)
    bestmove=None 
    for move in board.legal_moves:
        board.push(move)   
        score = alphabeta2(-beta, -alpha, depth - 1, board)[0]*-1
        board.pop()
        if(score >= beta):
            bestmove=move
            return [beta, bestmove] #fail hard beta-cutoff
        if(score > alpha):
            bestmove=move
            alpha = score   
    return [alpha, bestmove] #alpha acts like max in MiniMax

def quiesce(alpha, beta, board):
    stand_pat = evaluate_board2(board)
    bestmove= None
    if(stand_pat >= beta):
        return [beta, None]
    if(alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)        
            score = quiesce(-beta, -alpha, board)[0]*-1
            board.pop()
            if(score >= beta):
                bestmove=move
                return [beta, bestmove]
            if(score > alpha):
                bestmove=move
                alpha = score  
    return [alpha, bestmove]

#Using Square-Piece Tables
def quiesce2(alpha, beta, board):
    stand_pat = evaluate_board3(board)
    bestmove= None
    if(stand_pat >= beta):
        return [beta, None]
    if(alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)        
            score = quiesce2(-beta, -alpha, board)[0]*-1
            board.pop()
            if(score >= beta):
                bestmove=move
                return [beta, bestmove]
            if(score > alpha):
                bestmove=move
                alpha = score  
    return [alpha, bestmove]

def ran_player(board):
    move = random.choice(list(board.legal_moves))
    movehistory.append(move)
    return move.uci()

def who(player):
    return "White" if player == chess.WHITE else "Black"

def play_game(player1, player2, pause=0.05):

    game = chess.pgn.Game()
    game.headers["Event"] = "Game"
    game.headers["Site"] = "WoW"
    game.headers["Date"] = str(datetime.datetime.now().date())
    game.headers["Round"] = 1
    game.headers["White"] = "player2"
    game.headers["Black"] = "ran_player"
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = who(board.turn)
            board.push_uci(uci)
            board_stop = board._repr_svg_()
            clear_output(wait=True)
            print("Move " + str(len(board.move_stack)) +" "+ name +" , Play "+ uci + " ")
            display(board)
            time.sleep(pause)
            
            
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    game.add_line(movehistory)
    game.headers["Result"] = str(board.result(claim_draw=True))
    print(game)
    print(game, file=open("game.pgn", "w"), end="\n\n")
    print(msg)
    display(board_stop)
    return [result, msg, board]

def human_player(board):
    display(board)
    uci = get_move("%s's move [q to quit]> " % who(board.turn))
    legal_uci_moves = [move.uci() for move in board.legal_moves]
    while uci not in legal_uci_moves:
        print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
        uci = get_move("%s's move[q to quit]> " % who(board.turn))
    return uci
def get_move(prompt):
    uci = input(prompt)
    if uci and uci[0] == "q":
        raise KeyboardInterrupt()
    try:
        chess.Move.from_uci(uci)
    except:
        uci = None
    return uci
#Opening book implemented in player 5
def player5(board):
    start= time.time()
    bestMove = chess.Move.null()
    try:
        bestMove = chess.polyglot.MemoryMappedReader("Stockfish_Book.bin").weighted_choice(board).move
        print ("Book Move")
    except:
        alpha = -100000
        beta = 100000
        bestValue = -99999
        bestMove = chess.Move.null()
        depth = 3
        bestMove= alphabeta2(alpha, beta, depth, board)[1]
    end= time.time()
    print("Total time thiking= "+ str(end-start))
    movehistory.append(bestMove)
    return bestMove.uci()
#Negamax and Quiescence Added
def player3(board):
    start= time.time()
    alpha = -100000
    beta = 100000
    bestValue = -99999
    bestMove = chess.Move.null()
    depth = 3
    bestMove= alphabeta(alpha, beta, depth, board)[1]
    end= time.time()
    print("Total time thiking= "+ str(end-start))
    movehistory.append(bestMove) 
    return bestMove.uci()
