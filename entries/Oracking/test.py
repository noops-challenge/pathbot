from random import choice
from pathbot import ConsoleWorld

def random_solver(map):
    return choice(["W", "A", "S", "D"])

game = ConsoleWorld(input_interface=random_solver)
game.start()
