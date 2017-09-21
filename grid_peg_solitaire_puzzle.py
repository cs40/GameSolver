from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """
    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set


    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> grid += [["*", "*", ".", "*", "*"]]
        >>> grid += [["*", "*", "*", "*", "*"]]
        >>> g = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(g)
        *****
        *****
        *****
        **.**
        *****
        _____
        """
        markers = self._marker[:]
        string_ = ''
        for i in markers:
            for j in i:
                string_ += j
            string_ += '\n'

        return string_[:-1] + "\n" + '_____'

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equal to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid = [["*", "*", ".", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> grid_2 = [["#", "*", ".", "."]]
        >>> gpsp_2 = GridPegSolitairePuzzle(grid_2, {"*", ".", "#"})
        >>> gpsp_2 == gpsp
        False
        >>> gpsp_2 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp_2 == gpsp
        True
        """
        return ((type(self) == type(other)) and
                (self._marker == other._marker) and
                (self._marker_set == other._marker_set))

    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", ".", "*"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp.extensions()[0])
        ..**
        _____
        >>> grid = [["*", "*", ".", "*", "#"]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp.extensions()[0])
        ..**#
        _____
        """
        grid_ = [x[:] for x in self._marker]  # copy
        list_extensions = []

        for i in range(len(grid_)):
            for j in range(len(self._marker[i])):
                if grid_[i][j] == ".":  # if that index is empty
                    # check to the right
                    if (j + 2 in range(len(grid_[0]))) and\
                            (grid_[i][j + 1] == "*") and\
                            (grid_[i][j + 2] == "*"):

                        grid_copy = [x[:] for x in self._marker]
                        grid_copy[i][j] = "*"
                        grid_copy[i][j + 1] = "."
                        grid_copy[i][j + 2] = "."
                        list_extensions.append(
                            GridPegSolitairePuzzle(
                                grid_copy, self._marker_set))

                    # check to the left
                    if (j - 2 in range(len(grid_[0]))) and\
                            (grid_[i][j - 1] == "*") and\
                            (grid_[i][j - 2] == "*"):
                        grid_copy = [x[:] for x in self._marker]
                        grid_copy[i][j] = "*"
                        grid_copy[i][j - 1] = "."
                        grid_copy[i][j - 2] = "."
                        list_extensions.append(
                            GridPegSolitairePuzzle(
                                grid_copy, self._marker_set))

                    # check above
                    if (i + 2 in range(len(grid_))) and\
                            (grid_[i + 1][j] == "*") and\
                            (grid_[i + 2][j] == "*"):
                        grid_copy = [x[:] for x in self._marker]
                        grid_copy[i][j] = "*"
                        grid_copy[i + 1][j] = "."
                        grid_copy[i + 2][j] = "."
                        list_extensions.append(
                            GridPegSolitairePuzzle(
                                grid_copy, self._marker_set))

                    # check below
                    if (i - 2 in range(len(grid_))) and\
                            (grid_[i - 1][j] == "*") and\
                            (grid_[i - 2][j] == "*"):
                        grid_copy = [x[:] for x in self._marker]
                        grid_copy[i][j] = "*"
                        grid_copy[i - 1][j] = "."
                        grid_copy[i - 2][j] = "."
                        list_extensions.append(
                            GridPegSolitairePuzzle(
                                grid_copy, self._marker_set))

        return list_extensions


    # override is_solved()
    # A configuration is solved when there is exactly one "*" left

    def is_solved(self):
        """
        Return whether self is solved.

        @return: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [["*", ".", ".", "."]]
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> gpsp.is_solved()
        True
        >>> grid2 = [[".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.is_solved()
        False
        """
        count = 0
        for item in self._marker:
            for symbol in item:
                if symbol == "*":
                    count += 1

        return count == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    # grid = [["*", "*", ".", "*"]] # 0.0001888275146484375 seconds bfs solved

    # grid = [["#", "*", ".", "*", "*"]] # 0.00020813941955566406 seconds
    # bfs solved

    grid = [["#"], # 0.00023102760314941406 seconds bfs solved
            ["*"],
            ["*"],
            ["."],
            ["*"]]

    # grid = [["*", "*", "*"], # 0.017332077026367188 seconds bfs solved
    #         ["*", "*", "*"],
    #         ["*", "*", "*"],
    #         [".", "*", "*"]]

    # grid = [["*", "*", ".", "*", "*"], # 602.9188828468323 seconds bfs solved
    #         ["*", "*", "*", "*", "*"], # 4.51656699180603 seconds dfs solved
    #         ["*", "*", "*", "*", "*"],
    #         ["*", "*", ".", "*", "*"],
    #         ["*", "*", "*", "*", "*"]]

    # grid = [["*", "*", "*", "*", "*"],
    #         ["*", "*", "*", "*", "*"],
    #         ["*", "*", "*", "*", "*"],
    #         ["*", "*", ".", "*", "*"],
    #         ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    # solution = breadth_first_solve(gpsp)
    solution = depth_first_solve(gpsp)
    while solution.children:
        solution = solution.children[0]
    end = time.time()

    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    # print("Using depth-first: \n{}".format(solution))
    print(solution)
