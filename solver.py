#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

import ant_colony as ac
import local_search as ls
import greedy as g
import google_tools as gt


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)




def get_adj(points: list, n: int) -> list:
    adj: list = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            cost = distance(points[i], points[j])
            adj[i][j] = cost
            adj[j][i] = cost
    return adj




def solve_it(points, points_count):
    


    n = points_count
    


    if n < 120:
        adj = get_adj(points, n)
        #init_path, cost = ac.optimize(adj, 30, 0.01, 100, n)
        init_path = g.greedy_by_adj(adj, n)
        path, cost = ls.accurate_simulated_annealing(init_path, adj, n, 4000, 10, 0.99)

    elif n < 200:
        adj = get_adj(points, n)
        init_path = g.greedy_by_adj(adj, n)
        path, cost = ls.semi_accurate_simulated_annealing(init_path, adj, n, 4000, 10, 0.99)

    elif n < 20000:
        adj = get_adj(points, n)
        manager = gt.create_manager(n)
        model = gt.create_model(manager)
        transit_callback_index = gt.add_distance_callback(model, manager, adj)
        gt.set_arc_cost(model, transit_callback_index)
        search_parameters = gt.get_search_parameters()
        gt.set_time_limit(search_parameters, 300)
        assignment = gt.solve(model, search_parameters)
        path, cost = gt.get_answer(assignment, model, manager)
        cost = ac.get_path_cost(path, adj, n)

    else:
        path = g.greedy_by_nodes(points, n)
        cost = ls.get_cost_by_nodes(path, n, points)


   

    return path, cost
