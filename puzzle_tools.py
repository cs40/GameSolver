"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
from word_ladder_puzzle import WordLadderPuzzle
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)

def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    >>> word_set = {"b"}
    >>> w = WordLadderPuzzle("a", "c", word_set)
    >>> sol = depth_first_solve(w)
    >>> sol is None
    True
    >>> word_set = {"c"}
    >>> w = WordLadderPuzzle("b", "c", word_set)
    >>> sol = depth_first_solve(w)
    >>> print(sol)
    b --> c
    <BLANKLINE>
    c --> c
    <BLANKLINE>
    <BLANKLINE>
    """
    seen = set()
    dfs_node = _helper_dfs(puzzle, seen)
    return dfs_node


def _helper_dfs(puzzle, seen):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @type seen: set
    @rtype: PuzzleNode | None
    """
    if puzzle.is_solved():
        return PuzzleNode(puzzle)
    elif puzzle.fail_fast():
        return None
    else:
        list_extensions = puzzle.extensions()
        for x in list_extensions:
            if str(x) not in seen:
                seen.add(str(x))  # adds to seen
                node = _helper_dfs(x, seen)
                if node is not None:
                    return PuzzleNode(puzzle, [node])
            # if in seen, then skip to next puzzle config
        return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> word_set = {"b"}
    >>> w = WordLadderPuzzle("a", "c", word_set)
    >>> sol = depth_first_solve(w)
    >>> sol is None
    True
    >>> word_set = {"c"}
    >>> w = WordLadderPuzzle("b", "c", word_set)
    >>> sol = depth_first_solve(w)
    >>> print(sol)
    b --> c
    <BLANKLINE>
    c --> c
    <BLANKLINE>
    <BLANKLINE>
    """
    bfs = _helper_bfs(puzzle)
    if bfs is not None:
        first_node = _helper_bfs_rebuild(bfs)
        return first_node
    else:
        return None


def _helper_bfs_rebuild(puzzlenode):
    """
    Return a reverse PuzzleNode from solution to the original configuration.

    @type puzzlenode: PuzzleNode
    @rtype: PuzzleNone
    """
    node = puzzlenode
    node.children = []
    while node.parent is not None:
        tmp = node.parent
        tmp.children = [node]
        node = node.parent
    return node


def _helper_bfs(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    """
    queue = deque()
    seen = set([])

    first_node = PuzzleNode(puzzle)
    first_node.children = _helper_dfs_extension(puzzle.extensions(),
                                                first_node)
    queue.append(first_node)  # append first node to queue
    seen.add(str(first_node))  # append first node to seen set

    while queue:
        removed = queue.popleft()  # removed is a PuzzleNode
        # with child, and its child has it as a parent

        if not removed.puzzle.is_solved():
            if not removed.puzzle.fail_fast():

                for PN in removed.children:  # each child is a PuzzleNode
                    if str(PN.puzzle) not in seen:
                        seen.add(str(PN.puzzle))
                        PN.children = _helper_dfs_extension(
                            PN.puzzle.extensions(), PN)
                        # set child's child to a PuzzleNode
                        queue.append(PN)

        elif removed.puzzle.is_solved():  # if the PuzzleNode is a solution
            return removed

    return None


def _helper_dfs_extension(list_, parent=None):
    """
    Return a list of Puzzlenode, with parents and empty children.

    @type list_: list
    @type parent: PuzzleNode | None
    @rtype: list[PuzzleNode]
    """
    list_new = []
    for puzzle in list_:
        list_new.append(PuzzleNode(puzzle, [], parent))
    return list_new

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
