import json
from decimal import Decimal
from dataclasses import dataclass, asdict, field, fields
import glob
import os

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

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
    NewEff: int = field(compare=False)
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
                Eff = r.get("Eff", 0),\
                BEff = r.get("BEff", Decimal("0.0")),\
                Score = r.get("Score", 0),\
                NewEff = r.get("NewEff", 0),\
                AdjustedScore = r.get("AdjustedScore", 0))

def main():
    slot = [1,2,3,4,5,6]
    rune_qty = 25
    rune_qty_dps = 5

    kept_runes = [[],[],[],[],[],[]]

    path_pattern = os.path.join("./analysis/", "*.txt")
    analysis_files = glob.glob(path_pattern)

    for analysis in analysis_files:
        final_list = []
        print(analysis)
        slot = analysis.split('_')[-1].split('.')[0]
        number_slot = int(slot[-1])-1
        filename = analysis.split("/")[-1]
        with open(analysis, 'r') as f:
            data = json.loads(f.read())

        converted_data = [convert_rune(d) for d in data]
        for i in range(len(converted_data) - 1, -1, -1):
            if converted_data[i] not in kept_runes[number_slot]:
                kept_runes[number_slot].append(converted_data[i])
                final_list.append({k: v for k, v, in custom_asdict(converted_data[i]).items() if v is not None})
                if len(final_list) >= rune_qty:
                    break
                if len(final_list) >= rune_qty_dps and "Slow" in analysis:
                    break

        with open(f"./kept_runes/{filename}.json", 'w') as f:
            f.write(json.dumps(final_list, indent = 4, ensure_ascii = False, cls=DecimalEncoder))

    with open(f"./kept_runes/FastDPS_SPD_Slot2.txt.json", 'r') as f:
        data = json.loads(f.read())
    with open(f"./kept_runes/FastDPS_SPD_Slot2.txt.json", 'w') as f:
        f.write(json.dumps(data[:10], indent = 4))

if __name__ == "__main__":
    main()
