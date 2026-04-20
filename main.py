import csv
import json
from utils import *

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
        value = int(row.get("s"+str(idx)+"_v", 0))
        minus = json.loads(row.get("s"+str(idx)+"_data", "{}"))
        minus = minus.get("gvalue", "0")
        value -= int(minus)
        final_output.append(mapping_dict[row.get("s"+str(idx)+"_t", "")]\
            + " " + str(value))
    if row["i_t"]:
        final_output.append(mapping_dict[row.get("i_t", "")] + "i " + \
            row.get("i_v", 0))
    return final_output

def filter_stats(full_stats: list, filter: list = []) -> list:
    filtered_stats = []
    for stat in full_stats:
        for f in filter:
            if f not in stat:
                continue
            filtered_stats.append(stat)
            break
    return filtered_stats

def output_data(name: str, data: list):
    with open(f"{name}.json", "w") as f:
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
def raw_analysis(stat_list: list, f_stats: list, \
                 slots: list, match_qty: int, \
                 main_stat: str = "", filename: str = ""):
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        filtered_best = []
        total_amount = 0
        for row in reader:
            if slots[0] in ["2", "4", "6"]:
                if main_stat != row["m_t"]:
                    continue
            if "Slime" in row["monster_n"] or\
                "Forest"in row["monster_n"] or\
                "Inventory"in row["monster_n"]:
                row["monster_n"] = ""
            if row["monster_n"] != "":
                continue
            if row["slot"] in slots:
                qty = has_stats(row, stat_list)
                if qty >= match_qty:
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
                    filtered_stats = filter_stats(b_stats, f_stats)
                    # Adjusted score adjusted to only filtered stats
                    b_eff = calc_score(filtered_stats)
                    gem = is_gemmed(row)
                    filtered_best.append(
                        get_rune(
                            row = row,
                            eff = b_eff,
                            boozero_eff = boozero_eff,
                            score = score,
                            adjusted_score = adjusted_score,
                            is_gemmed = gem
                        )
                    )
        filtered_best = sorted(filtered_best, key=lambda x: x["Eff"])
        output_data(f"./analysis/{filename}_Slot{slots[0]}", filtered_best)

# Creating a new function to get analysis of the BEST RUNES 
def best_analysis(slots: list,\
                 filename: str = ""):
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        total_amount = 0
        filtered_best = []
        for row in reader:
            if "Slime" in row["monster_n"] or\
                "Forest"in row["monster_n"] or\
                "Inventory"in row["monster_n"]:
                row["monster_n"] = ""
            if row["monster_n"] != "":
                continue
            if row["slot"] in slots:
                total_amount += 1
                # just changing format to reuse the boozero eff function 
                b_stats = get_boozero_stats(row)
                # getting the boozero efficiency
                boozero_eff = calc_eff(b_stats)
                # calculating the score, it may vary 1 point from the official
                score = calc_score(b_stats)
                # Is adjusted score to grow as boozero efficiency
                adjusted_score = calc_adjusted_score(b_stats)
                stat_list = ["spd", "spdi", "cr", "cri", "cd", "cdi", "atk", "atki"]
                dps_score = calc_eff(filter_stats(b_stats, stat_list))
                stat_list = ["cr", "cri", "cd", "cdi", "atk", "atki"]
                slow_dps_score = calc_eff(filter_stats(b_stats, stat_list))
                stat_list = ["spd", "spdi", "hp", "hpi", "def", "defi", "res", "resi"] # Tank/Sup
                tank_score = calc_eff(filter_stats(b_stats, stat_list))
                stat_list = ["spd", "spdi", "acc", "acci"] # Control
                control_score = calc_eff(filter_stats(b_stats, stat_list))
                stat_list = ["spd", "spdi", "hp", "hpi",
                             "def", "defi", "atk", "atki",
                             "cr", "cri", "cd", "cdi"] # bruiser
                bruiser_score = calc_eff(filter_stats(b_stats, stat_list))
                # Adjusted score adjusted to only filtered stats
                gem = is_gemmed(row)
                filtered_best.append(
                    get_rune(
                        row=row,
                        eff=0,
                        boozero_eff=boozero_eff,
                        score=score,
                        adjusted_score=adjusted_score,
                        slow_dps_score=slow_dps_score,
                        dps_score=dps_score,
                        tank_score=tank_score,
                        control_score=control_score,
                        bruiser_score=bruiser_score,
                        is_gemmed = gem,
                        ))
        filtered_best = sorted(filtered_best, key=lambda x: x["AdjustedScore"])
        output_data(f"./analysis/{filename}_Slot{slots[0]}", filtered_best)
def everything():
    filename = "Everything"
    slots = [[str(i)] for i in range(1,7)]
    for slot in slots:
        best_analysis(slot,filename)

def dps():
    # stat_list = ["SPD", "HP%", "DEF%", "RES", "CRate", "CDmg", "ATK%", "ACC"] # Everything
    # stat_list = ["SPD", "HP%", "DEF%", "RES"] # Tank/Sup
    # stat_list = ["SPD", "ACC"'] # Control
    # stat_list = ["SPD", "HP%", "CRate", "CDmg"] # HP-based bruiser
    # stat_list = ["SPD", "DEF%", "CRate", "CDmg"] # Def-based bruiser
    # stat_list = ["CDmg", "CRate", "ATK%"] # DPS
    # stat_list = ["CDmg", "CRate"] # DPS for slot 3
    # stat_list = ["SPD", "CRate", "CDmg", "ATK%"] # FastDPS for slot 1/3/5
    # The stats are after the mapping so needs to be like this
    # f_stats = ['spd', 'spdi', 'hp', 'hpi', 'def', 'defi', 'res'] # Tank/Support
    # stat_list = []
    match_qty = 1
    # only needed for 2/4/6
    for filename in ["FastDPS", "SlowDPS"]:
        for i in range(1,7):
            if filename == "FastDPS":
                f_stats = ['cr', 'cri', 'atk', 'atki' , 'cd', 'cdi', 'spd', 'spdi'] # FastDPS
                slots = [str(i)]
                if i in [1,3,5]:
                    stat_list = ["SPD", "CRate", "CDmg", "ATK%"] # FastDPS for slot 1/3/5
                    raw_analysis(stat_list, f_stats, slots, match_qty, "", filename)
                elif i == 2:
                    stat_list = ["CRate", "ATK%", "CDmg"] # FastDPS SPD for slot 2 or Slow slot 1/3/5
                    raw_analysis(stat_list, f_stats, slots, match_qty, "SPD", filename+"_SPD")
                    stat_list = ["SPD", "CRate", "CDmg"] # FastDPS for slot 2/6
                    raw_analysis(stat_list, f_stats, slots, match_qty, "ATK%", filename)
                elif i == 6:
                    stat_list = ["SPD", "CRate", "CDmg"] # FastDPS for slot 2/6
                    raw_analysis(stat_list, f_stats, slots, match_qty, "ATK%", filename)
                else:
                    stat_list = ["CRate", "ATK%", "SPD"] # FastDPS for slot 4
                    raw_analysis(stat_list, f_stats, slots, match_qty, "CDmg", filename)
            else:
                f_stats = ['cr', 'cri', 'atk', 'atki' , 'cd', 'cdi'] # SlowDPS
                slots = [str(i)]
                if i in [1,3,5]:
                    stat_list = ["CRate", "ATK%", "CDmg"] # FastDPS SPD for slot 2 or Slow slot 1/3/5
                    raw_analysis(stat_list, f_stats, slots, match_qty, "", filename)
                elif i in [2, 6]:
                    stat_list = ["CRate", "CDmg"] # SlowDPS for slot 2/6
                    raw_analysis(stat_list, f_stats, slots, match_qty, "ATK%", filename)
                else:
                    stat_list = ["CRate", "ATK%"] # SlowDPS for slot 4
                    raw_analysis(stat_list, f_stats, slots, match_qty, "CDmg", filename)


if __name__ == "__main__":
    # dps()
    everything()
