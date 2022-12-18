# read autonomy json file

from db_functions import create_connection, select_all_routes, create_routes_dict, traverse_graph_1, compute_probability_success

import json
import os
from collections import defaultdict

# assumes curr directory is 'submission'

autonomy_file_path = os.path.join("example4", "millennium-falcon.json")
empire_file_path = os.path.join("example4", "empire.json")


with open(autonomy_file_path) as r:
    millennium_dict = json.load(r)

autonomy = millennium_dict.get("autonomy")
departure = millennium_dict.get("departure")
arrival = millennium_dict.get("arrival")
routes_db = millennium_dict.get("routes_db")

# can be relative to millennium.json file or absolute
db_path = os.path.join("example4", routes_db)

with open(empire_file_path) as r:
    empire_dict = json.load(r)

countdown = empire_dict.get("countdown")
bounty_hunters = empire_dict.get("bounty_hunters")

# map: planet -> list of days with bounty hunters

hunting = defaultdict(list)

for i in bounty_hunters:
    hunting[i.get("planet")].append(i.get("day"))

curr = create_connection(db_path)
routes = select_all_routes(curr)
routes_dict = create_routes_dict(routes)
bounty_encounters = traverse_graph_1(routes_dict, departure, arrival, countdown, hunting, autonomy)
# print(bounty_encounters)
print(compute_probability_success(bounty_encounters))



