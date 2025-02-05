

"""
Function knapsack_brute_force takes in three arguments:
Params:
    weights: a list of weights for each item.
    values: a list of values for each item.
    capacity: the maximum capacity of the knapsack.
Returns:
    max_capcity
    best combination
"""
def knapsack_brute_force(weights, values, capacity):
    n = len(weights)
    max_value = 0
    best_combination = []

    # There are 2^n possible combinations, as each item can either be included or not
    # For each possible subset of items (from 0 to 2^n - 1), we calculate the total weight and value.
    for i in range(2 ** n):
        total_weight = 0
        total_value = 0
        combination = []

        # Check each bit in the binary representation of `i`
        for j in range(n):
            if (i >> j) & 1:  # If the j-th bit is set, include item j in the knapsack
                total_weight += weights[j]
                total_value += values[j]
                combination.append(j)

        # Check if this combination is valid and if it gives a better value
        if total_weight <= capacity and total_value > max_value:
            max_value = total_value
            best_combination = combination

    return max_value, best_combination

"""
Branch and Bound Approach
The branch-and-bound method divides the problem into smaller subproblems and uses bounds to "prune" parts 
of the solution space that cannot possibly contain the optimal solution.
Bounding: At each decision point (include or exclude an item), 
we compute an upper bound on the maximum value achievable from that point onward. 
If the upper bound is less than the current best solution, we skip exploring that branch.

Recursive DFS: We explore every item with two choices — include or exclude the item 
— and recursively explore each choice.
"""

"""
The bound() function calculates an optimistic upper bound on the total value achievable from the current item onward, 
assuming we can take fractional parts of items. 
This is like a fractional knapsack heuristic to estimate the maximum potential value of the branch.
"""
def knapsack_branch_and_bound(weights, values, capacity):
    # Number of items
    n = len(weights)

    # Initialize max value and best items selection
    max_value = 0
    best_items = []

    # Helper function to calculate the upper bound for the remaining items
    def boundFraction(i, current_weight, current_value):
        if current_weight >= capacity:
            return 0  # If weight exceeds capacity, bound is zero

        # Initial bound is the current value
        bound_value = current_value
        total_weight = current_weight

        # Add items as much as possible to maximize the bound (fractional knapsack)
        for j in range(i, n):
            if total_weight + weights[j] <= capacity:
                total_weight += weights[j]
                bound_value += values[j]
            else:
                # Add fractional part of the next item
                bound_value += values[j] * (capacity - total_weight) / weights[j]
                break

        return bound_value

    def bound(i, current_weight, current_value):
        if current_weight >= capacity:
            return 0  # If weight exceeds capacity, bound is zero

        # Initial bound is the current value
        bound_value = current_value
        total_weight = current_weight

        # Add whole items until the capacity is reached
        for j in range(i, n):
            if total_weight + weights[j] <= capacity:
                total_weight += weights[j]
                bound_value += values[j]
            else:
                break  # Stop if we can't add the whole item

        return bound_value

    # Recursive DFS function with branch and bound
    """
    The dfs() function explores each item index i with two choices: include or exclude the item.
    Before making these recursive calls, it calculates an upper bound. If the bound is less than or equal 
    to the current max_value, it prunes the branch, as it cannot improve the best solution found so far.
    If including the item doesn’t exceed the capacity, we add the item to the knapsack and continue the DFS.
    """
    def dfs(i, current_weight, current_value, current_items):
        nonlocal max_value, best_items

        # Base case: all items have been considered
        if i == n:
            if current_value > max_value:
                max_value = current_value
                best_items = current_items[:]
            return

        # Pruning: Calculate upper bound for the remaining items
        upper_bound = bound(i, current_weight, current_value)
        if upper_bound <= max_value:
            return  # Prune this branch if bound is less than max_value

        # Decision 1: Exclude the current item and move to the next
        dfs(i + 1, current_weight, current_value, current_items)

        # Decision 2: Include the current item (if it doesn't exceed capacity)
        if current_weight + weights[i] <= capacity:
            current_items.append(i)  # Include item i
            dfs(i + 1, current_weight + weights[i], current_value + values[i], current_items)
            current_items.pop()  # Backtrack to explore other possibilities

    # Start DFS from the first item
    dfs(0, 0, 0, [])
    return max_value, best_items

"""
The greedy strategy is to:

Calculate the value-to-weight ratio for each item.
Sort the items in decreasing order of this ratio.
Add as much of each item as possible to the knapsack until the knapsack is full.
"""


def knapsack_greedy(weights, values, capacity):
    # Calculate value-to-weight ratio for each item
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(len(values))]

    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x[0], reverse=True)

    total_value = 0  # Total value accumulated in the knapsack
    selected_items = []  # Track items added to the knapsack

    for ratio, weight, value, index in items:
        if capacity >= weight:
            # Take the whole item
            capacity -= weight
            total_value += value
            selected_items.append((index, 1))  # 1 indicates the item was taken fully
        else:
            # Take the fraction of the item that fits
            fraction = capacity / weight
            total_value += value * fraction
            selected_items.append((index, fraction))  # Fraction indicates partial item taken
            break  # Knapsack is full after taking the fraction

    # Return the total value and the list of selected items with their fractions
    return total_value, selected_items

"""
    Solve the Knapsack problem using dynamic programming.

    :param weights: List of weights of the items.
    :param values: List of values of the items.
    :param capacity: Maximum capacity of the knapsack.
    :return: Maximum value that can be obtained within the given capacity.
"""
def knapsack_dynamics(weights, values, capacity):

    n = len(values)  # Number of items
    # Create a DP table to store maximum values at each capacity
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                # If the item can be included, decide to take it or not
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                # If the item cannot be included, take the value from the previous item
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]  # The maximum value for the full capacity


if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    max_value, best_combination = knapsack_brute_force(weights, values, capacity)
    print("Maximum value:", max_value)
    print("Items included:", best_combination)


    max_value, best_combination = knapsack_branch_and_bound(weights, values, capacity)
    print("Maximum value:", max_value)
    print("Items included:", best_combination)

    max_value, best_combination = knapsack_greedy(weights, values, capacity)
    print("Maximum value:", max_value)
    print("Items included:", best_combination)