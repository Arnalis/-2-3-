import matplotlib.pyplot as plt
import networkx as nx


def build_graph():
    """Строит граф функции is_valid_array."""
    graph = nx.DiGraph()

    labels = {
        1: "N1\nвход",
        2: "N2\nlen(set) != len?",
        3: 'N3\nreturn False,\n"различные"',
        4: "N4\nany(abs > 10^9)?",
        5: 'N5\nreturn False,\n"диапазон"',
        6: 'N6\nreturn True,\n""',
        7: "N7\nвыход",
    }
    for node, label in labels.items():
        graph.add_node(node, label=label)

    edges = [
        (1, 2, ""), (2, 3, "да"), (2, 4, "нет"),
        (3, 7, ""), (4, 5, "да"), (4, 6, "нет"),
        (5, 7, ""), (6, 7, ""),
    ]
    for source, target, edge_label in edges:
        graph.add_edge(source, target, label=edge_label)

    return graph, labels


def draw_single_path(graph, labels, path, color, filename, title):
    positions = {
        1: (0, 4), 2: (0, 3), 3: (-2, 2), 4: (0, 2),
        5: (-1.5, 1), 6: (1.5, 1), 7: (0, 0),
    }

    plt.figure(figsize=(10, 8))

    node_colors = []
    for node in graph.nodes():
        if node == 1:
            node_colors.append("#66dd66")
        elif node == 7:
            node_colors.append("#ff8888")
        else:
            node_colors.append("#aaccff")

    #  серые стрелки без подписей
    nx.draw_networkx_edges(graph, positions, edge_color="lightgray",
                           arrows=True, arrowsize=15, width=1.0, node_size=2500)

    #  ребра текущего пути
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(graph, positions, edgelist=path_edges,
                           edge_color=color, arrows=True, arrowsize=25,
                           width=3.5, node_size=2500,
                           connectionstyle="arc3,rad=0.1") 


    edge_labels = {}
    for u, v in path_edges:
        lbl = graph.edges[u, v].get("label", "")
        if lbl:
            edge_labels[(u, v)] = lbl

    if edge_labels:
        nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels,
                                     font_size=12, font_color=color,
                                     font_weight="bold", label_pos=0.4,
                                     bbox=dict(boxstyle="round,pad=0.2",
                                               fc="white", ec=color, alpha=0.9))

    #  Вершины и их подписи
    nx.draw_networkx_nodes(graph, positions, node_color=node_colors,
                           node_size=2500, edgecolors="black")
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=9)

    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()
    print(f"Сохранено: {filename}")


def main():
    graph, labels = build_graph()

    # Пути
    paths_info = [
        (
            [1, 2, 3, 7],
            "#dd2222",
            "path_test1_duplicates.png",
            "Путь 1: [1, 2, 3, 7] — массив с дубликатами"
        ),
        (
            [1, 2, 4, 5, 7],
            "#2255dd",
            "path_test2_out_of_range.png",
            "Путь 2: [1, 2, 4, 5, 7] — число вне диапазона 10^9"
        ),
        (
            [1, 2, 4, 6, 7],
            "#22aa44",
            "path_test3_valid.png",
            "Путь 3: [1, 2, 4, 6, 7] — валидный массив"
        ),
    ]

    print("=" * 60)
    print("  ВИЗУАЛИЗАЦИЯ ГРАФА is_valid_array (отдельные картинки)")
    print("=" * 60)
    print("Вершины: {1, 2, 3, 4, 5, 6, 7}")
    print("Рёбра:   {(1,2), (2,3), (2,4), (3,7), (4,5), (4,6), (5,7), (6,7)}")
    print("ЦС = 8 - 7 + 2 = 3")
    print()

    for path, color, filename, title in paths_info:
        print(f"Генерация: {title}")
        draw_single_path(graph, labels, path, color, filename, title)
        print()

    print("Все картинки сгенерированы.")


if __name__ == "__main__":
    main()
