"""
Bron-Kerbosch Algorithm for Maximal Cliques Detection
The Bron-Kerbosch algorithm is chosen for its efficiency and effectiveness in finding all maximal cliques in an undirected graph. This algorithm employs a recursive depth-first search mechanism, which avoids the redundancy and inefficiency inherent in other brute-force methods.
chttps://www.geeksforgeeks.org/maximal-clique-problem-recursive-solution/


Follow the steps to solve the problem:

Converts a list of edges to an adjacency list representation of the graph to facilitate quick access to neighbors.
Initializes three sets: R (current clique), P (potential nodes that can be added to the clique), and X (nodes already processed and not included in the clique).
Utilizes a recursive approach where for each node in P, the node is added to R, and the algorithm recursively explores further potential cliques.
The recursion continues, refining P and X based on adjacency relations, until P and X are empty, indicating a maximal clique has been found.
Outputs the maximal clique size after computing all possible clique
"""

def bron_kerbosch(R, P, X, graph):
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph
        )
        X.add(v)


def main():
    edges = [(1, 2), (2, 3), (3, 1), (4, 3), (4, 1), (4, 2)]
    n = 4  # Number of nodes

    # Create an adjacency list from the edges
    graph = {i: set() for i in range(1, n + 1)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # Convert set keys into sorted lists for consistent ordering
    graph = {key: set(graph[key]) for key in graph}

    all_cliques = list(bron_kerbosch(set(), set(graph.keys()), set(), graph))
    if all_cliques:
        max_clique_size = max(len(clique) for clique in all_cliques)
    else:
        max_clique_size = -1
    print(max_clique_size)


if __name__ == "__main__":
    main()