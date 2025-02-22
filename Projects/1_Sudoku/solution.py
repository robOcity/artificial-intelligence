from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs)
    for rs in ("ABC", "DEF", "GHI")
    for cs in ("123", "456", "789")
]
diag_1 = [[row + col for row, col in zip(rows, cols)]]
diag_2 = [[row + col for row, col in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_1 + diag_2


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md

    """
    reduced = values.copy()
    for box1 in values:
        for box2 in peers[box1]:
            if len(values[box1]) == 2 and set(values[box1]) == set(values[box2]):
                for peer in set(peers[box1]).intersection(set(peers[box2])):
                    for digit in values[box1]:
                        reduced[peer] = reduced[peer].replace(digit, '')

    return reduced


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """

    # loop over singletons
    singletons = [
        (box, value) for box, value in values.items() if len(value) == 1
    ]
    for one_box, one_value in singletons:

        # create the set of boxes for domain reduction
        box_set = set.union(*[set(peers) for peers in units[one_box]])
        box_set.discard(one_box)
        if any([len(box) == 1 for box in box_set]):
            print(box_set)

        # reduce the domain expressed as a string
        for box in box_set:
            values[box] = values[box].replace(one_value, "")

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for domain_value in "123456789":
            peers_w_domain_value = [
                peer for peer in unit if domain_value in values[peer]
            ]
            if len(peers_w_domain_value) == 1:
                values[peers_w_domain_value[0]] = domain_value
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1]
        )
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1]
        )
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        return False

    # Check if solved
    if all([len(v) == 1 for v in values.values()]):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    fewest = [
        k
        for k in sorted(values, key=lambda k: len(values[k]))
        if len(values[k]) > 1
    ]
    if not fewest:
        return False
    fewest = fewest[0]
    # Now use recursion to solve each one of the resulting sudokus
    # If one returns a value (not False), return that answer!
    for value in values[fewest]:
        values_copy = values.copy()
        values_copy[fewest] = value
        result = search(values_copy)
        if result:
            return result


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = "2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3"
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print(
            "We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement."
        )
