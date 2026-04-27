import json
import collections

with open("./kept_runes/Everything_Slot1.json", "r") as f:
    runes = json.loads(f.read())
spd_runes = [s for s in runes if "SPD" in s.keys() and "Swift" == s.get("Set")]
s = {}
for rune in spd_runes:
    s[int(rune["SPD"])] = s.get(int(rune["SPD"]), 1) + 1
od = collections.OrderedDict(sorted(s.items()))
print(od)