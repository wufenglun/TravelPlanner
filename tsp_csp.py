from cspbase import *
from itertools import *


def tsp_model(tsp):
    vertices = tsp.get_vertices()
    vars = {}
    var_array = []
    len_v = len(vertices)
    cons = []
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            v_name = vertices[i] + vertices[j]
            vars[v_name] = Variable(v_name, [0, 1])

            v_name = vertices[j] + vertices[i]
            vars[v_name] = Variable(v_name, [0, 1])

    for i in range(len(vertices)):
        vertex = vertices[i]
        vertices_copy = vertices[:]
        vertices_copy.remove(vertex)
        scope = []
        for j in range(len(vertices_copy)):
            temp = vars[vertices[i]+vertices_copy[j]]
            scope.append(temp)
        c = Constraint('out', scope)
        satisfying_tuples = []
        temp = []
        for i in range(len_v - 1):
            temp.append(0)
        for i in range(len_v - 1):
            temp_copy = temp[:]
            temp_copy[i] = 1
            satisfying_tuples.append(temp_copy)
        c.add_satisfying_tuples(satisfying_tuples)
        cons.append(c)

    for i in range(len(vertices)):
        vertex = vertices[i]
        vertices_copy = vertices[:]
        vertices_copy.remove(vertex)
        scope = []
        for j in range(len(vertices_copy)):
            temp = vars[vertices_copy[j]+vertices[i]]
            scope.append(temp)
        c = Constraint('in', scope)
        satisfying_tuples = []
        temp = []
        for i in range(len_v - 1):
            temp.append(0)
        for i in range(len_v - 1):
            temp_copy = temp[:]
            temp_copy[i] = 1
            satisfying_tuples.append(temp_copy)
        c.add_satisfying_tuples(satisfying_tuples)
        cons.append(c)

    facs = vertices
    l1 = []
    l2 = []
    for pattern in product([True, False], repeat=len(facs)):
        l1.append([x[1] for x in zip_longest(pattern, facs) if x[0]])
        l2.append([x[1] for x in zip_longest(pattern, facs) if not x[0]])
    l1.remove(l1[0])
    l2.remove(l2[0])
    l1.remove(l1[-1])
    l2.remove(l2[-1])
    for i in range(len(l1)):
        scope = []
        for j in l1[i]:
            for k in l2[i]:
                scope.append(vars[j+k])

        n = len(scope)
        satisfying_tuples = [[int(i) for i in bin(x)[2:].rjust(n, '0')] for x in range(2 ** n)]
        satisfying_tuples.remove(satisfying_tuples[0])

        c = Constraint('nst', scope)
        c.add_satisfying_tuples(satisfying_tuples)
        cons.append(c)

    for var in vars:
        var_array.append(vars[var])

    csp = CSP("TSP", var_array)
    for c in cons:
        csp.add_constraint(c)
    return csp, var_array