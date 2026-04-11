import json
from typing import Tuple

def check_qty(rune: dict, stat_list: list, max_qty: int):
    qty = 0
    has = []
    for stat in stat_list:
        exist = rune.get(stat) or rune.get(stat+"I")
        if exist:
            qty += 1
            has.append(stat)

    if qty <= max_qty:
        return [rune for rune in stat_list if rune not in has]
    return []

def get_gem_stats(gem_stat: list) -> Tuple[int, str]:
    if "ATK%" in gem_stat:
        return 28, "ATK%"
    elif "SPD" in gem_stat:
        return 27, "SPD"
    elif "CRate" in gem_stat:
        return 24, "CRate"
    else:
        return 23, "CDmg"

slow = {
    "SlowDPS_Slot1.txt": {
        "filename": "./analysis/SlowDPS_Slot1.txt",
        "stat_list": ["CDmg", "CRate", "ATK%"]
    },
    "SlowDPS_Slot2.txt": {
        "filename": "./analysis/SlowDPS_Slot2.txt",
        "stat_list": ["CDmg", "CRate"]
    },
    "SlowDPS_Slot3.txt": {
        "filename": "./analysis/SlowDPS_Slot3.txt",
        "stat_list": ["CDmg", "CRate"]
    },
    "SlowDPS_Slot4.txt": {
        "filename": "./analysis/SlowDPS_Slot4.txt",
        "stat_list": ["CRate", "ATK%"]
    },
    "SlowDPS_Slot5.txt": {
        "filename": "./analysis/SlowDPS_Slot5.txt",
        "stat_list": ["CDmg", "CRate", "ATK%"]
    },
    "SlowDPS_Slot6.txt": {
        "filename": "./analysis/SlowDPS_Slot6.txt",
        "stat_list": ["CDmg", "CRate"]
    },
}

analysis_list = [
    "SlowDPS_Slot1.txt",
    "SlowDPS_Slot2.txt",
    "SlowDPS_Slot3.txt",
    "SlowDPS_Slot4.txt",
    "SlowDPS_Slot5.txt",
    "SlowDPS_Slot6.txt",
]

for analysis in analysis_list:
    slow_obj = slow[analysis]
    if not(slow_obj):
        print(f"slow obj: {slow_obj} does not exists {analysis}")
        break
    filename = slow_obj["filename"]
    stat_list = slow_obj["stat_list"]
    with open(filename, 'r') as f:
        runes = json.loads(f.read())

    count = 0
    new_list = []
    for rune in runes:
        count += 1
        max_qty = len(stat_list)
        gem_stat = check_qty(rune, stat_list, max_qty)
        if not(gem_stat) or rune.get("IsGemmed"):
            rune["NewEff"] = rune["Eff"]
            rune["Gemmed"] = "None"
            new_list.append(rune)
            continue

        new_eff, stat = get_gem_stats(gem_stat)
        rune["NewEff"] = rune["Eff"] + new_eff
        rune["Gemmed"] = stat
        new_list.append(rune)

    new_list = sorted(new_list, key=lambda x: x["NewEff"])
    new_list = new_list[-5:]
    gemmed_f = analysis.split(".")[0]

    gemmed_filename = f"./kept_runes/Gemmed_{gemmed_f}.json"
    with open(gemmed_filename, "w") as f:
        f.write(json.dumps(new_list, indent = 4))
