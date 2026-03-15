import csv
import math

DEBUG = 0

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
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        for row in reader:
            if row["slot"] == "1":
                eff, qty = check_eff(row)
                if qty == 3:
                    count_dict[math.floor(eff)] = count_dict.get(math.floor(eff), 0) + 1
                    count_3 += 1
                count += 1
    print("Total :" + str(count_3))
    print(str(count_dict))



def main():
    analyze_3()

if __name__ == "__main__":
    main()
