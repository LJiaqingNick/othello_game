"""
Jiaqing(Nick) Liu
CS5001 -- Fall2021
Final project -- Milestone 2 -- Controller file
This file contain all othello's model
"""
from othello_constant import *
from model import *
import turtle

class Controller:
    """
    Class Controller -- the controller of the othello board
    Attributes: judge -- the object of main Model class 
                screen -- turtle_screen
    Methods: get_click, convert_click, check_row_column_in_range,
            inform_judge
    """

    def __init__(self, judge, screen):
        """
        Constructor of controller
        Parameter: judge -- an object of Judge class in model.py
                    screen -- an object of turtle screen
                
        Raise TypeError, judge is not the class of Judge
        """
        if not isinstance(judge, Judge) or not isinstance(screen, turtle._Screen):
            raise TypeError("Wrong type of parameters")
        screen.onclick(self.get_click)
        self.judge = judge

    def __str__(self):
        """
        Method: __str__ return this object description
        """
        return "This is an Othello game controller."

    def __eq__(self, other):
        """
        Method: compare two controller are the same type
        """
        return type(self) == type(other)

    def get_click(self, x, y):
        """
        Method: get_click to recive the x and y coordinate from user click
        Parameters: x, is x_coordinate
                 y, is y_coordinate
        Raise ValueError if x and y is not integer of float
        """
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError("x coordinate must be integer or float")
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError("y coordinate must be integer or float")
        # assign x and y as attribute in controller

        # we call the mehod convert x and y to the idex value in our dictionary board
        row, column = self.convert_click_to_row_column(x, y)
        # we check whether row and column is in range
        if self.check_row_column_in_range(row, column):
            # if it's in range we  start passing the row and column to judge
            self.inform_judge(row, column)

    def convert_click_to_row_column(self, x, y):
        """
        Method: convert_click, conver x_coordinate and y_coordiate into row and column
        Parameters:
            x -- a float x_coordinate
            y -- a float y_coordinate
        """
        row = int(x // SQUARE_LENGTH + NUMBER_OF_SQUARES / TWO)
        column = int(y // SQUARE_LENGTH + NUMBER_OF_SQUARES / TWO)
        return row, column

    def check_row_column_in_range(self, row, column):
        """
        Method: check_row_column_in_range,
        Return: boolean value
        """
        return row in range(NUMBER_OF_SQUARES) and column in range(NUMBER_OF_SQUARES)

    def inform_judge(self, row, column):
        """
        Method: inform_judge, this is our only connection to the model, we passing 
                the row and column to judge
        Raise Error:
            ValueErroe if row and column not in range
        """
        if row not in range(NUMBER_OF_SQUARES) and column not in range(NUMBER_OF_SQUARES):
            raise ValueError("row and column not in range!")
        self.judge.receive_move(row, column)
