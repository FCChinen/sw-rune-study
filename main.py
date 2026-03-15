import csv
import collections
import math

from eff import calc_eff

DEBUG = 0

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
        final_output.append(mapping_dict[row.get("s"+str(idx)+"_t", "")] + " " + \
            row.get("s"+str(idx)+"_v", 0))
    if row["i_t"]:
        final_output.append(mapping_dict[row.get("i_t", "")] + "i " + \
            row.get("i_v", 0))
    return final_output

def checking_stats(row: dict, stat: str) -> int:
    idx_list = [1,2,3,4]
    for idx in idx_list:
        if row["s"+str(idx)+"_t"] == stat:
            return int(row["s"+str(idx)+"_v"])
    return 0

def get_rune(row: dict) -> dict:
    idx_list = [1,2,3,4]
    rune = dict()
    for idx in idx_list:
        rune[row["s"+str(idx)+"_t"]] = row["s"+str(idx)+"_v"]
    return rune

def check_eff(row: dict) -> tuple:
    global DEBUG
    stat_list = ["ATK%", "CRate", "CDmg"]
    val_dict = dict()
    eff = 0.0
    stat_eff = 0.0
    count = 0
    for stat in stat_list:
        val = checking_stats(row, stat)
        if val > 0:
            count += 1
            if stat == "ATK%":
                stat_eff = val/8
                eff += stat_eff
            elif stat == "CRate":
                stat_eff = val/6
                eff += stat_eff
            elif stat == "CDmg":
                stat_eff = val/7
                eff += stat_eff
            val_dict[stat] = {
                stat: val,
                "eff": stat_eff
            }
    if math.floor(eff) == 3 and count == 3:
        print(get_rune(row))
        print(val_dict)
    if DEBUG:
        print(val_dict)
    return eff, count

def analyze_3():
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
            if row["slot"] == "1":
                eff, qty = check_eff(row)
                if qty == 3:
                    count_dict[math.floor(eff)] = count_dict.get(math.floor(eff), 0) + 1
                    count_dict = collections.OrderedDict(sorted(count_dict.items()))
                    count_3 += 1
                    b_stats= get_boozero_stats(row)
                    b_eff = calc_eff(b_stats)
                    fb_eff = math.floor(b_eff)
                    if fb_eff < 75:
                        print(b_stats, b_eff, eff)
                        _ = input()
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
    analyze_3()

if __name__ == "__main__":
    main()
