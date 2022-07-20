"""
Jiaqing(Nick)
CS5001 -- Fall2021
Final project -- Milestone 2 -- othello_test
"""
import turtle
from controller import *
from model import *
from view import *
from othello_constant import *
import unittest

# test model classes
class TestJudge(unittest.TestCase):

    def setUp(self):
        screen = turtle.Screen()
        othello_graph = OthelloGraph(screen)
        self.othello_judge = Judge(othello_graph)
        controller = Controller(self.othello_judge, screen)
        self.othello_judge.temp_flip_list = []
        self.othello_judge.flip_list =[]
        self.othello_judge.is_valid_move = False

    def test__str__(self):
        self.assertEqual(str(self.othello_judge), "This is an object of class Judge")

    def test_judge_init(self):
        self.assertEqual(self.othello_judge.number_squares, 8)
        self.assertEqual(type(self.othello_judge.player), Player)
        self.assertEqual(type(self.othello_judge.computer), Player)
        self.assertEqual(type(self.othello_judge.othello_board), OthelloBoard)
    
    def test_flip_tiles(self):
        self.othello_judge.flip_list.append((0, 0))
        self.othello_judge.flip_tiles()
        self.assertEqual(self.othello_judge.othello_board.board[(0, 0)], "black")

    def test_init_raise_error(self):
        with self.assertRaises(TypeError):
            othello_judge = Judge("a")
    
    def test_receive_move_raise_error_out_range(self):
        with self.assertRaises(ValueError):
            self.othello_judge.receive_move(100, 55)

    def test_update_graph_raise_error(self):
        with self.assertRaises(ValueError):
            self.othello_judge.update_graph(200, 300, "black")
        with self.assertRaises(ValueError):
            self.othello_judge.update_graph(4, 4, "pink")

    def test_convert_to_x_y_coordinate_raise_error(self):
        with self.assertRaises(ValueError):
            self.othello_judge.convert_to_x_y_coordinate(200, 100)
    
    def test_convert_to_x_y_coordinate_raise_error(self):
        new_x, new_y = self.othello_judge.convert_to_x_y_coordinate(3, 3)
        self.assertEqual(new_x, -25.0)
        self.assertEqual(new_y, -45)

    def test_switch_turn(self):
        self.othello_judge.switch_turn()
        self.assertEqual(self.othello_judge.current_turn.tile_color, "white")
        self.assertEqual(self.othello_judge.next_turn.tile_color, "black")

    def test_check_left_side_true(self):
        self.othello_judge.row_position = 5
        self.othello_judge.column_position = 3
        self.othello_judge.check_left_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_left_top_side_true(self):
        self.othello_judge.othello_board.board[2,5] = "black"
        self.othello_judge.row_position = 5
        self.othello_judge.column_position = 2
        self.othello_judge.check_left_top_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_left_bottom_side_true(self):
        self.othello_judge.othello_board.board[2,3] = "black"
        self.othello_judge.row_position = 4
        self.othello_judge.column_position = 5
        self.othello_judge.check_left_bottom_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_left_top_side_true(self):
        self.othello_judge.othello_board.board[2,5] = "black"
        self.othello_judge.row_position = 5
        self.othello_judge.column_position = 2
        self.othello_judge.check_left_top_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_bottom_side_true(self):
        self.othello_judge.row_position = 3
        self.othello_judge.column_position = 5
        self.othello_judge.check_bottom_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_top_side_true(self):
        self.othello_judge.row_position = 4
        self.othello_judge.column_position = 2
        self.othello_judge.check_top_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_right_sidez_true(self):
        self.othello_judge.row_position = 2
        self.othello_judge.column_position = 4
        self.othello_judge.check_right_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_right_bottom_side_true(self):
        self.othello_judge.othello_board.board[5,2] = "black"
        self.othello_judge.row_position = 2
        self.othello_judge.column_position = 5
        self.othello_judge.check_right_bottom_side()
        self.assertEqual(self.othello_judge.is_valid_move, True)

    def test_check_right_top_side_true(self):
        self.othello_judge.othello_board.board[4,5] = "black"
        self.othello_judge.row_position = 2
        self.othello_judge.column_position = 3
        self.othello_judge.check_right_top_side()

    def test_check_legal_move_true(self):
        self.othello_judge.row_position = 5
        self.othello_judge.column_position = 3
        self.assertEqual(self.othello_judge.check_legal_move(), True)

    def test_check_legal_move_False(self):
        self.othello_judge.row_position = 7
        self.othello_judge.column_position = 3
        self.assertEqual(self.othello_judge.check_legal_move(), False)

    def test_append_flip_list(self):
        self.othello_judge.temp_flip_list = [(1, 3)]
        self.othello_judge.append_flip_list()
        self.assertEqual(len(self.othello_judge.flip_list), 1)

    def test_check_right_top_side_recursively_true(self):
        self.othello_judge.othello_board.board[5, 4] = "black"
        self.assertEqual(self.othello_judge.check_right_top_side_recursively(4, 3), True)

    def test_check_right_bottom_side_recursively_true(self):
        self.othello_judge.othello_board.board[5, 2] = "black"
        self.assertEqual(self.othello_judge.check_right_bottom_side_recursively(3, 4), True)

    def test_check_right_bottom_side_recursively_false(self):
        self.othello_judge.othello_board.board[1, 2] = "black"
        self.assertEqual(self.othello_judge.check_right_bottom_side_recursively(3, 7), False)

    def test_check_right_side_recursively_true(self):
        self.othello_judge.column_position = 4
        self.assertEqual(self.othello_judge.check_right_side_recursively(3), True)

    def test_check_top_side_recursively_true(self):
        self.othello_judge.row_position = 4
        self.assertEqual(self.othello_judge.check_top_side_recursively(3), True)

    def test_check_bottom_side_recursively_true(self):
        self.othello_judge.row_position = 3
        self.assertEqual(self.othello_judge.check_bottom_side_recursively(4), True)

    def test_find_available_moves(self):
        self.othello_judge.find_available_moves()
        self.assertEqual(len(self.othello_judge.flip_tiles_count_list), 4)
    
    def test_pick_best_move(self):
        self.othello_judge.find_available_moves()
        row, column = self.othello_judge.pick_best_move()
        self.assertEqual(row, 2)
        self.assertEqual(column, 4)

    def test_write_file_raise_error(self):
        with self.assertRaises(TypeError):
            self.othello_judge.write_file(1)

    def test_read_file(self):
        file_content, int_scores_list = self.othello_judge.read_file()
        self.assertEqual(type(file_content), str)
        self.assertEqual(type(int_scores_list), list)

    def test_find_max_flips_moves(self):
        self.othello_judge.find_available_moves()
        self.othello_judge.find_max_flips_moves()
        self.assertEqual(len(self.othello_judge.max_flips_moves), 4)

    def test_find_moves_next_border(self):
        self.othello_judge.find_available_moves()
        self.othello_judge.find_moves_next_border()
        self.assertEqual(len(self.othello_judge.next_border_moves), 0)

    def test_check_left_top_side_recursively_true(self):
        self.othello_judge.othello_board.board[2, 5] = "black"
        self.assertEqual(self.othello_judge.check_left_top_side_recursively(4, 3), True)

    def test_check_left_bottom_side_recursively_true(self):
        self.othello_judge.othello_board.board[3, 2] = "black"
        self.assertEqual(self.othello_judge.check_left_bottom_side_recursively(4, 3), True)

    def test_check_left_side_recursively_true(self):
        self.othello_judge.column_position = 3
        self.assertEqual(self.othello_judge.check_left_side_recursively(4), True)
        
    def test_check_tile_empty_true(self):
        self.othello_judge.row_position = 0
        self.othello_judge.column_position = 0
        self.assertEqual(self.othello_judge.check_tile_empty(), True)

    def test_check_tile_empty_false(self):
        self.othello_judge.row_position = 3
        self.othello_judge.column_position = 3
        self.assertEqual(self.othello_judge.check_tile_empty(), False)

    def test_count_tiles(self):
        empty_count, black_count, white_count = self.othello_judge.count_tiles()
        self.assertEqual(empty_count, 60)
        self.assertEqual(black_count, 2)
        self.assertEqual(white_count, 2)

    def test_check_no_legal_move_left_true(self):
        for key, value in self.othello_judge.othello_board.board.items():
            self.othello_judge.othello_board.board[key] = "white"
        self.othello_judge.othello_board.board[0,0] = "empty"
        self.assertEqual(self.othello_judge.check_no_legal_move_left(), True)
    
    def test_check_no_legal_move_left_false(self):
        self.assertEqual(self.othello_judge.check_no_legal_move_left(), False)

    def test_check_store_winner_score_name_raise_error(self):
        with self.assertRaises(ValueError):
            self.othello_judge.store_winner_score_name("1")

    def test_inform_graph_announce_winner_raise_error(self):
        with self.assertRaises(ValueError):
            self.othello_judge.inform_graph_announce_winner(1, "3")
    

class TestOthelloBoard(unittest.TestCase):

    def setUp(self):
        self.othello_board = OthelloBoard(8)

    def test_init_board_size0(self):
        test_board0 = OthelloBoard(0)
        self.assertEqual(test_board0.board, {})

    def test_init_board_size_2(self):
        test_board2 = OthelloBoard(2)
        self.assertEqual(test_board2.board, {(0, 0): 'black', (0, 1): 'white', (1, 0): 'white', (1, 1): "black"})

    def test_init(self):
        self.assertEqual(self.othello_board.number_squares, 8)
        self.assertEqual(self.othello_board.board[3,4], "white")
        self.assertEqual(self.othello_board.board[4,4], "black")

    def test_str(self):
        self.assertEqual(str(self.othello_board), "This is a size of 8 X 8 Othello Board")

    def test_eq_false(self):
        self.assertEqual(self.othello_board == "a", False)

    def test_generate_board(self):
        self.assertEqual(len(self.othello_board.board), 64)

    def test_put_starting_tiles(self):
        self.assertEqual(self.othello_board.board[3,4], "white")

class TestPlayer(unittest.TestCase):

    def test_init_raise_error(self):
        with self.assertRaises(ValueError):
            player1 = Player("empty")

    def test_init(self):
        player2 = Player("white")
        self.assertEqual(player2.tile_color, "white")

    def test_str(self):
        player3 = Player("black")
        self.assertEqual(str(player3), "This player use black tile to play") 

    def test_eq_true(self):
        player4 = Player("black")
        other = Player("black")
        self.assertTrue(player4 == other)

    def test_eq_false(self):
        player5 = Player("black")
        other = Player("white")
        self.assertFalse(player5 == other)

    def test_make_move_raise_error(self):
        with self.assertRaises(ValueError):
            player7 = Player("black")
            a = {}
            player7.make_move(a, 3, "3")

# controler

class TestController(unittest.TestCase):

    def setUp(self):
        screen = turtle.Screen()
        othello_graph = OthelloGraph(screen)
        othello_judge = Judge(othello_graph)
        self.controller = Controller(othello_judge, screen)
    
    def test_init_raise_error(self):
        with self.assertRaises(TypeError):
            test_controller = Controller(1, 2)

    def test_str(self):
        self.assertEqual(str(self.controller), "This is an Othello game controller.")

    def test_eq_true(self):
        screen = turtle.Screen()
        othello_graph = OthelloGraph(screen)
        othello_judge = Judge(othello_graph)
        other = Controller(othello_judge, screen)
        self.assertTrue(self.controller == other)

    def test_eq_false(self):
        self.assertFalse(self.controller == 1)

    def test_get_click_raise_error(self):
        with self.assertRaises(ValueError):
            self.controller.get_click("1", "2")

    def test_convert_click_to_row_column(self):
        row, column = self.controller.convert_click_to_row_column(75, 125)
        self.assertEqual(row, 5)
        self.assertEqual(column, 6)

    def test_check_row_column_in_range_true(self):
        self.assertTrue(self.controller.check_row_column_in_range(1, 1))

    def test_check_row_column_in_range_false(self):
        self.assertFalse(self.controller.check_row_column_in_range(100, -100))

    def test_inform_judge_raise_error(self):
        with self.assertRaises(ValueError):
            self.controller.inform_judge(100, -33)
        

def main():
    unittest.main(verbosity = 3)


if __name__ == "__main__":
    main()
