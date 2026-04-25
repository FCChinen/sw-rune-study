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

def get_gem_list(runes: list, stat_list: list, rune_type: str) -> list:
    count = 0
    new_list = []
    for rune in runes:
        count += 1
        max_qty = len(stat_list)
        gem_stat = check_qty(rune, stat_list, max_qty)
        if not(gem_stat) or rune.get("IsGemmed"):
            rune[rune_type] = rune[rune_type]
            rune["Gemmed"] = "None"
            new_list.append(rune)
            continue

        new_eff, stat = get_gem_stats(gem_stat)
        rune[rune_type] = rune[rune_type] + new_eff
        rune["Gemmed"] = stat
        new_list.append(rune)
    return new_list

slow = {
    "DPS_Slot1.json": {
        "filename": "./analysis/Everything_Slot1.json",
        "stat_list": ["CDmg", "CRate", "ATK%"]
    },
    "DPS_Slot2.json": {
        "filename": "./analysis/Everything_Slot2.json",
        "stat_list": ["CDmg", "CRate"],
        "main_stat": "ATK%"
    },
    "DPS_Slot3.json": {
        "filename": "./analysis/Everything_Slot3.json",
        "stat_list": ["CDmg", "CRate"]
    },
    "DPS_Slot4.json": {
        "filename": "./analysis/Everything_Slot4.json",
        "stat_list": ["CRate", "ATK%"],
        "main_stat": "CDmg"
    },
    "DPS_Slot5.json": {
        "filename": "./analysis/Everything_Slot5.json",
        "stat_list": ["CDmg", "CRate", "ATK%"]
    },
    "DPS_Slot6.json": {
        "filename": "./analysis/Everything_Slot6.json",
        "stat_list": ["CDmg", "CRate"],
        "main_stat": "ATK%"
    },
}

fast = {
        "DPS_Slot1.json" : {
            "stat_list": ["CDmg", "CRate", "ATK%", "SPD"]
        },
        "DPS_Slot2.json" : {
            "stat_list": ["CDmg", "CRate", "ATK%"],
            "main_stat": "SPD"
        },
        "DPS_Slot3.json" : {
            "stat_list": ["CDmg", "CRate", "SPD"]
        },
        "DPS_Slot4.json" : {
            "stat_list": ["CRate", "ATK%", "SPD"],
            "main_stat": "CDmg"
        },
        "DPS_Slot5.json" : {
            "stat_list": ["CDmg", "CRate", "ATK%", "SPD"],
        },
        "DPS_Slot6.json" : {
            "stat_list": ["CDmg", "CRate", "SPD"],
            "main_stat": "ATK%"
        },
}

analysis_list = [
    "DPS_Slot1.json",
    "DPS_Slot2.json",
    "DPS_Slot3.json",
    "DPS_Slot4.json",
    "DPS_Slot5.json",
    "DPS_Slot6.json",
]

review = {}
review2 = {}
for analysis in analysis_list:
    slow_obj = slow[analysis] 
    if not(slow_obj):
        print(f"slow obj: {slow_obj} does not exists {analysis}")
        break
    filename = slow_obj["filename"]
    stat_list = slow_obj["stat_list"]
    with open(filename, 'r') as f:
        runes = json.loads(f.read())
    
    if slow_obj.get("main_stat"):
        main_stat = slow_obj["main_stat"]
        new_list = [rune for rune in runes if rune.get("MainStat") == main_stat]
    else:
        new_list = runes
    new_list = get_gem_list(new_list, stat_list, "SlowDPSSCore")
    new_list = sorted(new_list, key=lambda x: x["SlowDPSSCore"],reverse=True)
    filtered_list = new_list[:5]
    unique_id_list = []
    for r in filtered_list:
        unique_id_list.append(r["UniqueId"])
    gemmed_f = f"""Gemmed_Slow{analysis.split(".")[0]}"""
    review[gemmed_f] = {
        "highest": filtered_list[0]["SlowDPSSCore"],
        "lowest": filtered_list[-1]["SlowDPSSCore"]
    }
    review2[analysis.split(".")[0]] = {
        "SlowDPSSCore": filtered_list[-1]["SlowDPSSCore"]
    }
    gemmed_filename = f"./kept_runes/{gemmed_f}.json"
    with open(gemmed_filename, "w") as f:
        f.write(json.dumps(filtered_list, indent = 4))
    runes = [rune for rune in runes if rune["UniqueId"] not in unique_id_list]

    fast_obj = fast[analysis]
    if not(fast_obj):
        print(f"fast_obj: {fast_obj} does not exists {analysis}")
        break
    #filename = fast_obj["filename"]
    stat_list = fast_obj["stat_list"]
    if fast_obj.get("main_stat"):
        main_stat = slow_obj["main_stat"]
        new_list = [rune for rune in runes if rune.get("MainStat") == main_stat]
    else:
        new_list = runes
    new_list = get_gem_list(new_list, stat_list, "DPSScore")
    new_list = sorted(new_list, key=lambda x: x["DPSScore"],reverse=True)
    filtered_list = new_list[:25]
    for r in filtered_list:
        unique_id_list.append(r["UniqueId"])
    gemmed_f = f"""Gemmed_Fast{analysis.split(".")[0]}"""
    review[gemmed_f] = {
        "highest": filtered_list[0]["DPSScore"],
        "lowest": filtered_list[-1]["DPSScore"]
    }
    review2[analysis.split(".")[0]]["DPSScore"] = filtered_list[-1]["DPSScore"]
    gemmed_filename = f"./kept_runes/{gemmed_f}.json"
    with open(gemmed_filename, "w") as f:
        f.write(json.dumps(filtered_list, indent = 4))
    everything_list = sorted(runes, key=lambda x: x["BEff"],reverse=True)
    print(f"{everything_list[-1]}")
    gemmed_f = f"""Everything_{analysis.split("_")[1].split(".")[0]}"""
    review[gemmed_f] = {
        "highest": everything_list[0]["BEff"],
        "lowest": everything_list[-1]["BEff"]
    }
    review2[analysis.split(".")[0]]["BEff"] = everything_list[-1]["BEff"]
    gemmed_filename = f"./kept_runes/{gemmed_f}.json"
    with open(gemmed_filename, "w") as f:
        f.write(json.dumps(everything_list, indent = 4))

with open("./kept_runes/Review.json", "w") as f:
    f.write(json.dumps(review, indent = 4)) 

with open("./kept_runes/Review2.json", "w") as f:
    f.write(json.dumps(review2, indent = 4)) 