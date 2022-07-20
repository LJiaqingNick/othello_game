"""
Jiaqing(Nick) Liu
CS5001 -- Fall2021
Final project -- Milestone 2 -- Model file
This file contain all othello's model
"""
import turtle
from othello_constant import *
from view import *

class OthelloBoard:
    """
    Class OthelloBoard, to generate strating board, a dictionary
    Attribute: borad a dictionary, key is the position value is can empty, white or black
    Methods: generating_board, put_starting_tiles,
    """
    def __init__(self, number_squares):
        """
        Constructor: boad, we start with empty dictionary
        Raise ValueError is number_square is not an integer
        """
        if not isinstance(number_squares, int):
            raise ValueError("Number of square must be integer")

        self.board = {}
        self.number_squares = number_squares
        # we generate our starting board
        self.generate_board()

    def __str__(self):
        """
        Methods: __str__ print out the size of the board
        """
        return f"This is a size of {self.number_squares} X {self.number_squares} Othello Board"

    def __eq__(self, other):
        """
        Methods: __eq__ check two board size are same 
        """
        if not isinstance(other, OthelloBoard):
            return False
        return len(self.board) == len(other.board)

    def generate_board(self):
        """
        Method: generate_board a dictionary, each value start as empty
        """
        for x in range(self.number_squares):
            for y in range(self.number_squares):
                self.board[(x, y)] = EMPTY_TILE
        self.put_starting_tiles()

    def put_starting_tiles(self):
        """
        Methods: put_starting_tiles put two white tile and two black tile at middle of the board
        """
        for key in self.board.keys():
            # place White tile
            if key[0] == (int(self.number_squares / TWO) - ONE) and key[1] == int(self.number_squares / TWO): 
                self.board[key] = WHITE_TILE
            elif key[0] == int(self.number_squares / TWO) and key[1] == (int(self.number_squares / TWO) - ONE):
                self.board[key] = WHITE_TILE
            # place black tile
            elif key[0] == (int(self.number_squares / TWO) - ONE) and key[1] == (int(self.number_squares / TWO) - ONE):
                self.board[key] = BLACK_TILE
            elif key[0] == (int(self.number_squares) / TWO) and key[1] == (int(self.number_squares / TWO)):
                self.board[key] = BLACK_TILE

class Player:
    """
    Class player -- player make the move, and have their own color
    Attribute: tile_color
    Method: Make_the_move
    """

    def __init__(self, tile_color):
        """
        Constructor 
        Parameters: tile_color, player use which color of tile to play
        R
        """
        self.tile_color = tile_color
        if self.tile_color != WHITE_TILE and self.tile_color != BLACK_TILE:
            raise ValueError("Tile color must be white or black")

    def __str__(self):
        """
        Method: __str__ descripe player use which color
        """
        description = f"This player use {self.tile_color} tile to play"
        return description

    def __eq__(self, other):
        """
        Method: __eq__ check whether two player use same color tile
                always return False if other is not a player
        """
        if not isinstance(other, Player):
            return False
        return self.tile_color == other.tile_color
    
    def make_move(self, board, row_position, column_position):
        """
        Method: make_move, change the value of dictionary board
        Parameters: 
            row_position -- an integr
            column_position -- an integer
        Raise ValueError, if parameters are not integer
        """
        if not isinstance(row_position, int) or not isinstance(column_position, int):
            raise ValueError("Both Parameters must be integer")
        # place the tile on board
        board.board[row_position, column_position] = self.tile_color


class Judge:
    """
    Class Judge: decide whether game is over and valuaded player's move is legal or not,
                        also the is computer opponent
    Attributes: othello_board, player, computer, current_turn, next_turn
    Methods: receive_move, check_legal_move, check_tile_not_empty, update_graph
        convert_to_x_y_coordinate, switch_turn, count_tiles, check_the_winner,
        inform_graph_winner, find_move_next_border, pick_best_moves, find_abailable
        moves, find_max_flip_moves,
    """

    def __init__(self, othello_graph):
        """
        Constructor :
            othello_board -- an instance of OthelloBoard class
            player1 -- is an instance of Player class
            player2 -- is an instance of player cleas
            current_turn -- each time player make legal move they chage the turn
            next_turn -- each time player make legal move they chage the turn
            othello_graph -- an object of view, use for update date view
            inform_graph_draw_starting_tiles -- to starting two white tiles and 
                                                two black tiles
        Parameters:
            othello_graph -- an object, of view class
        Rasie TypeError if othello_graph is an object of OthelloGraph class
        """
        if not isinstance(othello_graph, OthelloGraph):
            raise TypeError("othello_graph must be an object of OthelloGraph class")
        # Judge prepare the starting board
        self.number_squares = NUMBER_OF_SQUARES
        self.othello_board = OthelloBoard(NUMBER_OF_SQUARES)
        # Judge create two player
        self.player = Player(BLACK_TILE)
        self.computer = Player(WHITE_TILE)
        # assign first turn to a player whose tile color is black
        self.current_turn = self.player
        self.next_turn = self.computer
        # make connection with view to update the the board
        self.othllo_graph = othello_graph
        self.inform_graph_draw_starting_tiles()
        # announce the begginning of the turn

    def __str__(self):
        """
        Method: return a string descripe the judge class
        """
        return "This is an object of class Judge"

    def __eq__(self, other):
        """
        Method: compare the oher is same type are same
        """
        return type(self) == type(other)


    def inform_graph_draw_starting_tiles(self):
        """
        Method: inform_graph_draw_starting_tiles
        """
        for key, value in self.othello_board.board.items():
            if value == WHITE_TILE:
                self.update_graph(key[0], key[1], value)
            elif value == BLACK_TILE:
                self.update_graph(key[0], key[1], value)


    def receive_move(self, row_position, column_position):
        """
        receive_move -- receive x, and y coordinate from the controller, and it's
                the start of event.
        Parameters:
            row_position -- an integer of the square row position
            column_position -- an integer of the square column position
        Raise ValueError, row_position, and column_position out of range
        """
        if row_position not in range(self.number_squares) and\
            column_position not in range(self.number_squares):
            raise ValueError("Row and column out of range!")
        self.row_position = row_position
        self.column_position = column_position
        # check the move is legal or not
        if self.check_legal_move():
            self.current_turn.make_move(self.othello_board, self.row_position, self.column_position)
            self.update_graph(self.row_position, self.column_position, self.current_turn.tile_color)
            self.flip_tiles()
            self.switch_turn()
            if not self.check_the_winner():
                self.othllo_graph.announce_turn(self.current_turn.tile_color)
                self.find_available_moves()
                self.row_position, self.column_position = self.pick_best_move()
                self.check_legal_move()
                self.current_turn.make_move(self.othello_board, self.row_position, self.column_position)
                self.update_graph(self.row_position, self.column_position, self.current_turn.tile_color)
                self.flip_tiles()
                self.switch_turn()
                if not self.check_the_winner():
                    self.othllo_graph.announce_turn(self.current_turn.tile_color)


    def pick_best_move(self):
        """
        Method -- pick_best_move, the core of computer opponent logical
        """
        # place the tile on boader
        self.find_max_flips_moves()
        self.find_moves_next_border()
        for key in self.available_moves.keys():
            if (key[0] == START_OF_ROW or key[0] == END_OF_ROW) \
                and (key[1] == START_OF_COLUMN or key[1] == END_OF_COLUMN):
                if key in self.max_flips_moves:
                    return key[0], key[1]

        for key in self.available_moves.keys():
            if (key[0] == START_OF_ROW or key[0] == END_OF_ROW) \
                and (key[1] == START_OF_COLUMN or key[1] == END_OF_COLUMN):
                return key[0], key[1]

        for key in self.available_moves.keys():
            if (key[0] == START_OF_ROW or key[0] == END_OF_ROW) and (key in self.max_flips_moves):
                return key[0], key[1]

        for key in self.available_moves.keys():
            if (key[1] == START_OF_COLUMN or key[1] == END_OF_COLUMN) and (key in self.max_flips_moves):
                return key[0], key[1]

        for key in self.available_moves.keys():
            if key[0] == START_OF_ROW or key[0] == END_OF_COLUMN \
                or key[1] == START_OF_COLUMN or key[1] == END_OF_COLUMN:
                return key[0], key[1]

        # Avoid second border
        for key in self.available_moves.keys():
            if key not in self.next_border_moves and key in self.max_flips_moves:
                return key[0], key[1]

        for key, value in self.available_moves.items():
            for count in self.flip_tiles_count_list:
                if value == count and key not in self.next_border_moves:
                    return key[0], key[1]

        return self.max_flips_moves[0][0], self.max_flips_moves[0][1]
            
    def find_moves_next_border(self):
        """
        Method: find_moves_next_border, find all the moves that close to the border
        """
        self.next_border_moves = []
        for key in self.available_moves.keys():
            if key[0] == START_OF_ROW + 1 or key[0] == END_OF_ROW - 1 \
                or key[1] == START_OF_COLUMN +1 or key[1] == END_OF_ROW -1:
                self.next_border_moves.append(key)
    
    def find_max_flips_moves(self):
        """
        Methods: find_max_flips_moves, find all the moves has maximum amount flip
        """
        self.max_flips_moves = []
        max_flips = max(self.available_moves.values())
        for key, value in self.available_moves.items():
            if max_flips == value:
                self.max_flips_moves.append(key)

    def find_available_moves(self):
        """
        Methods: find_available_moves, find all the possible moves on the board
        """
        self.available_moves = {}
        self.flip_tiles_count_list = []
        # put all the available , values is number of tiles can flip
        for key, value in self.othello_board.board.items():
            if value == EMPTY_TILE:
                self.row_position = key[0]
                self.column_position = key[1]
                if self.check_legal_move():
                    self.available_moves[(self.row_position, self.column_position)] = len(self.flip_list)
                    self.flip_tiles_count_list.append(len(self.flip_list))
        self.flip_tiles_count_list.sort(reverse=True)


    def flip_tiles(self):
        """
        MethodL flip_tiles in the flip_list
        """
        for item in self.flip_list:
            self.othello_board.board[item[0], item[1]] = self.current_turn.tile_color
            self.update_graph(item[0], item[1], self.current_turn.tile_color)

    def update_graph(self, row, column, tile_color):
        """
        Method: update_graph tell the OthelloGraph to draw the legal tile
        Rasie ValueError, row and column not in range
                ValueError, if tile_color is white, and black
        """
        if row not in range(NUMBER_OF_SQUARES) or column not in range(NUMBER_OF_SQUARES):
            raise ValueError("Row and column not in range")
        if tile_color != WHITE_TILE and tile_color != BLACK_TILE:
            raise ValueError("Tile_color must white or black")
        new_x, new_y = self.convert_to_x_y_coordinate(row, column)

        # othello_graph receive the instruction
        self.othllo_graph.receive_instruction(new_x, new_y, tile_color)

    def convert_to_x_y_coordinate(self, row, column):
        """
        Method: convert row position and column position into x and y coordinate
        Parameters:
            row -- an integer,
            column -- an integer
        Return:
            new_x, a float
            new_y, a float
        Raise ValueError if row and column not in range
        """
        if row not in range(NUMBER_OF_SQUARES) or column not in range(NUMBER_OF_SQUARES):
            raise ValueError("row or column out of range")
        new_x = (row - NUMBER_OF_SQUARES / TWO) * SQUARE_LENGTH + SQUARE_LENGTH / TWO
        new_y = (column - NUMBER_OF_SQUARES / TWO) * SQUARE_LENGTH + Y_POSITION_DIFFERENCE_BETWEEN_CYCLE
        return new_x, new_y


    def switch_turn(self):
        """
        Method -- switch_turn swape the turn for current_turn and next_turn
        Parameters: None
        Return: None
        """
        tempory_turn = self.current_turn
        self.current_turn = self.next_turn
        self.next_turn = tempory_turn

    def check_left_side(self):
        """
        Method: check_left_side
        Parameters: None
        Return: None
        """
        if self.row_position > START_OF_ROW:
            if self.othello_board.board[self.row_position - 1, self.column_position] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_left_side_recursively(self.row_position - 1):
                    self.append_flip_list()
                    self.is_valid_move = True

    def check_left_bottom_side(self):
        """
        Method: check_left_bottom_side
        Parameters: None
        Return: None
        """
        if self.row_position > START_OF_ROW and self.column_position > START_OF_COLUMN: 
            if self.othello_board.board[self.row_position -1, self.column_position -1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_left_bottom_side_recursively(self.row_position - 1, self.column_position -1):
                    self.append_flip_list()
                    self.is_valid_move = True


    def check_left_top_side(self):
        """
        Method: check_left_top_side
        Parameters: None
        Return None
        """
        if self.row_position > START_OF_ROW and self.column_position < END_OF_COLUMN:
            if self.othello_board.board[self.row_position - 1, self.column_position + 1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_left_top_side_recursively(self.row_position - 1, self.column_position + 1):
                    self.append_flip_list()
                    self.is_valid_move = True

    def check_bottom_side(self):
        """
        Method: check_bottom_side
        Parameters: None
        Return: None
        """
        if self.column_position > START_OF_COLUMN:
            if self.othello_board.board[self.row_position, self.column_position - 1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_bottom_side_recursively(self.column_position - 1):
                    self.append_flip_list()
                    self.is_valid_move = True
    
    def check_top_side(self):
        """
        Method: check_top_side
        Parameters: None
        Return: None
        """
        if self.column_position < END_OF_COLUMN:
            if self.othello_board.board[self.row_position, self.column_position + 1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_top_side_recursively(self.column_position + 1):
                    self.append_flip_list()
                    self.is_valid_move = True
    
    def check_right_side(self):
        """
        Methond: check_right_side
        Parameters: None
        Retrun: None
        """
        if self.row_position < END_OF_ROW:
            if self.othello_board.board[self.row_position + 1, self.column_position] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_right_side_recursively(self.row_position + 1):
                    self.append_flip_list()
                    self.is_valid_move = True

    def check_right_bottom_side(self):
        """
        Method: check_right_bottom_side
        Parameters: None
        Return: None
        """
        if self.row_position < END_OF_ROW and self.column_position > START_OF_COLUMN:
            if self.othello_board.board[self.row_position +1, self.column_position -1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_right_bottom_side_recursively(self.row_position +1, self.column_position -1):
                    self.append_flip_list()
                    self.is_valid_move = True
    
    def check_right_top_side(self):
        """
        Method: check_tight_top_side
        Parameters: None
        Return: None
        """
        if self.row_position < END_OF_ROW and self.column_position < END_OF_COLUMN:
            if self.othello_board.board[self.row_position +1, self.column_position + 1] == self.next_turn.tile_color:
                self.temp_flip_list = []
                if self.check_right_top_side_recursively(self.row_position + 1, self.column_position + 1):
                    self.append_flip_list()
                    self.is_valid_move = True

    def check_legal_move(self):
        """
        Method -- Check whtether this move is legal or not
        Parameters: None
        Return: boolean value
        """
        self.is_valid_move = False
        if self.check_tile_empty():
            self.flip_list = []
            self.check_left_side()
            self.check_left_bottom_side()
            self.check_left_top_side()
            self.check_bottom_side()
            self.check_top_side()
            self.check_right_side()
            self.check_right_bottom_side()
            self.check_right_top_side()
        return self.is_valid_move

    def append_flip_list(self):
        """
        Method: append_flip_list
                append tempory tiles that need to be flip into flip list
        Parameters: None
        Return: None
        """
        for item in self.temp_flip_list:
            self.flip_list.append(item)

    def check_right_top_side_recursively(self, row, column):
        """
        Method: check_right_top_side_recursively
                check right side recursively until reach the edge of board, if all the tiles meet 
                legal move condition.
        Parameters:
            row -- an interger
            column -- an integer
        """
        if (row == END_OF_ROW or column == END_OF_COLUMN) \
            and self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        elif (row == END_OF_ROW or column == END_OF_COLUMN) \
            and self.othello_board.board[row, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([row, column])
            return self.check_right_top_side_recursively(row + 1, column + 1)


    def check_right_bottom_side_recursively(self, row, column):
        """
        Method: check_right_bottom_side_recursively
                check right bottom side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            row -- an interger
            column -- an integer
        """
        if (row == END_OF_ROW or column == START_OF_COLUMN) \
            and self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        elif (row == END_OF_ROW or column == START_OF_COLUMN) \
            and self.othello_board.board[row, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([row, column])
            return self.check_right_bottom_side_recursively(row + 1, column - 1)

    def check_right_side_recursively(self, row):
        """
        Method: check_right_side_recursively
                check right side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            row -- an interger
        """
        if row == END_OF_ROW and self.othello_board.board[row, self.column_position] == self.current_turn.tile_color:
            return True
        elif row == END_OF_ROW and self.othello_board.board[row, self.column_position] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, self.column_position] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, self.column_position] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([row, self.column_position])
            return self.check_right_side_recursively(row + 1)

    def check_top_side_recursively(self, column):
        """
        Method: check_top_side_recursively
                check top side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            column -- an interger
        """
        if column == END_OF_COLUMN and self.othello_board.board[self.row_position, column] == self.current_turn.tile_color:
            return True
        elif column == END_OF_COLUMN and self.othello_board.board[self.row_position, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[self.row_position, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[self.row_position, column] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([self.row_position, column])
            return self.check_top_side_recursively(column + 1)


    def check_bottom_side_recursively(self, column):
        """
        Method: check_bottom_side_recursively
                check bottom side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            column -- an interger
        """
        if column == START_OF_COLUMN and self.othello_board.board[self.row_position, column] == self.current_turn.tile_color:
            return True
        elif column == START_OF_COLUMN and self.othello_board.board[self.row_position, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[self.row_position, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[self.row_position, column] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([self.row_position, column])
            return self.check_bottom_side_recursively(column - 1)


    def check_left_top_side_recursively(self, row, column):
        """
        Method: check_top_side_recursively
                check top side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            row -- an integer
            column -- an integer
        """
        if (row == START_OF_ROW or column == END_OF_COLUMN) \
            and self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        elif (row == START_OF_ROW or column == END_OF_COLUMN) \
            and self.othello_board.board[row, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        else:
            # recursively check left top side
            self.temp_flip_list.append([row, column])
            return self.check_left_top_side_recursively(row - 1, column + 1)

    def check_left_bottom_side_recursively(self, row, column):
        """
        Method: check_left_bottom_side_recursively
                check left_bottom side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            row -- an integer
            column -- an integer
        """
        if (row == START_OF_ROW or column == START_OF_COLUMN) \
            and self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        elif (row == START_OF_ROW or column == START_OF_COLUMN) \
            and self.othello_board.board[row, column] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, column] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, column] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([row, column])
            # recursively check left bottom side valid 
            return self.check_left_bottom_side_recursively(row - 1, column - 1)

    def check_left_side_recursively(self, row):
        """
        Method: check_left_side_recursively
                check left side recursively until reach the edge of board, if all the tiles meet 
                legal move condition we add tiles in flip list.
        Parameters:
            row -- an integer
        """
        if row == START_OF_ROW and \
            self.othello_board.board[row, self.column_position] == self.current_turn.tile_color:
            return True
        elif row == START_OF_ROW and self.othello_board.board[row, self.column_position] != self.current_turn.tile_color:
            return False
        elif self.othello_board.board[row, self.column_position] == EMPTY_TILE:
            return False
        elif self.othello_board.board[row, self.column_position] == self.current_turn.tile_color:
            return True
        else:
            self.temp_flip_list.append([row, self.column_position])
            # recusively check left side valid
            return self.check_left_side_recursively(row - 1)

    def check_tile_empty(self):
        """
        Method -- to check the tile is empty or not
        Return: boolean value
        """
        if self.othello_board.board[self.row_position, self.column_position] == EMPTY_TILE:
            return True
        else:
            return False

    def count_tiles(self):
        """
        Method: counting the tiles for white , black, and empty
        Return:
            empty_count, an integer the number of empty tile
            black_count, an integer the number of black tiles
        """
        empty_count = ZERO
        black_count = ZERO
        white_count = ZERO
        for value in self.othello_board.board.values():
            if value == EMPTY_TILE:
                empty_count += ONE
            elif value == BLACK_TILE:
                black_count += ONE
            elif value == WHITE_TILE:
                white_count += ONE
        return empty_count, black_count, white_count

    def check_the_winner(self):
        """
        Method: check_game_over
        Return: True or false, if game is ove
        """
        empty_count, black_count, white_count = self.count_tiles()
        if empty_count == ZERO or self.check_no_legal_move_left():
            if black_count > white_count:
                winner = BLACK_TILE
                self.inform_graph_announce_winner(winner, black_count)
                self.store_winner_score_name(black_count)
            elif black_count < white_count:
                winner = WHITE_TILE
                self.inform_graph_announce_winner(winner, white_count)
                self.store_winner_score_name(black_count)
            elif black_count == white_count:
                winner = EMPTY_TILE
                self.inform_graph_announce_winner(winner, black_count)
                self.store_winner_score_name(black_count)
            return True
        return False

    def store_winner_score_name(self, black_count):
        """
        Method: store_winner_score_name
        Parameters: black_count -- a integer
        Raise ValueError if black_count not an integer
        """
        if not isinstance(black_count, int):
            raise ValueError("black_count must be an integer")
        player_name = input("What's your name?").strip().title()
        file_content, int_scores_list = self.read_file()
        if len(int_scores_list) == 0:
            file_content = player_name + " " + str(black_count) + "\n"
        elif black_count > max(int_scores_list):
            file_content = player_name + " " + str(black_count) + "\n" + file_content
        else:
            file_content = file_content + player_name + " " + str(black_count) + "\n"  
        self.write_file(file_content)

    def write_file(self, file_content):
        """
        Method: write_file, write the file content into file
        Parameters: file_content, a string
        Return: None
        Raise TypeError, if file_content not a string
        """
        if not isinstance(file_content, str):
            raise TypeError("File_content must be string")
        with open(FILE_NAME, "w") as file:
            file.write(file_content)

    def read_file(self):
        """
        Method: read the file
        Parameters: None
        Return: file_content -- a string
                int_scores_list -- a list, with integer in it
        """
        with open(FILE_NAME, "r") as file:
            file_content = file.read()
        if len(file_content) == 0:
            int_scores_list = [0]
        else:
            content_list = file_content.split() 
            scores_list = content_list[1::2]
            int_scores_list = []
            for item in scores_list:
                int_scores_list.append(int(item))
        return file_content, int_scores_list



    def check_no_legal_move_left(self):
        """
        Method: check_no_legal_move_left
                use for loop on the board dcitionary to check every empty tile if there is any
                legal move left
        Parameters: None
        Return boolean value
        """
        for key, value in self.othello_board.board.items():
            if value == EMPTY_TILE:
                self.row_position = key[0]
                self.column_position = key[1]
                if self.check_legal_move():
                    return False
        return True

    def inform_graph_announce_winner(self, winner, tiles_count):
        """
        Method: infor_graph_announce_winner, pass the winner and tile count
        Parameters: winner -- who win the game
                    tiles_count -- winner's tile count
        Raise ValueError if winner not string, or tiles_count not an integer
        """
        if not isinstance(winner, str) or not isinstance(tiles_count, int):
            raise ValueError("winner must be string, and tiles_count must be integer")
        if winner == EMPTY_TILE:
            winner_description = f"It's a TIE!! There are {tiles_count} of each!"
        else:
            winner_description = f"The winner is {winner}, and {winner} has {tiles_count} tiles."

        self.othllo_graph.announce_winner(winner_description)

