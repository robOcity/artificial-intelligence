# TODO: Incorporate the `depth` parameter into each function
# TODO: Update all recursive calls to pass the depth parameter
# TODO: Add a new conditional to cut off search when the depth
#       limit is reached
# NOTE: The minimax_decision function has been done for you!


def minimax_decision(gameState, depth):
    """Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.

    You can ignore the special case of calling this function
    from a terminal state.
    """
    best_score = float("-inf")
    best_move = None
    for a in gameState.actions():
        # DONE: call has been updated with a depth limit
        v = min_value(gameState.result(a), depth - 1)
        if v > best_score:
            best_score = v
            best_move = a
    return best_move


# TODO: add a depth parameter to the function signature
def min_value(gameState):
    """Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if gameState.terminal_test():
        return gameState.utility(0)

    # TODO: add a new conditional test to cut off search
    #       when the depth parameter reaches 0 -- for now
    #       just return a value of 0 at the depth limit

    v = float("inf")
    for a in gameState.actions():
        # TODO: pass a decremented depth parameter to each recursive call
        v = min(v, max_value(gameState.result(a)))
    return v


# TODO: add a depth parameter to the function signature
def max_value(gameState):
    """Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if gameState.terminal_test():
        return gameState.utility(0)

    # TODO: add a new conditional test to cut off search
    #       when the depth parameter reaches 0 -- for now
    #       just return a value of 0 at the depth limit

    v = float("-inf")
    for a in gameState.actions():
        # TODO: pass a decremented depth parameter to each recursive call
        v = max(v, min_value(gameState.result(a)))
    return v
