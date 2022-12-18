import sqlite3
from collections import defaultdict, deque

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def select_all_routes(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM ROUTES")

    rows = cur.fetchall()

    return rows

def create_routes_dict(routes):
    routes_dict = defaultdict(list)
    for route in routes:
        start = route[0]
        end = route[1]
        travel_days = route[2]
        routes_dict[start].append((end, travel_days))
    return routes_dict

# bfs
# maxamize probability while being under countdown
# on any planet, it can either move to another planet, refuel till capacity, or wait any number of days
# def traverse_graph(routes, departure, arrival, countdown, hunting, autonomy):
#     queue = deque([[departure, autonomy]])
#     # maps location -> smallest bounty encounters from start to location
#     locations = {}
#     locations[departure] = [0, 0]
#     while queue:
#         start, fuel = queue.pop()
#         # not every location is a start
#         if start in routes:
#             for stop_info in routes[start]:
#                 curr_fuel = fuel
#                 stop = stop_info[0]
#                 travel_days = stop_info[1]
#                 need_refuel = False
#                 day_number = locations[start][1]
#                 day_at_stop = day_number + travel_days
#                 # check if there is enough fuel to travel and travel to stop is less than countdown:
#                 if curr_fuel >= travel_days and day_at_stop <= countdown:
#                     # count number of encounters with bounty hunters
#                     bounty_encounters = 0
#                     if stop in hunting:
#                         if day_at_stop in hunting[stop]:
#                             bounty_encounters += 1
#                             # check if need to refuel
#                             need_refuel = True if curr_fuel == travel_days else False
#                             if need_refuel:
#                                 bounty_encounters += 1
#                     # decrement fuel
#                     curr_fuel -= travel_days
#                     # compare bounty encounters
#                     if bounty_encounters not in locations:
#                         locations[stop] = [bounty_encounters, day_at_stop]
#                     else:
#                         if bounty_encounters < locations[stop][0]:
#                             locations[stop] = [bounty_encounters, day_at_stop]
#                         # add its children 
#                         if stop in routes:
#                             for children in routes[stop]:
#                                 # add child name to queue
#                                 queue.append([children[0], fuel])
#                         else:
#                             pass
#         else:
#             # nothing to be done
#             continue
                
#     return locations[arrival]

# on any planet, it can either move to another planet, refuel till capacity, or wait any number of days
def traverse_graph_1(routes, departure, arrival, countdown, hunting, autonomy):
    cache = {}
    def solve(departure, fuel, day, bounty_encounters):
        # if departure == arrival:
        #     print("departure ", departure, "fuel ", fuel, "day ", day, "bounty_encounters ", bounty_encounters)
        if day > countdown or fuel < 0:
            return float("inf")
        if departure == arrival:
            return bounty_encounters
        if departure not in routes:
            return float("inf")
        # if (departure, fuel, day, bounty_encounters) in cache:
        #     return cache[(departure, fuel, day, bounty_encounters)]
        encounter_bounty = False
        if departure in hunting and day in hunting[departure]:
            encounter_bounty = True
        # move to another planet
        minimum_travel_time = float("inf")
        min_move = float("inf")
        for stop_info in routes[departure]:
            stop_name = stop_info[0]
            travel_time = stop_info[1]
            minimum_travel_time = min(minimum_travel_time, travel_time)
            move = solve(stop_name, fuel - travel_time, day + travel_time, bounty_encounters + 1) if encounter_bounty else solve(stop_name, fuel - travel_time, day + travel_time, bounty_encounters)
            min_move = min(min_move, move)
        # wait/refuel
        min_refuel = float("inf")
        # number of days the ship can wait before it has to travel
        for d in range(1, countdown - minimum_travel_time - day + 1):
            refuel = solve(departure, autonomy, day + d, bounty_encounters + d) if encounter_bounty else solve(departure, autonomy, day + d, bounty_encounters)
            min_refuel = min(min_refuel, refuel)
        min_total = min(min_move, min_refuel) 
        # cache[(departure, fuel, day, bounty_encounters)] = min_total
        return min_total

    res = solve(departure, autonomy, 0, 0)
    return 0 if res == float("inf") else res



# returns probability of being captured
def compute_probability_success(bounty_encounters):
    if bounty_encounters == 0:
        return 1
    if bounty_encounters == 1:
        return 1 - 1/10
    k = bounty_encounters - 1
    probability = 1/10 + (9**k / 10**(k + 1))
    return 1 - probability
