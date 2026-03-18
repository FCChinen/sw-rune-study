def checking_stats(row: dict, stat: str) -> int:
    if row["i_t"] == stat and int(row["i_v"]) > 0:
        return int(row["i_v"])
    idx_list = [1,2,3,4]
    for idx in idx_list:
        if row["s"+str(idx)+"_t"] == stat:
            return int(row["s"+str(idx)+"_v"])
    return 0


def get_rune(row: dict, eff: float = 0.0, boozero_eff: float = 0.0) -> dict:
    idx_list = [1,2,3,4]
    custom_order = ["CRate", "CDmg", "ATK%", "SPD", \
                    "DEF%", "HP%", "ATK flat", "DEF flat", \
                    "HP flat", "RES", "ACC", "Eff", "BEff"]
    rune = dict()
    for idx in idx_list:
        rune[row["s"+str(idx)+"_t"]] = row["s"+str(idx)+"_v"]
    if int(row["i_v"]) > 0:
        rune[row["i_t"]] = int(row["i_v"])
    if eff:
        rune["Eff"] = eff
    if boozero_eff:
        rune["BEff"] = boozero_eff
    return {key: rune[key] for key in custom_order if key in rune}


def check_eff(row: dict, stat_list: list = []) -> tuple:
    if not(stat_list):
        stat_list = ["CRate", "CDmg", "ATK", "SPD", \
                    "DEF%", "HP%", "ATK flat", "DEF flat", \
                    "HP flat", "RES", "ACC"]
    val_dict = dict()
    eff = 0.0
    stat_eff = 0.0
    count = 0
    for stat in stat_list:
        val = checking_stats(row, stat)
        if val > 0:
            count += 1
            if stat == "ATK%":
                stat_eff = val/8
                eff += stat_eff
            elif stat == "CRate":
                stat_eff = val/6
                eff += stat_eff
            elif stat == "CDmg":
                stat_eff = val/7
                eff += stat_eff
            val_dict[stat] = {
                stat: val,
                "eff": stat_eff
            }
    return eff, count
