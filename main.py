import csv
import json
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

# The raw analysis is made to create the needed information of
# the runes by: stats and by slot
# (Needs to get runes-data.csv from SWOP Runes export:!)
# The output is the rune with their respective:
# - Raw stats
# - Boozero eff as BEff
# - Score(The official gaming score, it may vary by 1 point)
# - Adjusted Score(The official score adjusted to be a function
# that grews like Boozero eff)
def raw_analysis(stat_list: list, slots: list, match_qty: int):
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        i_75 = []
        i_75_84 = []
        i_84_95 = []
        i_95 = []
        count = [0, 0, 0, 0]
        lowest_84_95 = 1000
        lowest_75_84 = 1000
        highest_84_95 = 0
        highest_75_84 = 0
        total_amount = 0
        for row in reader:
            if "Slime" in row["monster_n"] or\
                "Forest"in row["monster_n"] or\
                "Inventory"in row["monster_n"]:
                row["monster_n"] = ""
            if row["monster_n"] != "":
                continue
            if row["slot"] in slots:
                qty = has_stats(row, stat_list)
                if qty == match_qty:
                    total_amount += 1
                    # just changing format to reuse the boozero eff function 
                    b_stats = get_boozero_stats(row)
                    #Excluding runes with spd
                    # getting the boozero efficiency
                    boozero_eff = calc_eff(b_stats)
                    # calculating the score, it may vary 1 point from the official
                    score = calc_score(b_stats)
                    # Is adjusted score to grow as boozero efficiency
                    adjusted_score = calc_adjusted_score(b_stats)
                    b_stats = filter_stats(b_stats)
                    b_eff = calc_eff(b_stats)
                    if boozero_eff < 75.0:
                        i_75.append(get_rune(row, b_eff, boozero_eff\
                                             , score, adjusted_score))
                        count[0] += 1
                    elif 75.0 <= boozero_eff < 85.0:
                        i_75_84.append(get_rune(row, b_eff, boozero_eff\
                                                , score, adjusted_score))
                        if adjusted_score > highest_75_84:
                            highest_75_84 = adjusted_score
                        elif adjusted_score < lowest_75_84:
                            lowest_75_84 = adjusted_score
                        count[1] += 1
                    elif 85.0 <= boozero_eff < 95.0:
                        i_84_95.append(get_rune(row, b_eff, boozero_eff\
                                                , score, adjusted_score))
                        if adjusted_score < lowest_84_95:
                            lowest_84_95 = adjusted_score 
                        elif adjusted_score > highest_84_95:
                            highest_84_95 = adjusted_score
                        count[2] += 1
                    elif 95.0 <= boozero_eff :
                        i_95.append(get_rune(row, b_eff, boozero_eff\
                                             , score, adjusted_score))
                        count[3] += 1
        print(f"less 75:{count[0]}\n75-84:{count[1]}\n85-95:{count[2]}\n95+:{count[3]}")
        print(f"lowest 84: {lowest_75_84}\n highest 84: {highest_75_84}\n")
        print(f"lowest 95: {lowest_84_95}\n highest 95: {highest_84_95}\n")
        print(f"total amount: {total_amount}")
        i_75 = sorted(i_75, key=lambda x: x["Score"])
        i_75_84 = sorted(i_75_84, key=lambda x: x["Score"])
        i_84_95 = sorted(i_84_95, key=lambda x: x["Score"])
        i_95 = sorted(i_95, key=lambda x: x["Score"])
        output_data("75", i_75)
        output_data("75_84", i_75_84)
        output_data("84_95", i_84_95)
        output_data("95", i_95)

def main():
    # stat_list = ["SPD", "HP%", "DEF%"] # Tank/Sup
    # stat_list = ["SPD", "ACC"'] # Control
    # stat_list = ["HP%", "CRate", "CDmg"] # HP-based bruiser
    # stat_list = ["DEF%", "CRate", "CDmg"] # Def-based bruiser
    stat_list = ["CDmg", "CRate", "ATK%"] # DPS
    # stat_list = []
    slots = ["1"]
    match_qty = 3
    raw_analysis(stat_list, slots, match_qty)

if __name__ == "__main__":
    main()
