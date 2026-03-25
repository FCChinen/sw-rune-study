import glob
import os
import json

path_pattern = os.path.join("./analysis/", "*.txt")
txt_files = glob.glob(path_pattern)

with open('./kept_runes/TankSup_Slot1.txt', 'r') as f:
    data = json.loads(f.read())

sets = dict()
for r in data:
    sets[r["Set"]] = sets.get(r["Set"], 0) + 1

print(sets)

print(txt_files)
