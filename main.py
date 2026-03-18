import csv
import json
import collections
import math
from utils import *
from eff import calc_eff

def get_boozero_stats(row: dict) -> list:
    mapping_dict = {
            "CRate": "cr",
            "CDmg": "cd",
            "ATK%": "atk",
            "HP%": "hp",
            "DEF%": "def",
            "ATK flat": "atkm",
            "DEF flat": "defm",
            "HP flat": "hpm",
            "RES": "res",
            "ACC": "acc",
            "SPD": "spd"
    }
    final_output = []
    idx_list = [1,2,3,4]
    for idx in idx_list:
        if not(row.get("s"+str(idx)+"_t", "")):
            continue
        final_output.append(mapping_dict[row.get("s"+str(idx)+"_t", "")] + " " + \
            row.get("s"+str(idx)+"_v", 0))
    if row["i_t"]:
        final_output.append(mapping_dict[row.get("i_t", "")] + "i " + \
            row.get("i_v", 0))
    return final_output

def filter_stats(full_stats: list, filter: list = ["cr", "cd", "atk", "spd"]) -> list:
    filtered_stats = []
    for stat in full_stats:
        for f in filter:
            if f not in stat:
                continue
            filtered_stats.append(stat)
    return filtered_stats

def output_data(name: str, data: list):
    with open(f"{name}.txt", "w") as f:
        f.write(json.dumps(data, indent=4))

def analyze_2():
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        i_75 = []
        i_75_84 = []
        i_84_95 = []
        i_95 = []
        count = [0, 0, 0, 0]
        for row in reader:
            if row["slot"] == "1":
                stat_list = ["CDmg", "CRate", "ATK%"]
                eff, qty= check_eff(row, stat_list)
                if qty == 3:
                    b_stats= get_boozero_stats(row)
                    boozero_eff = calc_eff(b_stats)
                    b_stats = filter_stats(b_stats)
                    b_eff = calc_eff(b_stats)
                    if b_eff < 75.0:
                        i_75.append(get_rune(row, b_eff, boozero_eff))
                        count[0] += 1
                    elif 75.0 <= b_eff < 85.0:
                        i_75_84.append(get_rune(row, b_eff, boozero_eff))
                        count[1] += 1
                    elif 85.0 <= b_eff < 95.0:
                        i_84_95.append(get_rune(row, b_eff, boozero_eff))
                        count[2] += 1
                    elif 95.0 <= b_eff:
                        i_95.append(get_rune(row, b_eff, boozero_eff))
                        count[3] += 1
        print(f"less 75:{count[0]}\n75-84:{count[1]}\n85-95:{count[2]}\n95+:{count[3]}")
        output_data("75", i_75)
        output_data("75_84", i_75_84)
        output_data("84_95", i_84_95)
        output_data("95", i_95)

def analyze_1():
    count = 0
    count_3 = 0
    count_dict = {}
    final_dict = {}
    interval_75_less= 0
    interval_75_84 = 0
    interval_84_95 = 0
    interval_95_plus = 0
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        for row in reader:
            slot = ["1", "3", "5"]
            if row["slot"] in slot:
                eff, qty = check_eff(row)
                count_dict[math.floor(eff)] = count_dict.get(math.floor(eff), 0) + 1
                count_dict = collections.OrderedDict(sorted(count_dict.items()))
                count_3 += 1
                b_stats= get_boozero_stats(row)
                b_eff = calc_eff(b_stats)
                fb_eff = math.floor(b_eff)
                if fb_eff < 75:
                    interval_75_less += 1
                elif 75 <= fb_eff < 85:
                    interval_75_84 += 1
                elif 85 <= fb_eff < 95:
                    interval_84_95 += 1
                else:
                    interval_95_plus += 1
                final_dict[math.floor(b_eff)] = final_dict.get(math.floor(b_eff), 0) + 1
                # final_dict = collections.OrderedDict(sorted(final_dict.items()))
                count += 1
    print("Total :" + str(count_3))
    print(str(count_dict))
    print(str(final_dict))
    print(f"<75: {interval_75_less}")
    print(f"75 85: {interval_75_84}")
    print(f"85 95: {interval_84_95}")
    print(f">95: {interval_95_plus}")


def main():
    analyze_1()

if __name__ == "__main__":
    main()
