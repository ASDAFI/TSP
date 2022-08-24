from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def create_manager(points_count: int) -> pywrapcp.RoutingIndexManager:
    return pywrapcp.RoutingIndexManager(points_count,1, 0)

def create_model(manager: pywrapcp.RoutingIndexManager) -> pywrapcp.RoutingModel:
    model = pywrapcp.RoutingModel(manager)
    return model

def add_distance_callback(model: pywrapcp.RoutingModel ,manager: pywrapcp.RoutingIndexManager, distance_matrix : list):
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = model.RegisterTransitCallback(distance_callback)
    return transit_callback_index

def set_arc_cost(model: pywrapcp.RoutingModel, transit_callback_index: int):
    model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


def get_search_parameters():
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    '''
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)'''

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)

    return search_parameters

def set_time_limit(search_parameters: pywrapcp.DefaultRoutingSearchParameters, time_limit: int):
        search_parameters.time_limit.seconds = time_limit

def solve(model: pywrapcp.RoutingModel, search_parameters: pywrapcp.DefaultRoutingSearchParameters):

    assignment = model.SolveWithParameters(search_parameters)
    return assignment

def get_answer(assignment: pywrapcp.Assignment, model: pywrapcp.RoutingModel, manager: pywrapcp.RoutingIndexManager):
    """Prints solution on console."""
    index = model.Start(0)
    answer = []
    route_distance = 0
    while not model.IsEnd(index):
        answer.append(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(model.NextVar(index))
        route_distance += model.GetArcCostForVehicle(previous_index, index, 0)

    return answer, route_distance