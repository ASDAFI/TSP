import math

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def greedy_by_adj(adj: list, n: int) -> list:
    """
    choose path by adj in O(n ^ 2) time complexity
    """

    start: int = 0
    path = [start]
    is_visited: list = [False for _ in range(n)]
    is_visited[start] = True

    for _ in range(n - 1):
        selected: int = -1
        selected_adj: int = float("inf")
        for i in range(n):
            if is_visited[i] or path[-1] == i:
                continue
            if selected_adj > adj[path[-1]][i]:
                selected = i
                selected_adj = adj[path[-1]][i]
        path.append(selected)
        is_visited[selected] = True

    return path

def greedy_by_nodes(nodes: list, n: int) -> list:
    """
    choose path by nodes in O(n ^ 2) time complexity
    """

    start: int = 0
    path = [start]
    is_visited: list = [False for _ in range(n)]
    is_visited[start] = True

    for _ in range(n - 1):
        selected: int = -1
        selected_node: int = float("inf")
        for i in range(n):
            if is_visited[i] or path[-1] == i:
                continue
            if selected_node > distance(nodes[path[-1]], nodes[i]):
                selected = i
                selected_node = distance(nodes[path[-1]], nodes[i])
        path.append(selected)
        is_visited[selected] = True

    return path