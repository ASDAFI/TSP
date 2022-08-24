import random
import time


def choose_by_chance(factors: list) -> int:
    s: int = sum(factors)
    n: int = len(factors)

    chances: list = [factors[i] / s for i in range(n)]
    for i in range(1, n):
        chances[i] = chances[i - 1] + chances[i]

    r: float = random.random()
    for i in range(n):
        if r <= chances[i]:
            return i


def get_path_cost(path: list, adj: list, n: int) -> int:
    """
    get Path Cost in O(n) time complexity
    """
    cost: int = 0

    for i in range(1, n):
        cost += adj[path[i - 1]][path[i]]

    cost += adj[path[n - 1]][path[0]]

    return cost


def choose_path_by_pheromone(pheromone: list, n: int) -> list:
    """
    choose path by pheromone in O(n ^ 2) time complexity
    """
    start: int = 0
    path = [start]
    is_visited: list = [False for _ in range(n)]
    is_visited[start] = True

    for _ in range(n - 1):
        selected: int = -1
        selected_pheromone: int = -1
        for i in range(n):
            if is_visited[i]:
                continue
            if selected_pheromone < pheromone[path[-1]][i]:
                selected = i
                selected_pheromone = pheromone[path[-1]][i]
        path.append(selected)
        is_visited[selected] = True

    return path


def do_iteration(adj: list, pheromone: list, ants: int, evaporation: float, n: int) -> None:
    """
    do one iteration of Ant Colony Optimization in O(ants * n ^ 2) time complexity
    """

    current_node: list = [0 for _ in range(ants)]
    is_visited: list = [[True] + [False for _ in range(n - 1)] for _ in range(ants)]
    length_visited: list = [1 for _ in range(ants)]

    for _ in range(n):
        next_edges_for_pheromone: list = []
        for ant in range(ants):
            if length_visited[ant] == n:
                next_edges_for_pheromone.append([current_node[ant], 0])

                current_node[ant] = 0

                is_visited[ant] = [True] + [False for _ in range(n - 1)]
                length_visited[ant] = 1

                continue

            choices: list = []
            choices_reward: list = []

            for v in range(n):
                if is_visited[ant][v] or v == current_node[ant]:
                    continue
                choices.append(v)
                choices_reward.append(pheromone[current_node[ant]][v])

            is_visited[ant][current_node[ant]] = True
            length_visited[ant] += 1

            next_v = choices[choose_by_chance(choices_reward, )]
            next_edges_for_pheromone.append([current_node[ant], next_v])
            current_node[ant] = next_v

        for edge in next_edges_for_pheromone:
            pheromone[edge[0]][edge[1]] = (pheromone[edge[0]][edge[1]] + 1 / adj[edge[0]][edge[1]]) * (1 - evaporation)


def optimize(adj: list, ants: int, evaporation: float,
             epochs: int, n: int, deadlock: int = float("INF"), logging: bool = False,
             time_limit: float = float("INF")) -> tuple:
    """
    do Ant Colony Optimization in O(ants * n ^ 2 * epochs) time complexity
    """
    pheromone: list = [[1 for _ in range(n)] for _ in range(n)]

    best_path: list = []
    best_path_cost: float = float('inf')
    best_is_stable: int = 0
    start_time: float = time.time()

    for iteration in range(epochs):
        if best_is_stable >= deadlock or time.time() - start_time > time_limit:
            break
        do_iteration(adj, pheromone, ants, evaporation, n)

        current_path: list = choose_path_by_pheromone(pheromone, n)
        current_path_cost: float = get_path_cost(current_path, adj, n)

        if current_path_cost < best_path_cost:
            best_path = current_path
            best_path_cost = current_path_cost
        else:
            best_is_stable += 1

        if logging:
            print(f"Iteration: {iteration}\t Best Cost: {best_path_cost}\t Current Cost: {current_path_cost}")

    # best_path : list = choosePathByMephrone(mephrone, n)
    # best_path_cost : float = getPathCost(best_path, adj, n)

    return best_path, best_path_cost
