import random

from gamestate import GameState

NUM_ROUNDS = 10


def build_table(num_rounds=NUM_ROUNDS):
    """Build a basic opening book of moves."""

    import random

    initial_moves = [
        (2, 2),
        (1, 1),
        (0, 0),
        (0, 2),
        (2, 0),
        (1, 2),
        (2, 1),
        (3, 3),
        (3, 1),
        (1, 3),
    ]
    openingbook = {}
    for i, move in enumerate(initial_moves):
        game = GameState()
        liberties = game.liberties(game._player_locations[game.player()])
        if move not in liberties:
            move = random.choice(liberties)
        game = game.result(move)
        openingbook[game.hashable] = move
    return openingbook


def h_moves_diff(gamestate):
    """
    The differential in moves available to the current player.  Positive values
    are better than negative values for this evaluation heuristic.  
    """
    my_loc = gamestate._player_locations[gamestate.player()]
    op_loc = gamestate._player_locations[gamestate.player() ^ 1]
    return gamestate.liberties(my_loc) - gamestate.liberties(op_loc)
