assignments = []

column_numbers = '123456789'
row_letters = 'ABCDEFGHI'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ a + b for a in A for b in B]

# utility data structures used to encode the sudoku board
boxes = cross(row_letters, column_numbers)
rows = [cross(row, column_numbers) for row in row_letters]
columns = [cross(row_letters, col) for col in column_numbers]
squares = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# diagonal units, used to solve for diagonal sudokus
diagonals = [boxes[::10], boxes[8:-1:8]]
unitlist = rows + columns + squares + diagonals
units = dict((box, [unit for unit in unitlist if box in unit]) for box in boxes)
# a dict from a box to other boxes in units that its in
peers = dict((box, set(sum(units[box],[]))-set([box])) for box in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    def generate_naked_twin_list_values(possible_naked_twins):
        """Helper method to generate list of naked twin values in a unit
        Args:
            possible_naked_twins(list): a list containing sudoku boxes ['A1', 'A2', 'A7']

        Returns:
            A list of the naked twin boxes for the unit
        """
        naked_twin_list_values = []
        # the dict defined below used to determine if a value has been seen already e.g. {'23' : 'A1'}
        # if a value occurs twice, only then will it be added to the naked_twin_list_values list
        possible_box_values_to_box_id_dict = {}
        for box in possible_naked_twins:
            box_value = values[box]
            if box_value in possible_box_values_to_box_id_dict:
                # since a value has already appeared before for this unit, then it must be a naked twin
                naked_twin_list_values.append(box_value)
            else:
                possible_box_values_to_box_id_dict[box_value] = box
        return naked_twin_list_values

    for unit in unitlist:
        # generate a list of boxes which may be naked twins e.g. ['A1', 'A2', 'A7']
        possible_naked_twins = [box for box in unit if len(values[box]) == 2]
        # list of actual naked twin values for a unit e.g. ['A1', 'A7']
        naked_twin_list_values = generate_naked_twin_list_values(possible_naked_twins)

        # iterate through all the boxes in the unit and eliminate the naked twin values
        # for all boxes, except for the boxes with only naked twins and boxes for which
        # we already have a solution (i.e. whose length is 1)
        for box in unit:
            if values[box] not in naked_twin_list_values and len(values[box]) != 1:
                # e.g. naked_twin = '23'
                for naked_twin in naked_twin_list_values:
                    # we need to iterate through each digit, as the naked twin digits may be separated e.g. digit = '2'
                    for digit in naked_twin:
                        assign_value(values, box, values[box].replace(digit, ''))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    values = []
    for el in grid:
        if el == '.':
            values.append(column_numbers)
        else:
            values.append(el)

    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in row_letters:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in column_numbers))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
