"""
    To find a unique set of all stars, we use the simplex algorithm
    (see: https://en.wikipedia.org/wiki/Simplex_algorithm). It turns
    out trying to hand-wrap your own optimization algorithm just gets
    ugly and doesn't work all the time. It would have been cool to
    learn about algorithms like this back in school, but I was a math
    major who was only interested in graduating.

    Stay in school, kids, and for the right reasons. And take the right
    classes.
"""


from collections import defaultdict, namedtuple, OrderedDict
from fractions import Fraction
from itertools import product
from sortedcontainers import SortedDict



class SimplexTableauBuilder:

    ZERO = Fraction.from_float(0)
    ONE = Fraction.from_float(1)

    def __init__(self, coeffs):
        self._coeffs = self._to_fraction(coeffs)
        self._num_variables = len(coeffs)
        self._num_slack_variables = 0
        self._constraints = []
        self._values = []

    @staticmethod
    def _to_fraction(float_list):
        return list(map(lambda coeff: Fraction.from_float(coeff), float_list))

    def add_constraint(self, constraint, value):
        assert len(constraint) == self._num_variables, (
                f"Constraint {constraint} did not have"
                f" {self._num_slack_variables} variables."
        )

        [constraint.append(self.ZERO) for constraint in self._constraints]
        self._constraints.append([
                *self._to_fraction(constraint),
                *[self.ZERO] * self._num_slack_variables,
                self.ONE,
        ])

        self._values.append(value)
        self._num_slack_variables += 1

    def build(self):
        tableau = [
                [*constraint, self._values[index]]
                for index, constraint in enumerate(self._constraints)
        ]
        tableau.append([
                *self._coeffs,
                *[self.ZERO] * (self._num_slack_variables + 1),
        ])
        return SimplexTableauSolver(tableau)


Pivot = namedtuple("Pivot", ["row", "column"])


class SimplexTableauSolver:

    def __init__(self, tableau):
        self.tableau = tableau

    def solve(self):
        while self._can_improve():
            self._pivot(*self._find_pivot())

    def _can_improve(self):
        return any(x < 0 for x in self.tableau[-1][:-1])

    def _find_pivot(self):
        non_zero_values = filter(lambda x: x != 0, self.tableau[-1][:-1])
        pivot_column = self.tableau[-1].index(min(non_zero_values))

        print(f"Pivot column {pivot_column}")

        def coefficient_ratio(row):
            if row[pivot_column] == 0:
                return None
            value = row[-1] / row[pivot_column]
            return value if value > 0 else None
    
        quotients = [
                (index, row[-1] / row[pivot_column])
                for index, row in enumerate(self.tableau[:-1])
                if row[pivot_column] != 0 and row[-1] / row[pivot_column] > 0
        ]

        min_value = min(quotients, key=lambda entry: entry[1])
        min_values = [
                index 
                for index, value in enumerate(quotients)
                if value == min_value[1]
        ]
        if len(min_values) > 1:
            raise Exception("Linear program is degenerate")

        return min_values[0], pivot_column

    def _pivot(self, pivot_row, pivot_column):
        pivot_cell = self.tableau[pivot_row][pivot_column]

        self.tableau[pivot_row] = [
                value / pivot_cell
                for value in self.tableau[pivot_row]
        ]

        for row_index, row in enumerate(self.tableau):
            if row_index != pivot_row:
                pivot_column_value = self.tableau[row_index][pivot_column]
                multi_pivot_row = [
                        value * pivot_column_value
                        for value in self.tableau[row_index]
                ]
                self.tableau[row_index] = [
                        existing - new
                        for existing, new
                        in zip(self.tableau[row_index], multi_pivot_row)
                ]

