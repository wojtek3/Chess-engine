import chess
import chess.polyglot

board = chess.Board()
board.set_board_fen("rnbqkbnr/p4ppp/4p3/1pppP3/2PP4/8/PP3PPP/RNBQKBNR")

def check_book(board):
    book = chess.polyglot.open_reader("Titans.bin")
    try:
        main_entry = book.find(board)
        return main_entry
    except:
        return None

print(check_book(board))
