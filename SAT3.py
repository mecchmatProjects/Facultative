from itertools import product # Cartesian product


def parse_clause(clause):
    """Parse a clause into variable indices."""
    return [int(var[1:]) for var in clause]  # Skip 'x' and convert to int


def evaluate_clause(clause, assignment):
    """Evaluate a clause based on the given assignment."""
    return any((assignment[var] if var > 0 else not assignment[-var]) for var in clause)


def evaluate_formula(formula, assignment):
    """Evaluate the entire formula."""
    return all(evaluate_clause(clause, assignment) for clause in formula)


def sat_3_solver(formula):
    """Solve the 3-SAT problem."""
    # Determine the number of variables
    num_vars = max(abs(var) for clause in formula for var in clause)

    # Generate all possible assignments of variables
    for assignment_tuple in product([False, True], repeat=num_vars):
        assignment = {i + 1: val for i, val in enumerate(assignment_tuple)}
        if evaluate_formula(formula, assignment):
            return assignment  # Return the first satisfying assignment

    return None  # No satisfying assignment found


# Example: SAT-3 instance
# Representing the formula (x1 v x2 v x3) ^ (x1' v x2' v x3) ^ (x1 v x3)
# This corresponds to (x1 v x2 v x3) ^ (not x1 v not x2 v x3) ^ (x1 v x3)
formula = [
    [1, 2, 3],  # (x1 v x2 v x3)
    [-1, -2, 3],  # (not x1 v not x2 v x3)
    [1, 3]  # (x1 v x3)
]

solution = sat_3_solver(formula)

if solution:
    print("Satisfying assignment found:", solution)
else:
    print("No satisfying assignment exists.")