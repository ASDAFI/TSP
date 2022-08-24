import math
import random


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


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def lazy_get_neighbours(permutation: list, n: int):
    """
    get answer neighbours in O(n^2) time complexity
    """

    for i in range(n):
        for j in range(i + 1, n):
            permutation[i], permutation[j] = permutation[j], permutation[i]
            yield permutation
            permutation[i], permutation[j] = permutation[j], permutation[i]


def get_cost_by_adj(path: list, n: int, adj: list) -> int:
    """
    get cost by adj in O(n) time complexity
    """

    cost = 0
    for i in range(n):
        cost += adj[path[i]][path[(i + 1) % n]]
    return cost


def get_cost_by_nodes(path: list, n: int, nodes: list) -> int:
    """
    get cost by nodes in O(n) time complexity
    """

    cost = 0
    for i in range(n):
        cost += distance(nodes[path[i]], nodes[path[(i + 1) % n]])
    return cost


def accurate_simulated_annealing(init_path: list, adj: list, n: int, start_temp: float, end_temp: float,
                                 cooling_rate: float) -> list:

    path = init_path.copy()
    cost = get_cost_by_adj(path, n, adj)

    best_path = path.copy()
    best_cost = cost

    current_temp = start_temp

    while current_temp > end_temp:
        is_accepted = False
        for neighbour in lazy_get_neighbours(path, n):
            neighbour_cost = get_cost_by_adj(neighbour, n, adj)
            delta_energy = cost - neighbour_cost

            if delta_energy > 0:
                if neighbour_cost < best_cost:
                    best_cost = neighbour_cost
                    best_path = neighbour.copy()

                path = neighbour.copy()
                cost = neighbour_cost
                is_accepted = True

        if not is_accepted:
            chances = []

            for neighbour in lazy_get_neighbours(path, n):
                neighbour_cost = get_cost_by_adj(neighbour, n, adj)
                delta_energy = cost - neighbour_cost

                chance = math.exp(delta_energy / current_temp)
                chances.append(chance)
            index = choose_by_chance(chances)
            current_index = 0
            for neighbour in lazy_get_neighbours(path, n):
                if current_index == index:
                    path = neighbour.copy()
                    cost = neighbour_cost
                    break
                current_index += 1

        current_temp *= cooling_rate

    return best_path, best_cost

def semi_accurate_simulated_annealing(init_path: list, adj: list, n: int, start_temp: float, end_temp: float,
                                 cooling_rate: float) -> list:

    path = init_path.copy()
    cost = get_cost_by_adj(path, n, adj)

    best_path = path.copy()
    best_cost = cost

    current_temp = start_temp

    while current_temp > end_temp:
        is_accepted = False
        for neighbour in lazy_get_neighbours(path, n):
            neighbour_cost = get_cost_by_adj(neighbour, n, adj)
            delta_energy = cost - neighbour_cost

            if delta_energy > 0:
                if neighbour_cost < best_cost:
                    best_cost = neighbour_cost
                    best_path = neighbour.copy()

                path = neighbour.copy()
                cost = neighbour_cost
                is_accepted = True


        if not is_accepted:
            for neighbour in lazy_get_neighbours(path, n):
                neighbour_cost = get_cost_by_adj(neighbour, n, adj)
                delta_energy = cost - neighbour_cost

                if math.exp(delta_energy / current_temp) > random.random():
                    path = neighbour.copy()
                    cost = neighbour_cost
                    break



        current_temp *= cooling_rate
    return best_path, best_cost

def fast_simulated_annealing(init_path: list, adj: list, n: int, start_temp: float, end_temp: float,
                                 cooling_rate: float) -> list:

    path = init_path.copy()
    cost = get_cost_by_adj(path, n, adj)

    best_path = path.copy()
    best_cost = cost

    current_temp = start_temp

    while current_temp > end_temp:

        for neighbour in lazy_get_neighbours(path, n):
            neighbour_cost = get_cost_by_adj(neighbour, n, adj)
            delta_energy = cost - neighbour_cost

            if delta_energy > 0:
                if neighbour_cost < best_cost:
                    best_cost = neighbour_cost
                    best_path = neighbour.copy()

                path = neighbour.copy()
                cost = neighbour_cost
                break
            elif math.exp(delta_energy / current_temp) > random.random():
                path = neighbour.copy()
                cost = neighbour_cost
                break




        current_temp *= cooling_rate
        print(current_temp)

    return best_path, best_cost

def ultra_fast_simulated_annealing(init_path: list, nodes : list, n: int, start_temp: float, end_temp: float,
                                 cooling_rate: float) -> list:

    path = init_path.copy()
    cost = get_cost_by_nodes(path, n, nodes)

    best_path = path.copy()
    best_cost = cost

    current_temp = start_temp

    while current_temp > end_temp:

        for neighbour in lazy_get_neighbours(path, n):
            neighbour_cost = get_cost_by_nodes(neighbour, n, nodes)
            delta_energy = cost - neighbour_cost

            if delta_energy > 0:
                if neighbour_cost < best_cost:
                    best_cost = neighbour_cost
                    best_path = neighbour.copy()

                path = neighbour.copy()
                cost = neighbour_cost
                break
            elif math.exp(delta_energy / current_temp) > random.random():
                path = neighbour.copy()
                cost = neighbour_cost
                break




        current_temp *= cooling_rate
        print(current_temp)

    return best_path, best_cost