import json
from post_analysis_dps import DecimalEncoder, Rune, custom_asdict, convert_rune
from dataclasses import fields
rune1 = {
        "CRate": 5,
        "SPD": 19,
        "ATK%": 16,
        "HP%": 15,
        "ACCI": 8,
        "MainStat": "ATK flat",
        "Gemmed": "None",
        "DPSScore": 122,
        "TankScore": 103,
        "ControlScore": 85,
        "BruiserScore": 159,
        "Set": "Guard",
        "Eff": 0,
        "BEff": 105.49,
        "NewEff": 179,
        "Score": 179,
        "AdjustedScore": 246
    }
converted_rune1 = convert_rune(rune1)
rune2 = {
        "CRate": 5,
        "SPD": 19,
        "ATK%": 16,
        "HP%": 15,
        "ACCI": 8,
        "Gemmed": "CDmg",
        "Set": "Guard",
        "Eff": 122,
        "BEff": 105.49,
        "NewEff": 145,
        "Score": 179,
        "AdjustedScore": 246
    } 
converted_rune2 = convert_rune(rune2)

def diff_dataclass(a, b):
    diffs = {}

    for f in fields(a):
        if not f.compare:
            continue  # ignora campos com compare=False
        
        v1 = getattr(a, f.name)
        v2 = getattr(b, f.name)

        if v1 != v2:
            diffs[f.name] = (v1, v2)

    return diffs

from dataclasses import fields

for f in fields(converted_rune1):
    if f.compare:
        v1 = getattr(converted_rune1, f.name)
        v2 = getattr(converted_rune2, f.name)
        if v1 != v2:
            print("f.name", f.name, "v1", v1, "v2", v2)
