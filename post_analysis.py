import json
from decimal import Decimal
from dataclasses import dataclass, asdict, field

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
    ATK: int | None
    ATKI: int | None
    DEF: int | None
    DEFI: int | None
    HP: int | None
    HPI: int | None
    ACC: int | None
    ACCI: int | None
    ATKFlat: int | None
    ATKFlatI: int | None
    DEFFlat: int | None
    DEFFlatI: int | None
    HPFlat: int | None
    HPFlatI: int | None
    Set: str
    Eff: Decimal = field(compare=False)
    BEff: Decimal = field(compare=False)
    Score: int
    AdjustedScore: int

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
                ATKFlat = r.get("ATK Flat"),\
                ATKFlatI = r.get("ATK FlatI"),\
                DEFFlat = r.get("DEF Flat"),\
                DEFFlatI = r.get("DEF FlatI"),\
                HPFlat = r.get("HP Flat"),\
                HPFlatI = r.get("HP FlatI"),\
                Set = r.get("Set", ""),\
                Eff = r.get("Eff", Decimal("0.0")),\
                BEff = r.get("BEff", Decimal("0.0")),\
                Score = r.get("Score", 0),\
                AdjustedScore = r.get("AdjustedScore", 0))

name = "FastDPS_Slot6"
compare = True 
compare_name = "SlowDPS_Slot6"
rune_qty = 20

with open(f"./analysis/{name}.txt", "r") as f:
    data = json.loads(f.read())

converted_data = [convert_rune(d) for d in data]

if compare:
    with open(f"./kept_runes/{compare_name}.txt", "r") as f:
        compare_data = json.loads(f.read())
    converted_compare = [convert_rune(d) for d in compare_data]

    idx = (-1)*(rune_qty + len(converted_compare))
    new_data = converted_data[idx:]
    final_list = []
    for rune in new_data:
        if rune not in converted_compare:
            final_list.append({k: v for k, v in asdict(rune).items()\
                if v is not None})
        else:
            print(f"Rune is removed: {rune}")
    final_list = sorted(final_list, key=lambda x: x["Eff"])
else:
    final_list = data[-1*rune_qty:]

with open(f"./kept_runes/{name}.txt", "w") as f:
    f.write(json.dumps(final_list, indent=4))

print("highest: "+str(final_list[-1]["Eff"]))
print("lowest: "+str(final_list[0]["Eff"]))
