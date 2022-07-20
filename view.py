"""
Jiaqing(Nick) Liu
CS5001 -- Fall2021
Final project -- Milestone 2 -- View file
This file contain all othello's view
"""
import turtle
from model import *
from othello_constant import *


class OthelloGraph:
    """
    Class OthelloGraph
    Attributes: screen, turtle_object
    Methods: receive_instructiond, announce_winner
    """
    def __init__(self, screen):
        """
        Constructor:
            screen -- object of turtle screen
            turtle_object -- is the object of turtle
        Raise TypeError is screen and turtle_object not instance of turtle screen or turtle
        """
        if not isinstance(screen, turtle._Screen): 
            raise TypeError("Parameter1 must be object of turtle screen") 
        self.othello_screen = OthelloScreen(screen)
        self.othello_turtle = OthelloTurtle()
    
    def __str__(self):
        """
        Method -- descripe what is OthelloGraph
        """
        description = "This is Othello game graph"
        return description

    def __eq__(self, other):
        """
        Method -- compare two OthelloGraph are the same object
        """
        return type(self) == type(other)

    def receive_instruction(self, x_coordinate, y_coordinate, tile_color):
        """
        Method -- Model will use this method pass x, y and tile color to update the ve
        Parameters:
            x_coordinate -- x coordination
            y_coordinate -- y coordination
            tile_color -- color of tile
        """
        # use turtle to draw
        self.othello_turtle.draw_tile_on_board(x_coordinate, y_coordinate, tile_color)
    
    def announce_turn(self, tile_color):
        """
        Method -- announce_turn, print out current turn's color
        Parameterts: tile_color
        Raise: ValueError, if tile_color is not white or black
        """
        if tile_color != WHITE_TILE and tile_color != BLACK_TILE:
            raise ValueError("tile_color must be white and black")
        print(f"Current turn is {tile_color}")

    def announce_winner(self, winner_description):
        """
        Method: announce_winner, model will call this method, and
                let view print out the winner of this game
        """
        print("Game over!")
        print(winner_description)


class OthelloTurtle:
    """
    Class OthelloTurtle
    Attributes: turtle_object
    Methods:
    """
    def __init__(self):
        """
        Constructor
        Parameters:
            turtle_object -- an object of turtle
        """
        self.bottom_left_corner = -NUMBER_OF_SQUARES * SQUARE_LENGTH / TWO
        self.othello_turtle = turtle.Turtle()
        self.prepare_turtle()
        self.draw_board()

    def __str__(self):
        """
        Method: __str__ return a string to descripe turtle's current pen color
        """
        pen_color = self.othello_turtle.pencolor()
        return f"Current pen color is {pen_color}"

    def __eq__(self, other):
        """
        Method -- check two OthelloTurtle have same color, if other not an instance
                of OthelloTurtle will always return False
        """
        if not isinstance(other, OthelloTurtle):
            return False
        return self.othello_turtle.pencolor() == other.othello_turtle.pencolor()

    def prepare_turtle(self):
        """
        Method: prepare_turtle -- set turtle speed and hide turtle, also set turtle color
        """
        self.othello_turtle.penup()
        self.othello_turtle.speed(MAX_SPEED)
        self.othello_turtle.hideturtle()
        # draw line color in black and fill in green
        self.othello_turtle.color(PEN_COLOR, BOARD_BACKGROUND_COLOR)

    def draw_circle(self, tile_color):
        """
        Methos: draw_circle -- draw a circle fill with specific color
        Parameters:
            tile_color -- color of the circle
        Raise error tile_color is not white or black
        """
        # set fill color
        if tile_color != WHITE_TILE and tile_color != BLACK_TILE:
            raise ValueError("parameter must be white or black")
        self.othello_turtle.fillcolor(tile_color)
        self.othello_turtle.begin_fill()
        self.othello_turtle.pendown()
        self.othello_turtle.circle(RADIUS)
        self.othello_turtle.end_fill()
        self.othello_turtle.penup()

    def draw_tile_on_board(self, x_coordinate, y_coordinate, tile_color):
        """
        Method -- draw an tile on the board
        """
        self.othello_turtle.setposition(x_coordinate, y_coordinate)
        self.draw_circle(tile_color)


    def draw_board(self):
        """
        Method -- draw the board on the screen
        """
        self.othello_turtle.setposition(self.bottom_left_corner, self.bottom_left_corner)
        self.draw_background()
        self.draw_horizontial_lines()
        self.draw_vertical_lines()

    def draw_horizontial_lines(self):
        """
        Methods -- draw the horizontial lines of the board
        """
        for i in range(NUMBER_OF_SQUARES + ONE):
            self.othello_turtle.setposition(self.bottom_left_corner, SQUARE_LENGTH * i + self.bottom_left_corner)
            self.draw_lines()

    def draw_vertical_lines(self):
        """
        Method -- draw verical line on board
        """
        self.othello_turtle.left(TURN)
        for i in range(NUMBER_OF_SQUARES + 1):
            self.othello_turtle.setposition(SQUARE_LENGTH * i + self.bottom_left_corner, self.bottom_left_corner)
            self.draw_lines()
        self.othello_turtle.right(TURN)

    def draw_background(self):
        """
        Method: draw th background on board
        """
        self.othello_turtle.begin_fill()
        for i in range(FOUR_SIDE_SQUARE):
            self.othello_turtle.pendown()
            self.othello_turtle.forward(SQUARE_LENGTH * NUMBER_OF_SQUARES)
            self.othello_turtle.left(TURN)
        self.othello_turtle.end_fill()
        self.othello_turtle.penup()

    def draw_lines(self):
        """
        Method: draw straight forward line
        """
        self.othello_turtle.pendown()
        self.othello_turtle.forward(SQUARE_LENGTH * NUMBER_OF_SQUARES)
        self.othello_turtle.penup()


class OthelloScreen:
    """
    Class OthelloScreen
    Attributes: screen 
    Methods: initalize_screen
    """

    def __init__(self, screen):
        """
        Constructor
        Parameters:
            screen -- an object of turtle screen
        Raise Error:
            TypeError, if screen is not the object fo turtle screen
        """
        if not isinstance(screen, turtle._Screen):
            raise TypeError("Screen is not the correct type")
        self.othello_screen = screen
        self.initalize_screen()

    def __str__(self):
        """
        return a string that descripes the type of the object
        """
        return "This is an object of Class OthelloScreen"

    def __eq__(self, other):
        """
        Compare other is the object OthelloScreen
        """
        return type(self) == type(other)

    def initalize_screen(self):
        """
        Method: inistalize_screen -- set turtle window size, then set scrreen size, and bg color
        """
        self.othello_screen.setup(NUMBER_OF_SQUARES * SQUARE_LENGTH + SQUARE_LENGTH, 
        NUMBER_OF_SQUARES * SQUARE_LENGTH + SQUARE_LENGTH)
        self.othello_screen.screensize(NUMBER_OF_SQUARES * SQUARE_LENGTH, NUMBER_OF_SQUARES * SQUARE_LENGTH)
        self.othello_screen.bgcolor(SCREEN_BACKGROUND_COLOR)
