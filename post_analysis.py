import json

with open("95.txt", "r") as f:
    data = json.loads(f.read())

with open("84_95.txt", "r") as f:
    data2 = json.loads(f.read())

count = 0
for rune in data:
    if rune.get("SPD", 0) > 12:
        count += 1

print(count)
print("total: "+str(len(data)))

count = 0
sorted_data = sorted(data2, key=lambda item: item['BEff'])
for rune in data2:
    if rune.get("SPD", 0) > 12:
        count += 1

print(count)
print("total: "+str(len(data2)))
