import json


def check_qty(rune: dict, stat_list: list):
    qty = 0
    has = []
    for stat in stat_list:
        exist = rune.get(stat) or rune.get(stat+"I")
        if exist:
            qty += 1
            has.append(stat)

    if qty <= 2:
        return [rune for rune in stat_list if rune not in has]
    return []

filename = "./analysis/SlowDPS_Slot1.txt"

with open(filename, 'r') as f:
    runes = json.loads(f.read())

count = 0
stat_list = ["CDmg", "CRate", "ATK%"]
new_list = []
for rune in runes:
    count += 1
    gem_stat = check_qty(rune, stat_list)
    if not(gem_stat):
        continue
    if "ATK%" in gem_stat:
        rune["NewEff"] = rune["Eff"] + 28
        rune["Gemmed"] = "ATK%"
    elif "CRate" in gem_stat:
        rune["NewEff"] = rune["Eff"] + 24
        rune["Gemmed"] = "CRate"
    elif "CDmg" in gem_stat:
        rune["NewEff"] = rune["Eff"] + 23
        rune["Gemmed"] = "CDmg"
    new_list.append(rune)

new_list = sorted(new_list, key=lambda x: x["NewEff"])

gemmed_filename = "./kept_runes/Gemmed_SlowDPS_Slot1.json"
with open(gemmed_filename, "w") as f:
    f.write(json.dumps(new_list, indent = 4))
