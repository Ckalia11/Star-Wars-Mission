import sqlite3
from collections import defaultdict, deque
import json
import os
from collections import defaultdict

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


# on any planet, it can either move to another planet, refuel till capacity, or wait any number of days
def traverse_graph(routes, departure, arrival, countdown, hunting, autonomy):
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

example_folder = "example2"
app_dir = "singlepage"

def get_millennium_data():
    
    autonomy_file_path = os.path.join(app_dir, "json_files", "examples", example_folder, "millennium-falcon.json")
    
    # read millennium-falcon.json file
    with open(autonomy_file_path) as r:
        millennium_dict = json.load(r)

    autonomy = millennium_dict.get("autonomy")
    departure = millennium_dict.get("departure")
    arrival = millennium_dict.get("arrival")
    routes_db = millennium_dict.get("routes_db")

    return (autonomy, departure, arrival, routes_db)

def get_empire_data(empire_file):
    empire_dict = json.load(empire_file)

    countdown = empire_dict.get("countdown")
    bounty_hunters = empire_dict.get("bounty_hunters")

    # map: planet -> list of days with bounty hunters
    hunting = defaultdict(list)

    for i in bounty_hunters:
        hunting[i.get("planet")].append(i.get("day"))
    
    return (countdown, hunting)

def get_routes(routes_db):
    db_path = os.path.join(app_dir, "json_files", "examples", example_folder, routes_db)
    curr = create_connection(db_path)
    routes = select_all_routes(curr)

    routes_dict = create_routes_dict(routes)

    return routes_dict




