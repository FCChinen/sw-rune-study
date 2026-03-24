import glob
import os

path_pattern = os.path.join("./analysis/", "*.txt")
txt_files = glob.glob(path_pattern)

print(txt_files)
