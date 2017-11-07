#!/usr/bin/python

import copy
import itertools
from random import choice


class CSP:
    def __init__(self, select_randomly=True):
        # used to determine whether to select randomly in
        # select-random-variable and order-domain-values
        self.select_randomly = select_randomly
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.calls = 0
        self.failure = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if j not in self.constraints[i]:
            # First, get a list of all possible pairs
            # of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(
                self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(
            lambda value_pair: filter_function(*value_pair),
            self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        # input: {}, [(x,y),...]
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        self.calls += 1
        # check whether assignments have 1 variable each => complete
        complete = True
        for key in assignment.keys():
            if len(assignment[key]) != 1:
                complete = False
                # break, or the program will look through the entire domain
                # in every call
                break
        if complete:
            return assignment

        unassigned = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(assignment, unassigned):
            domain_copy = copy.deepcopy(assignment)
            domain_copy[unassigned] = [value]
            #  queue = self.get_all_neighboring_arcs(unassigned)
            queue = self.get_all_arcs()
            if self.inference(domain_copy, queue):
                result = self.backtrack(domain_copy)
                if result:
                    return result
        self.failure += 1
        return False

    def order_domain_values(self, assignment, unassigned):
        """
        here we experimented with several attempts,
        some of which tried ideas from LCV (least constraining value)
        but these all resulted in more iterations
        therefore, this simply returns the the according list
        """
        return assignment[unassigned]

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.

        Selecting a random variable with a valid # of constraints (>1)
        within the domain, might give better runtimes, but
        it is also less predictable.

        Both are based on the idea of minimum remaining value (MRV),
        however, as we can guarantee there to be a set with 2 remaining values,
        2 will always be present and will always be the minimum.
        """
        if self.select_randomly:
            return choice(filter(lambda var:
                                 len(assignment[var]) == 2,
                                 assignment.keys()))
        else:
            for var in assignment.keys():
                if len(assignment[var]) == 2:
                    return var

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        #  print('AC3')
        while queue:  # true as long as there are any constraints
            i, j = queue.pop(0)  # remove and return the first tuple
            if self.revise(assignment, i, j):
                if not assignment[i]:  # if there are no items in the domain
                    return False
                neighbors = self.get_all_neighboring_arcs(i)
                for n in neighbors:
                    # equivalent of removing j from the set of i's neighbors
                    if j not in n[0]:
                        queue.append((n[0], i))
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        constraints = self.constraints[i][j]
        revised = False
        # 
        for x in assignment[i]:
            constraint_satisfied = False
            for y in assignment[j]:
                if (x, y) in constraints:
                    constraint_satisfied = True
                    break
            if not constraint_satisfied:
                assignment[i].remove(x)
                revised = True
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
             'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename, select_randomly=True):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP(select_randomly)
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(
            ['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(
            ['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'


def solve_board(board, random_choices):
    csp = create_sudoku_csp('sudokus/' + board + '.txt', random_choices)
    assignment = csp.backtracking_search()
    print '~ Random? ', random_choices, '=> failure: ',
    print csp.failure, 'total: ', csp.calls
    if not random_choices:
        print_sudoku_solution(assignment)


for board in ['easy', 'medium', 'hard', 'veryhard', 'extreme']:
    print 'Solving board: ' + board
    solve_board(board, random_choices=False)
    #  solve_board(board, random_choices=True)
