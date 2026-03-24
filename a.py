import json

with open("./kept_runes/FastDPS_Slot2.txt") as f:
    data = json.loads(f.read())

print(data[-1]["Eff"])
print(data[-2]["Eff"])
print(data[0]["Eff"])
print(data[1]["Eff"])
