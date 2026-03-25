import glob
import os
import json

def get_files():
    path_pattern = os.path.join("./kept_runes/", "*.txt")
    return glob.glob(path_pattern)

def main():
    files = get_files()
    for file in files:
        lowest = 1000
        highest = 0
        with open(file, 'r') as f:
            data = json.loads(f.read())
            for r in data:
                if r["Score"] > highest:
                    highest = score
                if r["Score"] < lowest:
                    lowest = score

