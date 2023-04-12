import chess
import chess.svg
import multiprocessing as mp

board = chess.Board()

board.set_board_fen("r2q1rk1/2p1bppp/p1n5/1p2Pb2/8/1PPpBN2/1P3PPP/RB1Q1RK1")

def evaluate_board(board):

    pawn_white = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [78,  83,  86,  73, 102,  82,  85,  90],
    [7,  29,  21,  44,  40,  31,  44,   7],
    [-17,  16,  -2,  15,  14,   0,  15, -13],
    [-26,   3,  10,   9,   6,   1,   0, -23],
    [-22,   9,   5, -11, -10,  -2,   3, -19],
    [-31,   8,  -7, -37, -36, -14,   3, -31],
    [0, 0, 0, 0, 0, 0, 0, 0]]

    knight_white = [
    [-66, -53, -75, -75, -10, -55, -58, -70],
    [-3,  -6, 100, -36,   4,  62,  -4, -14],
    [10,  67,   1,  74,  73,  27,  62,  -2],
    [24,  24,  45,  37,  33,  41,  25,  17],
    [-1,   5,  31,  21,  22,  35,   2,   0],
    [-18,  10,  13,  22,  18,  15,  11, -14],
    [-23, -15,   2,   0,   2,   0, -23, -20],
    [-74, -23, -26, -24, -19, -35, -22, -69]]

    bishop_white = [
    [-59, -78, -82, -76, -23,-107, -37, -50],
    [-11,  20,  35, -42, -39,  31,   2, -22],
    [-9,  39, -32,  41,  52, -10,  28, -14],
    [25,  17,  20,  34,  26,  25,  15,  10],
    [13,  10,  17,  23,  17,  16,   0,   7],
    [14,  25,  24,  15,   8,  25,  20,  15],
    [19,  20,  11,   6,   7,   6,  20,  16],
    [-7,   2, -15, -12, -14, -15, -10, -10]]

    rook_white = [[35,  29,  33,   4,  37,  33,  56,  50],
    [55,  29,  56,  67,  55,  62,  34,  60],
    [19,  35,  28,  33,  45,  27,  25,  15],
    [0,   5,  16,  13,  18,  -4,  -9,  -6],
    [-28, -35, -16, -21, -13, -29, -46, -30],
    [-42, -28, -42, -25, -25, -35, -26, -46],
    [-53, -38, -31, -26, -29, -43, -44, -53],
    [-30, -24, -18,   5,  -2, -18, -31, -32]]

    queen_white = [[6,   1,  -8,-104,  69,  24,  88,  26],
    [14,  32,  60, -10,  20,  76,  57,  24],
    [-2,  43,  32,  60,  72,  63,  43,   2],
    [1, -16,  22,  17,  25,  20, -13,  -6],
    [-14, -15,  -2,  -5,  -1, -10, -20, -22],
    [-30,  -6, -13, -11, -16, -11, -16, -27],
    [-36, -18,   0, -19, -15, -15, -21, -38],
    [-39, -30, -31, -13, -31, -36, -34, -42]]

    king_white = [[4,  54,  47, -99, -99,  60,  83, -62],
    [-32,  10,  55,  56,  56,  55,  10,   3],
    [-62,  12, -57,  44, -67,  28,  37, -31],
    [-55,  50,  11,  -4, -19,  13,   0, -49],
    [-55, -43, -52, -28, -51, -47,  -8, -50],
    [-47, -42, -43, -79, -64, -32, -29, -32],
    [-4,   3, -14, -50, -57, -18,  13,   4],
    [17,  30,  -3, -14,   6,  -1,  40,  18]]

    score = 0
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(i*8 + j)
            if(piece is not None):
                if piece.color == chess.WHITE:
                    if piece.piece_type == chess.PAWN:
                        score += 100
                        score += pawn_white[7-i][j]
                    elif piece.piece_type == chess.KNIGHT:
                        score += 280
                        score += knight_white[7-i][j]
                    elif piece.piece_type == chess.BISHOP:
                        score += 320
                        score += bishop_white[7-i][j]
                    elif piece.piece_type == chess.ROOK:
                        score += 479
                        score += rook_white[7-i][j]
                    elif piece.piece_type == chess.QUEEN:
                        score += 929
                        score += queen_white[7-i][j]
                    elif piece.piece_type == chess.KING:
                        score += 60000
                        score += king_white[7-i][j]

                else:
                    if piece.piece_type == chess.PAWN:
                        score -= 100
                        score -= pawn_white[i][j]
                    elif piece.piece_type == chess.KNIGHT:
                        score -= 280
                        score -= knight_white[i][j]
                    elif piece.piece_type == chess.BISHOP:
                        score -= 320
                        score -= bishop_white[i][j]
                    elif piece.piece_type == chess.ROOK:
                        score -= 479
                        score -= rook_white[i][j]
                    elif piece.piece_type == chess.QUEEN:
                        score -= 929
                        score -= queen_white[i][j]
                    elif piece.piece_type == chess.KING:
                        score -= 60000
                        score -= king_white[i][j]

    return score

def minimax(board, depth, alpha, beta, maximizing_player, cache):
    key = (board.fen(), depth, maximizing_player)
    if key in cache:
        return cache[key]
    
    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board)
        cache[key] = eval
        return eval

    legal_moves = list(board.legal_moves)
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, cache)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        cache[key] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, cache)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        cache[key] = min_eval
        return min_eval


def get_best_move(board, depth):
    maximizing_player = board.turn
    legal_moves = list(board.legal_moves)
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    cache = {}

    pool = mp.Pool(processes=8)
    results = []
    for move in legal_moves:
        board.push(move)
        result = pool.apply_async(minimax, (board, depth - 1, alpha, beta, not maximizing_player, cache))
        results.append((move, result))
        board.pop()
    
    pool.close()
    pool.join()

    for move, result in results:
        eval = result.get()
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
    
    return best_move

while(True):
    print(evaluate_board(board))
    best_move = get_best_move(board, depth = 7)
    print(best_move)
    board.push(best_move)
    print(board)
    board.push(board.parse_san(input("Wpisz ruch przeciwnika: ")))
    print(board)
