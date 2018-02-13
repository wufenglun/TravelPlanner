from DirectedGraph import *
from propagators import *
from data import *
from hotelAndScenery import *
from tsp_csp import *
from anytime_algo import *


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print("=======================================================")
    print("Welcome! This is a simple travel planner program.")
    print("You can choose a hotel you are going to stay and several attractions you are going to visit in Toronto.")
    print("We will give you a best travelling solution that spend least time on road. Enjoy! ")
    print("=======================================================")
    answer = True
    while answer:
        while True:
            print("0 for a csp solver.")
            print("1 for a anytime greedy best first search solver.")
            sol = input("Which solver are you going to use: ")
            if is_number(sol) and int(sol) in [0, 1]:
                break
            else:
                print("Please enter a valid number. ")
        solver = int(sol)
        h_nodes = ['1', '2', '3', '4', '5']
        s_nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        print(" 1. Chelsea Hotel(Downtown), 2. Central Hotel(Downtown), 3. Best Western(Markham)")
        print(" 4. Seneca Residence(North York), 5. Delta (Scarborough)")
        while True:
            hotel = input("Which hotel are you living: ")
            if hotel in h_nodes:
                break
            else:
                print("Please choose a hotel in the above list. ")
        simple_tsp = DirectedGraph('start', 0, None, hotel, hotel)
        v_list = [hotel]
        if solver == 0:
            while True:
                num = input("How many places are you planning to visit (up to four): ")
                if num not in ['1', '2', '3', '4']:
                    print("Please provide a valid number. ")
                else:
                    break
            print("A. University of Toronto B. Casa Loma C. Dundas Square D. Air Canada Centre")
            print("E. Unionville F. CN Tower G. CNE H. Yorkdale I. Toronto Island J. Vaughan mills")
            count = 0
            while count < int(num):
                place = input("Which places are you planning to visit: ")
                place = place.upper()
                if place in s_nodes and place not in v_list:
                    v_list.append(place)
                    count += 1
                else:
                    print("Please choose a destination in the above list and not repeated. ")
            simple_tsp.create_vertices_list(v_list)
            for i in range(len(v_list)):
                vertex = v_list[i]
                vertices_copy = v_list[:]
                vertices_copy.remove(vertex)
                for j in range(len(vertices_copy)):
                    simple_tsp.add_edge(v_list[i], vertices_copy[j], dict_weight[(v_list[i], vertices_copy[j])])

            start_time = os.times()[0]
            csp, var_array = tsp_model(simple_tsp)
            solver = BT(csp)
            print("=======================================================")
            solver.bt_search(prop_BT)
            print("Solution 1:")
            if len(v_list) == 5:
                satisfying_tuples = five()
            else:
                satisfying_tuples = []
                n = len(v_list)-1
                for i in range(len(v_list)-1):
                    n += i
                n = n * 2
                l = [bin(x)[2:].rjust(n, '0') for x in range(2 ** n)]
                for item in l:
                    temp = list(item)
                    for i in range(len(temp)):
                        temp[i] = int(temp[i])
                    sum = 0
                    for i in temp:
                        sum += i
                    if sum == len(v_list):
                        satisfying_tuples.append(temp)
            sols = []
            sol = []
            for var in csp.get_all_vars():
                if var.get_assigned_value() == 1:
                    print(var)
                    sol.append(1)
                else:
                    sol.append(0)
            sols.append(sol)
            c = Constraint('all', var_array)
            satisfying_tuples.remove(sol)
            c.add_satisfying_tuples(satisfying_tuples)
            csp.add_constraint(c)

            sum = 0
            for i in range(len(sol)):
                if sol[i] == 1:
                    node1 = var_array[i].name[0]
                    node2 = var_array[i].name[1]
                    sum += simple_tsp.get_weight((node1, node2))
            print("Total weight is {}".format(sum))
            print("=======================================================")
            count = 2
            while True:
                if solver.bt_search(prop_BT):
                    print("Solution {}:".format(count))
                    count += 1
                    sol = []
                    for var in csp.get_all_vars():
                        if var.get_assigned_value() == 1:
                            print(var)
                            sol.append(1)
                        else:
                            sol.append(0)
                    csp.cons.pop()
                    c = Constraint('all', var_array)
                    satisfying_tuples.remove(sol)
                    c.add_satisfying_tuples(satisfying_tuples)
                    csp.add_constraint(c)
                    sols.append(sol)

                    sum = 0
                    for i in range(len(sol)):
                        if sol[i] == 1:
                            node1 = var_array[i].name[0]
                            node2 = var_array[i].name[1]
                            sum += simple_tsp.get_weight((node1, node2))
                    print("Total weight is {}".format(sum))
                    print("=======================================================")
                else:
                    break

            min = 2**100
            m_dict = {}
            for sol in sols:
                sum = 0
                for i in range(len(sol)):
                    if sol[i] == 1:
                        node1 = var_array[i].name[0]
                        node2 = var_array[i].name[1]
                        sum += simple_tsp.get_weight((node1, node2))
                if sum < min:
                    min = sum
                    m_dict[min] = sol

            print("=======================================================")
            finish_time = os.times()[0]
            print("The solution found in {} secs.".format(finish_time-start_time))
            print("The best solution to plan your trip:")
            print("Total time spend on road is {} mins.".format(min))
            print("=======================================================")
            dict_sol = {}
            for i in range(len(m_dict[min])):
                if m_dict[min][i] == 1:
                    dict_sol[var_array[i].name[0]] = (var_array[i].name[0], var_array[i].name[1])
            lst_dict_sol = list(dict_sol.keys())
            lst_dict_sol.sort()
            a = lst_dict_sol[0]
            for i in range(len(lst_dict_sol)):
                print(dict_name[dict_sol[a][0]], "to", dict_name[dict_sol[a][1]], "takes",
                      simple_tsp.get_weight((dict_sol[a][0], dict_sol[a][1])), "mins.")

                a = dict_sol[a][1]
        else:
            print("A. University of Toronto B. Casa Loma C. Dundas Square D. Air Canada Centre")
            print("E. Unionville F. CN Tower G. CNE H. Yorkdale I. Toronto Island J. Vaughan mills")
            while True:
                num = input("How many places are you planning to visit (1 to 10): ")
                if not is_number(num):
                    print("Please provide a number. ")
                elif is_number(num) and (int(num) < 1 or int(num) > 10):
                    print("Please provide a valid number. (1 to 10)")
                else:
                    break
            if int(num) == 10:
                v_list.extend(s_nodes)
            else:
                count = 0
                while count < int(num):
                    place = input("Which places are you planning to visit: ")
                    place = place.upper()
                    if place in s_nodes and place not in v_list:
                        v_list.append(place)
                        count += 1
                    else:
                        print("Please choose a destination in the above list and not repeated. ")

            simple_tsp.create_vertices_list(v_list)
            for i in range(len(v_list)):
                vertex = v_list[i]
                vertices_copy = v_list[:]
                vertices_copy.remove(vertex)
                for j in range(len(vertices_copy)):
                    simple_tsp.add_edge(v_list[i], vertices_copy[j], dict_weight[(v_list[i], vertices_copy[j])])

            timebound = 30
            solution = anytime_gbfs(simple_tsp, heur_fn=heur_zero, timebound=timebound)
            if solution:
                print("The best solution to plan your trip:")
                solution.print_path()
        print("=======================================================")
        while True:
            answer = input("Do you want to try another input? (yes or no)")
            if answer == "yes":
                answer = True
                break
            elif answer == 'no':
                answer = False
                break
            else:
                print("Please provide a valid input.")