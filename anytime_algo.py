from DirectedGraph import *
from search import * #for search engines
from hotelAndScenery import *


def heur_zero(state):
    return 0


def tsp_goal_state(state):
    return len(state.get_vertices()) == 1


def fval_function(sN, weight):
    return sN.gval + weight * sN.hval


def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    se = SearchEngine('best_first', 'none')
    se.init_search(initial_state, goal_fn=tsp_goal_state, heur_fn=heur_fn)
    cur_time = os.times()[0]
    start_time = os.times()[0]
    solutions = [None]
    costbound = (float('inf'), float('inf'), float('inf'))
    while timebound > 0:
        solution = se.search(timebound, costbound)
        if solution:
            if solution.gval < costbound[0]:
                costbound = (solution.gval, float('inf'), float('inf'))
                solutions.pop()
                solutions.append(solution)
        else:
            print("=======================================================")
            print("Solution found in {} secs.".format(os.times()[0] - start_time))
            break
        timebound = timebound - (os.times()[0] - cur_time)
        cur_time = os.times()[0]
    return False if solutions[0] is None else solutions[0]


