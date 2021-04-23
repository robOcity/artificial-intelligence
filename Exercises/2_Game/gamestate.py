from copy import deepcopy

xlim, ylim = 3, 2  # board dimensions

# The eight movement directions possible for a chess queen
RAYS = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]


class GameState:
    """
    Attributes
    ----------
    _board: list(list)
        Represent the board with a 2d array _board[x][y]
        where open spaces are 0 and closed spaces are 1

    _parity: bool
        Keep track of active player initiative (which
        player has control to move) where 0 indicates that
        player one has initiative and 1 indicates player 2

    _player_locations: list(tuple)
        Keep track of the current location of each player
        on the board where position is encoded by the
        board indices of their last move, e.g., [(0, 0), (1, 0)]
        means player 1 is at (0, 0) and player 2 is at (1, 0)
    """

    def __init__(self):
        self._board = [[0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self._parity = 0
        self._player_locations = [None, None]

    def actions(self):
        """Return a list of legal actions for the active player

        You are free to choose any convention to represent actions,
        but one option is to represent actions by the (row, column)
        of the endpoint for the token. For example, if your token is
        in (0, 0), and your opponent is in (1, 0) then the legal
        actions could be encoded as (0, 1) and (0, 2).
        """
        return self.liberties(self._player_locations[self._parity])

    def player(self):
        """Return the id of the active player

        Hint: return 0 for the first player, and 1 for the second player
        """
        return self._parity

    def result(self, action):
        """Return a new state that results from applying the given
        action in the current state

        Hint: Check out the deepcopy module--do NOT modify the
        objects internal state in place
        """
        assert action in self.actions(), "Attempting illegal action"
        new_game = deepcopy(self)
        self._board[action[0]][action[1]] = 1
        self._player_locations[self._parity] = action
        self._parity ^= 1  # xor to toggle between players
        return new_game

    def terminal_test(self):
        """return True if the current state is terminal,
        and False otherwise

        Hint: an Isolation state is terminal if _either_
        player has no remaining liberties (even if the
        player is not active in the current state)
        """
        return (
            any(
                [
                    len(self.liberties(self._player_locations[player])) == 0
                    for player in [0, 1]
                ]
            )
            == 0
        )

    def liberties(self, loc):
        """Return a list of all open cells in the
        neighborhood of the specified location.  The list
        should include all open spaces in a straight line
        along any row, column or diagonal from the current
        position. (Tokens CANNOT move through obstacles
        or blocked squares in queens Isolation.)

        Note: if loc is None, then return all empty cells
        on the board
        """
        if not loc:
            return self._get_blank_space()
        moves = []
        _x, _y = loc
        for ray in RAYS:
            dx, dy = ray
            while 0 < _x + dx <= xlim and 0 < _y + dy <= ylim:
                if self._board[_x + dx][_y + dy] == 0:
                    moves.append((dx, dy))
        return moves

    def _get_blank_space(self):
        return [
            (x, y)
            for x in range(xlim)
            for y in range(ylim)
            if self._board[x][y] == 0
        ]
