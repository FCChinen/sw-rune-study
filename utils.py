from decimal import Decimal

def checking_stats(row: dict, stat: str) -> int:
    if row["i_t"] == stat and int(row["i_v"]) > 0:
        return int(row["i_v"])
    idx_list = [1,2,3,4]
    for idx in idx_list:
        if row["s"+str(idx)+"_t"] == stat:
            return int(row["s"+str(idx)+"_v"])
    return 0


def get_rune(row: dict, eff: float = 0.0, boozero_eff: float = 0.0,\
             score: int = 0, adjusted_score: int = 0) -> dict:
    idx_list = [1,2,3,4]
    custom_order = ["CRate","CRateI", "CDmg", "CDmgI", "ATK%", "ATK%I", "SPD", "SPDI" \
                    "DEF%", "DEF%I", "HP%", "HP%I", "ATK flat", "ATK flatI", "DEF flat", "DEF flatI",\
                    "HP flat", "HP flatI", "RES", "RESI", "ACC", "ACCI", "Set", \
                    "Eff", "BEff", "Score", "AdjustedScore"]
    rune = dict()
    for idx in idx_list:
        rune[row["s"+str(idx)+"_t"]] = int(row["s"+str(idx)+"_v"])
    if int(row["i_v"]) > 0:
        rune[row["i_t"]+"I"] = int(row["i_v"])
    if eff:
        rune["Eff"] = eff
    if boozero_eff:
        rune["BEff"] = boozero_eff
    if score:
        rune["Score"] = score
    if row["set"]:
        rune["Set"] = row["set"]
    if adjusted_score:
        rune["AdjustedScore"] = adjusted_score
    return {key: rune[key] for key in custom_order if key in rune}

def calc_score(data: list):
    eff = Decimal("0")
    for line in data:
        stat, val = line.split(" ")
        float_val = Decimal(val)
        stat_val = 0
        if "spd" in stat:
            stat_val = float_val * Decimal("3.4")
        elif "cr" in stat:
            stat_val = float_val * Decimal("3.3")
        elif "cd" in stat:
            stat_val = float_val * Decimal("2.8")
        elif stat in ["hp", "hpi", "def", "defi", "atk", "atki", \
                      "acc", "acci", "res", "resi"]:
            stat_val = float_val * Decimal("2.5")
        elif stat in ["hpm", "hpmi"]:
            stat_val = float_val * Decimal("0.02")
        elif stat in ["atkm", "atkmi"]:
            stat_val = float_val * Decimal("0.33")
        elif stat in ["defm", "defmi"]:
            stat_val = float_val * Decimal("0.2")
        eff += stat_val
    return round(eff)

def calc_adjusted_score(data: list):
    eff = Decimal("0")
    grindCount = 0
    critCount = 0
    for line in data:
        stat, val = line.split(" ")
        float_val = Decimal(val)
        stat_val = 0
        if "spd" in stat:
            stat_val = float_val * Decimal("3.4")
            if stat != "spdi":
                stat_val += Decimal("5.0") * Decimal("3.4")
                grindCount += 1
        elif "cr" in stat:
            stat_val = float_val * Decimal("3.3")
            critCount += 1
        elif "cd" in stat:
            stat_val = float_val * Decimal("2.8")
            critCount += 1
        elif stat in ["hp", "hpi", "def", "defi", "atk", "atki", \
                      "acc", "acci", "res", "resi"]:
            stat_val = float_val * Decimal("2.5")
            if stat in ["hp", "def", "atk"]:
                stat_val += Decimal("25.0")
                grindCount += 1
        elif stat in ["hpm", "hpmi"]:
            stat_val = float_val * Decimal("0.02")
        elif stat in ["atkm", "atkmi"]:
            stat_val = float_val * Decimal("0.33")
        elif stat in ["defm", "defmi"]:
            stat_val = float_val * Decimal("0.2")
        eff += stat_val
    if grindCount == 4:
        eff -= Decimal("25.0")
    if grindCount == 2:
        eff += Decimal("20.0")

    return round(eff)

def has_stats(row: dict, stat_list: list = []) -> int:
    if not(stat_list):
        # Get all stats
        stat_list = ["CRate", "CDmg", "ATK", "SPD", \
                    "DEF%", "HP%", "ATK flat", "DEF flat", \
                    "HP flat", "RES", "ACC"]
    count = 0
    for stat in stat_list:
        val = checking_stats(row, stat)
        if val > 0:
            count += 1
    return count
