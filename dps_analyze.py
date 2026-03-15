import csv
import json

def is_dmg(stat: str) -> bool:
    dmg_stats = ["ATK%", "CRate", "CDmg"]
    if stat in dmg_stats:
        return True
    return False

def checking_stats(row: dict) -> int:
    stats_list = ["s1_t", "s2_t", "s3_t", "s4_t"]
    count = 0
    for stat in stats_list:
        if (is_dmg(row[stat])):
            count += 1
    return count

def check_slot(row: dict, slot: str) -> bool:
    if row["slot"] == slot:
        return True
    return False

def analyze():
    count = 0
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        for row in reader:
            if check_slot(row, "1"):
                count +=1
    print("count: ", count)


def main():
    analyze()

if __name__ == "__main__":
    main()
