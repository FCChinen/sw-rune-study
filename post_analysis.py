import json
from decimal import Decimal
from dataclasses import dataclass, asdict, field, fields
import glob
import os

@dataclass
class Rune:
    CRate: int | None
    CRateI: int | None
    CDmg: int | None
    CDmgI: int | None
    SPD: int | None
    SPDI: int | None 
    RES: int | None
    RESI: int| None  
    ATK: int | None = field(metadata={"json": "ATK%"})
    ATKI: int | None = field(metadata={"json": "ATK%I"})
    DEF: int | None = field(metadata={"json": "DEF%"})
    DEFI: int | None = field(metadata={"json": "DEF%I"})
    HP: int | None = field(metadata={"json": "HP%"})
    HPI: int | None = field(metadata={"json": "HP%I"})
    ACC: int | None
    ACCI: int | None
    ATKFlat: int | None = field(metadata={"json": "ATK flat"})
    ATKFlatI: int | None = field(metadata={"json": "ATK flatI"})
    DEFFlat: int | None = field(metadata={"json": "DEF flat"})
    DEFFlatI: int | None = field(metadata={"json": "DEF flatI"})
    HPFlat: int | None = field(metadata={"json": "HP flat"})
    HPFlatI: int | None = field(metadata={"json": "HP flatI"})
    Set: str
    Eff: Decimal = field(compare=False)
    BEff: Decimal = field(compare=False)
    Score: int = field(compare=False)
    AdjustedScore: int = field(compare=False)

def custom_asdict(obj):
    result = {}
    for f in fields(obj):
        val = getattr(obj, f.name)
        # Pega o nome customizado se existir, senão usa o nome da variável
        key = f.metadata.get("json", f.name)
        if hasattr(val, "__dataclass_fields__"):
            result[key] = custom_asdict(val)
        else:
            result[key] = val
    return result

def convert_rune(r: dict) -> Rune:
    return Rune(CRate = r.get("CRate"),\
                CRateI = r.get("CRateI"),\
                CDmg = r.get("CDmg"),\
                CDmgI = r.get("CDmgI"),\
                SPD = r.get("SPD"),\
                SPDI = r.get("SPDI"),\
                RES = r.get("RES"),\
                RESI = r.get("RESI"),\
                ATK = r.get("ATK%"),\
                ATKI = r.get("ATK%I"),\
                DEF = r.get("DEF%"),\
                DEFI = r.get("DEF%I"),\
                HP = r.get("HP%"),\
                HPI = r.get("HP%I"),\
                ACC = r.get("ACC"),\
                ACCI = r.get("ACCI"),\
                ATKFlat = r.get("ATK flat"),\
                ATKFlatI = r.get("ATK flatI"),\
                DEFFlat = r.get("DEF flat"),\
                DEFFlatI = r.get("DEF flatI"),\
                HPFlat = r.get("HP flat"),\
                HPFlatI = r.get("HP flatI"),\
                Set = r.get("Set", ""),\
                Eff = r.get("Eff", Decimal("0.0")),\
                BEff = r.get("BEff", Decimal("0.0")),\
                Score = r.get("Score", 0),\
                AdjustedScore = r.get("AdjustedScore", 0))

slot = "Slot2"
name = f"TankSup_HP_{slot}"
rune_qty = 10

with open(f"./analysis/{name}.txt", "r") as f:
    data = json.loads(f.read())

converted_data = [convert_rune(d) for d in data]

path_pattern = os.path.join("./kept_runes/", "*.txt")
txt_files = glob.glob(path_pattern)
txt_files = [t for t in txt_files if name not in t]
if txt_files:
    full_compare_list = []
    for compare_name in txt_files:
        if slot not in compare_name:
            continue
        print(compare_name)
        with open(compare_name, "r") as f:
            compare_data = json.loads(f.read())
        c_converted_compare = [convert_rune(d) for d in compare_data]
        for c in c_converted_compare:
            full_compare_list.append(c)

    idx = (-1)*(rune_qty + len(full_compare_list))
    new_data = converted_data[idx:]
    final_list = []
    for rune in new_data:
        if rune not in full_compare_list:
            final_list.append({k: v for k, v in custom_asdict(rune).items()\
                if v is not None})
        else:
            print(f"Rune is removed: {rune}")
    final_list = sorted(final_list, key=lambda x: x["Eff"])
    final_list = final_list[-1*rune_qty:]
else:
    final_list = data[-1*rune_qty:]

with open(f"./kept_runes/{name}.txt", "w") as f:
    f.write(json.dumps(final_list, indent=4, ensure_ascii=False))

print("highest: "+str(final_list[-1]["Eff"]))
print("lowest: "+str(final_list[0]["Eff"]))
