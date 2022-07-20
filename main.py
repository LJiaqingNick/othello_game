import turtle
from othello_constant import *
from model import *
from controller import *
from view import *


def main():
    try:
        screen = turtle.Screen()
        othello_graph = OthelloGraph(screen)
        othello_judge = Judge(othello_graph)
        controller = Controller(othello_judge, screen)
    except FileNotFoundError:
        print("File Not Found")
    except PermissionError:
        print("You don't have permission to read or wrtie this file")
    except ValueError as ve:
        print(ve)
    except TypeError as te:
        print(te)


if __name__ == "__main__":
    main()
