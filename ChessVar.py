# Name: Aadil Ali
# Date: 08/17/2023
# GitHub: aaadil777
# Creation of a chess game

class ChessVar:
    """
    Sets players turn and directs the game to UNFINISHED status.
    """
    def __init__(self):
        """
        Initializes game board as new game.
        """
        self.board = Board()
        self.current_turn = "white"
        self.game_state = "UNFINISHED"
        self.first_move_done = False
        self.moves_made = 0
        self.board = Board()
    def get_game_state(self):
        """
        gives the game's current state back. seeks out the winning criteria on the board.
        """
        return self.game_state
    def make_move(self, from_square, to_square):
        """
        refreshes the board after verifying the move's validity. The game condition might alter if a king
        moves up to the eighth row. It will switch the player's turn after a move. Ensures pawn moves first
        """
        piece = self.board.get_piece(start)
        if not piece:
            raise ValueError("No piece at the starting square.")
        if not self.first_move_done:
            piece = self.board.get_piece(from_square)
            if not isinstance(piece, Pawn):
                return False
        if not piece.is_valid_move(start, end):
            raise ValueError("Invalid move for the piece.")
        if self.game_state != "UNFINISHED":
            return False
        if not self.__is_valid_move(from_square, to_square):
            return False
         if piece.type == 'king' and end[0] == 7:
            return "King has reached the 8th row. Game won by " + piece.color + "!"
        self.board.move_piece(from_square, to_square)
        self.moves_made += 1
        self.__toggle_turn()
        self.__update_game_state()
        return True
    def __is_valid_move(self, from_square, to_square):
        """
        Verify the move's validity by checking that move is valid based on chess game logic, does not reveal one's king and the opponent's king
        """
        piece = self.board.get_piece(from_square)
        if not piece or piece.color != self.current_turn:
            return False
        if to_square not in piece.valid_moves(from_square):
            return False
        return True
    def __update_game_state(self):
        """
        Check the board for any situations that might discontinue the game, such a king landing on the
        eighth row
        """
        white_king_pos, black_king_pos = self.board.get_king_positions()
        if white_king_pos[1] == 7:
            self.game_state = "WHITE_WON"
        elif black_king_pos[1] == 7:
            self.game_state = "BLACK_WON"
    def __toggle_turn(self):
        """
        Switches the turn from white to black or vice versa.
        """
        self.current_turn = "black" if self.current_turn == "white" else "white"
    def make_move(self, start, end):
        """
        makes new move toggle
        """
        piece = self.board.get_piece(start)
        
        if not piece:
            raise ValueError("No piece at the starting square.")
        
        if self.moves_made == 0 and piece.type != 'pawn':
            raise ValueError("The first move of the game must be made by a pawn.")
        
        self.moves_made += 1

class Board:
    """
    configures board setup
    """
    def __init__(self):
        """
        Initialize the board to its starting position.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
    def move_piece(self, from_square, to_square):
        start_row, start_col = GameUtils.notation_to_index(from_square)
        end_row, end_col = GameUtils.notation_to_index(to_square)
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
    def place_piece(self, piece, row, col):
        """
        Place a piece on the board at the specified location.
        """
        self.board[row][col] = piece
    def get_piece(self, row, col):
        """
        Get the piece present at the specified location.
        Returns None if no piece is present.
        """
        row, col = GameUtils.notation_to_index(square)
        return self.board[row][col]

    def remove_piece(self, row, col):
        """
        Remove a piece from the specified location.
        """
        self.board[row][col] = None

    def knock_down_piece(self, piece):
        """
        Handles a piece that has been captured
        """
        piece = self.game_board.get_piece(square)
        if piece:
            self.captured_pieces.append(piece)
            row, col = GameUtils.notation_to_index(square)
            self.game_board.remove_piece(row, col)

    def is_king_in_check(self, color):
        """
        determines if a king (identified by color) is in check by inspecting the board.
        """
        king_position = self.get_king_position(color)
        return GameUtils.is_square_under_attack(self.board, king_position, "black" if color == "white" else "white")
        pass

    def get_king_positions(self):
        """
        gets the king position
        :param self:
        :return:
        """
        white_king_pos, black_king_pos = None, None
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and isinstance(piece, King):
                    if piece.color == "white":
                        white_king_pos = (i, j)
                    else:
                        black_king_pos = (i, j)
        return white_king_pos, black_king_pos

    def is_move_valid_for_piece(self, piece, from_square, to_square):
        """
        Verify if the move complies with the movement rules for the given piece, given the piece's
        beginning and finishing locations.
        """
        return to_square in piece.valid_moves(from_square) and not self.is_path_blocked(from_square, to_square)

    def is_path_blocked(self, from_square, to_square):
        """
        Checks if there is any piece obstructing the path between from_square and to_square.
        Assumes that the move is valid in terms of movement patterns.
        """
        start_row, start_col = GameUtils.notation_to_index(from_square)
        end_row, end_col = GameUtils.notation_to_index(to_square)
        if start_col == end_col:
            row_step = 1 if start_row < end_row else -1
            for r in range(start_row + row_step, end_row, row_step):
                if self.board[r][start_col]:
                    return True
        elif start_row == end_row:
            col_step = 1 if start_col < end_col else -1
            for c in range(start_col + col_step, end_col, col_step):
                if self.board[start_row][c]:
                    return True
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if start_row < end_row else -1
            col_step = 1 if start_col < end_col else -1
            r, c = start_row + row_step, start_col + col_step
            while r != end_row and c != end_col:
                if self.board[r][c]:
                    return True
                r += row_step
                c += col_step
        return False
    def display(self):
        """
        Displays basic board formation.
        """
        for row in self.board:
            display_row = []
            for piece in row:
                if piece:
                    display_row.append(f"{piece.color[0]}{piece.type[0]}")
                else:
                    display_row.append("--")
class Piece:
    """
    Base class for all chess pieces.
    """
    def __init__(self, color, piece_type):
        """
        Initialize a chess piece with a color (white or black) and type (e.g., 'pawn', 'rook', etc.).
        """
        self.color = color
        self.type = piece_type

    def valid_moves(self, position):
        """
        Method to get all valid moves for a piece from a given position.
        """
        raise NotImplementedError("valid_moves() must be defined in subclasses.")

class King(Piece):
    def valid_moves(self, position):
        """
        Get all valid moves for the king from the given position.
        """
        row, col = GameUtils.notation_to_index(position)
        moves = [(r, c) for r, c in [(row-1, col-1), (row-1, col), (row-1, col+1),
                                     (row, col-1), (row, col+1),
                                     (row+1, col-1), (row+1, col), (row+1, col+1)]
                 if 0 <= r < 8 and 0 <= c < 8]
        return [GameUtils.index_to_notation(move) for move in moves]

class Queen(Piece):
    def __init__(self, color):
        """
        Initializes queen for both sides and moves
        :param color:
        """
        super().__init__(color, "queen")
    def valid_moves(self, position):
        """
        Get all valid moves for the queen from the given position.
        """
        rook_moves = Rook.valid_moves(self, position)
        bishop_moves = Bishop.valid_moves(self, position)
        return rook_moves + bishop_moves

class Rook(Piece):
    """
    Initializes rook piece and moves
    """
    def __init__(self, color):
        super().__init__(color, "rook")
    def valid_moves(self, position):
        """
        Get all valid moves for the rook from the given position.
        """
        row, col = GameUtils.notation_to_index(position)
        moves = []
        for i in range(8):
            if i != row:
                moves.append((i, col))
        for j in range(8):
            if j != col:
                moves.append((row, j))
        return [GameUtils.index_to_notation(move) for move in moves]
class Bishop(Piece):
    """
    initializes bishop piece and moves
    :param color:
    """
    def __init__(self, color):
            super().__init__(color, "bishop")
    def valid_moves(self, position):
        """
        Get all valid moves for the bishop from the given position.
        """
        row, col = GameUtils.notation_to_index(position)
        moves = []
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            moves.append((i, j))
        for i, j in zip(range(row+1, 8), range(col+1, 8)):
            moves.append((i, j))
        for i, j in zip(range(row+1, 8), range(col-1, -1, -1)):
            moves.append((i, j))
        for i, j in zip(range(row-1, -1, -1), range(col+1, 8)):
            moves.append((i, j))
        return [GameUtils.index_to_notation(move) for move in moves]

class Knight(Piece):
    """
    initializes knight piece and moves
    """
    def __init__(self, color):
        super().__init__(color, "knight")
    def valid_moves(self, position):
        """
        Get all valid moves for the knight from the given position.
        """
        row, col = GameUtils.notation_to_index(position)
        possible_offsets = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                            (1, -2), (2, -1), (1, 2), (2, 1)]
        moves = [(row + r_offset, col + c_offset) for r_offset, c_offset in possible_offsets
                 if 0 <= row + r_offset < 8 and 0 <= col + c_offset < 8]
        return [GameUtils.index_to_notation(move) for move in moves]
class Pawn(Piece):
    """
    initializes pawn piece and moves
    """
    def __init__(self, color):
        super().__init__(color, "pawn")
        self.first_move = True
    def valid_moves(self, position):
        """
        Get all valid moves for the pawn from the given position.
        """
        row, col = GameUtils.notation_to_index(position)
        moves = []
        if self.color == "white":
            if row - 1 >= 0:
                moves.append((row-1, col))
            if row == 6:
                moves.append((row-2, col))
            if col - 1 >= 0:
                moves.append((row-1, col-1))
            if col + 1 < 8:
                moves.append((row-1, col+1))
        else:  # For black pawns
            if row + 1 < 8:
                moves.append((row+1, col))
            if row == 1:
                moves.append((row+2, col))
            if col - 1 >= 0:
                moves.append((row+1, col-1))
            if col + 1 < 8:
                moves.append((row+1, col+1))
        return [GameUtils.index_to_notation(move) for move in moves]

class GameUtils:
    """
    Utility class providing methods related to game operations.
    """
    @staticmethod
    def notation_to_index(notation):
        """
        Convert algebraic notation to row and column indices.
        """
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return row, col
    @staticmethod
    def index_to_notation(index):
        """
        Convert row and column indices to algebraic notation.
        """
        row, col = index
        return chr(col + ord('a')) + str(8 - row)
    @staticmethod
    def is_square_under_attack(board, square, attacking_color):
        class GameUtils:
    @staticmethod
    def is_square_under_attack(board, square, attacking_color):
        """
        Check if a given square is under attack by pieces of a given color.

        :param board: An instance of the Board class.
        :param square: A tuple (row, col) representing the square in question.
        :param attacking_color: The color of the potentially attacking pieces (e.g. 'white' or 'black').
        :return: True if the square is under attack, False otherwise.
        """

        for row in range(8):  # Assuming an 8x8 board
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == attacking_color:
                    if square in piece.get_legal_moves(board):
                        return True

        return False

