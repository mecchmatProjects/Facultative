import networkx as nx
import matplotlib.pyplot as plt


def sat_to_clique(clauses):
    G = nx.Graph()  # створюємо пустий граф

    # Додаємо вузли для кожної змінної та клаузи
    for i, clause in enumerate(clauses):
        for variable in clause:
            G.add_node((variable, i))  # вузол у вигляді (variable, clause_index)

    # Додаємо ребра згідно з правилами
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i >= j:  # щоб уникнути повторень
                continue
            # З'єднуємо тільки змінні з різних клауз
            for var1 in clause1:
                for var2 in clause2:
                    # Перевіряємо, чи змінна і її доповнення не зустрічаються разом
                    if var1 != var2 and var1 != f"-{var2}" and f"-{var1}" != var2:
                        G.add_edge((var1, i), (var2, j))

    # Пошук кліки розміру, рівного кількості клауз
    k = len(clauses)
    clique = None
    for c in nx.algorithms.clique.find_cliques(G):
        if len(c) == k:
            clique = c  # знайдена кліка розміру k
            break

    return G, clique


def visualize_graph(G, clique):
    pos = nx.spring_layout(G)  # обчислюємо позиції вузлів для візуалізації
    plt.figure(figsize=(10, 8))

    # Візуалізуємо всі вузли і ребра
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=500)
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Якщо знайдена кліка, підсвітимо її
    if clique:
        nx.draw_networkx_nodes(G, pos, nodelist=clique, node_color="orange", node_size=700)
        subgraph_edges = [(u, v) for u in clique for v in clique if G.has_edge(u, v)]
        nx.draw_networkx_edges(G, pos, edgelist=subgraph_edges, edge_color="red", width=2)

    plt.title("Visualization of Graph with Clique Highlighted")
    plt.show()


# Формула 3-SAT у вигляді списку клауз, де кожна клауза є списком змінних
clauses = [
    ["x1", "x2", "x3"],
    ["x1'", "x2", "x3'"],
    ["x1", "x3"]
]

G, clique = sat_to_clique(clauses)
if clique:
    print("Знайдена кліка:", clique)
else:
    print("Кліки розміру", len(clauses), "не знайдено.")

# Візуалізація графа
visualize_graph(G, clique)
