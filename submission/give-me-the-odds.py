import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("millennium_path")
parser.add_argument("empire_path")

args = parser.parse_args()


millennium_path = Path(args.millennium_path)
empire_path = Path(args.empire_path)


if not millennium_path.exists():
    print("The path to the millennium-falcon.json file doesn't exist")
    raise SystemExit(1)

if not empire_path.exists():
    print("The path to the empire.json file doesn't exist")
    raise SystemExit(1)

