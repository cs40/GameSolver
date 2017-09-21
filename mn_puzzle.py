from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> m = MNPuzzle(start_grid, target_grid)
        >>> t = MNPuzzle(start_grid, target_grid)
        >>> start = (("1", "2", "3"), ("4", "5", "*"))
        >>> target = (("1", "2", "3"), ("4", "5", "*"))
        >>> n = MNPuzzle(start, target)
        >>> n == m
        False
        >>> m == t
        True
        """
        return (type(other) == type(self) and self.n == other.n and
                self.m == other.m and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> m = MNPuzzle(start_grid, target_grid)
        >>> print(m)
        *23
        145
        _____
        """
        markers = self.from_grid
        string = ''
        for i in markers:
            for j in i:
                string += j
            string += '\n'

        return string[:-1] + '\n' + '_____'

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> target_grid = (("1", "2"), ("3", "*"))
        >>> start_grid = (("1", "2"), ("3", "*"))
        >>> s = MNPuzzle(start_grid, target_grid)
        >>> print(s.extensions()[0])
        12
        *3
        _____
        >>> print(s.extensions()[1])
        1*
        32
        _____
        """
        grid = _extensions_helper_tuple_list(self.from_grid)
        list_extensions = []

        for i in range(self.n):
            for j in range(self.m):
                if grid[i][j] == "*":
                    # check to the right
                    if (j + 1 in range(self.m)) and grid[i][j + 1].isalnum:
                        grid_copy = [x[:] for x in grid]
                        grid_copy[i][j], grid_copy[i][j + 1] = \
                            grid_copy[i][j + 1], "*"
                        list_extensions.append(
                            MNPuzzle(_extensions_helper_tuple_list(grid_copy),
                                     self.to_grid))

                    # check to the left
                    if (j - 1 in range(self.m)) and grid[i][j - 1].isalnum:
                        grid_copy = [x[:] for x in grid]
                        grid_copy[i][j], grid_copy[i][j - 1] = \
                            grid_copy[i][j - 1], "*"
                        list_extensions.append(
                            MNPuzzle(_extensions_helper_tuple_list(grid_copy),
                                     self.to_grid))

                    # check to above
                    if (i + 1 in range(self.n)) and grid[i + 1][j].isalnum:
                        grid_copy = [x[:] for x in grid]
                        grid_copy[i][j], grid_copy[i + 1][j] = \
                            grid_copy[i + 1][j], "*"
                        list_extensions.append(
                            MNPuzzle(_extensions_helper_tuple_list(grid_copy),
                                     self.to_grid))

                    # check below
                    if (i - 1 in range(self.n)) and grid[i - 1][j].isalnum:
                        grid_copy = [x[:] for x in grid]
                        grid_copy[i][j], grid_copy[i - 1][j] = \
                            grid_copy[i - 1][j], "*"
                        list_extensions.append(
                            MNPuzzle(_extensions_helper_tuple_list(grid_copy),
                                     self.to_grid))

        return list_extensions

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return whether self is solved.
        @type self: MNPuzzle
        @rtype: bool

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> m = MNPuzzle(start_grid, target_grid)
        >>> m.is_solved()
        False
        >>> start_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> m2 = MNPuzzle(start_grid2, target_grid2)
        >>> m2.is_solved()
        True
        """
        return self.from_grid == self.to_grid


def _extensions_helper_tuple_list(list_tuple):
    """
    Converts list_tuple and its elements to a list or tuple
    depending on the type of list_tuple.

    @type list_tuple: tuple[tuple[str]] | list[list[str]]
    @rtype: tuple[tuple[str]] | list[list[str]]

    >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
    >>> list_ = [['*', '2', '3'], ['1', '4', '5']]
    >>> _extensions_helper_tuple_list(start_grid)
    [['*', '2', '3'], ['1', '4', '5']]
    >>> _extensions_helper_tuple_list(list_)
    (('*', '2', '3'), ('1', '4', '5'))
    """
    extensions_tuple = []

    if isinstance(list_tuple, tuple):
        for row in list_tuple:
            extensions_tuple.append(list(row))
        return extensions_tuple

    else:
        for row in list_tuple:
            extensions_tuple.append(tuple(row))
        return tuple(extensions_tuple)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
