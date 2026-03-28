import glob
import os
import json

path_pattern = os.path.join("./analysis/", "*.txt")
txt_files = glob.glob(path_pattern)

with open('./analysis/everything_TankSup_HP_Slot6.txt.txt', 'r') as f:
    data = json.loads(f.read())


