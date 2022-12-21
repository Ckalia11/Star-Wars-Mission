
# cli
from singlepage.functions import get_probability_success
import os
from collections import defaultdict
import sys
from pathlib import Path
import json

args_count = len(sys.argv)
# check if more arguments than expected
if args_count > 3:
    print(f"Two arguments expected, got {args_count - 1}")
    raise SystemExit(1)
# check if less arguments than expected
elif len(sys.argv) < 3:
    print("You must specify paths to the millennium-falcon.json and empire.json files")
    raise SystemExit(1)
# check arguments type
if not (isinstance(sys.argv[1], str) and isinstance(sys.argv[2], str)):
    print("The file paths must be strings")
    raise SystemExit(2)
millennium_path = Path(sys.argv[1])
empire_path = Path(sys.argv[2])
# check if path exists
if not os.path.isfile(millennium_path):
    print("The millennium-falcon.json file doesn't exist")
    raise SystemExit(3)
if not os.path.isfile(empire_path):
    print("The empire.json file doesn't exist")
    raise SystemExit(3)

with open(empire_path) as empire_file:
    probability_success = get_probability_success(millennium_path, empire_file)
    print((int(100 * probability_success)))





