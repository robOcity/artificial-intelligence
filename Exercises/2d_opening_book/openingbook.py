import random

from gamestate import GameState

NUM_ROUNDS = 10


def build_table(num_rounds=NUM_ROUNDS):
    # You should run no more than `num_rounds` simulations -- the
    # goal of this quiz is to understand one possible way to develop
    # an opening book; not to develop a good one

    # NOTE: the GameState object is not hashable, and the python3
    #       runtime includes security features that make object
    #       hashes non-portable. There is a new attribute on
    #       GameState objects in this quiz called `hashable` that
    #       can be used as a dictionary key

    # TODO: return a table {k:v} where each k is a game state
    #       and each v is the best action to take in that state
    return {}