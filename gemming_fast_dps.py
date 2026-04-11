from post_analysis_dps import DecimalEncoder, Rune, custom_asdict, convert_rune

from gemming_slow_dps import check_qty, get_gem_stats
import json

fast = {
        "FastDPS_Slot1.txt" : {
            "filename": "./analysis/FastDPS_Slot1.txt",
            "stat_list": ["CDmg", "CRate", "ATK%", "SPD"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot1.json"]
        },
        "FastDPS_SPD_Slot2.txt" : {
            "filename": "./analysis/FastDPS_SPD_Slot2.txt",
            "stat_list": ["CDmg", "CRate", "ATK%"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot2.json"]
        },
        "FastDPS_Slot3.txt" : {
            "filename": "./analysis/FastDPS_Slot3.txt",
            "stat_list": ["CDmg", "CRate", "SPD"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot3.json"]
        },
        "FastDPS_Slot4.txt" : {
            "filename": "./analysis/FastDPS_Slot4.txt",
            "stat_list": ["CRate", "ATK%", "SPD"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot4.json"]
        },
        "FastDPS_Slot5.txt" : {
            "filename": "./analysis/FastDPS_Slot5.txt",
            "stat_list": ["CDmg", "CRate", "ATK%", "SPD"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot5.json"]
        },
        "FastDPS_Slot6.txt" : {
            "filename": "./analysis/FastDPS_Slot6.txt",
            "stat_list": ["CDmg", "CRate", "SPD"],
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot6.json"]
        },
}

for k, v in fast.items():
    fast_obj = fast[k]
    filename = fast_obj["filename"]
    stat_list = fast_obj["stat_list"]
    rune_qty = 25
    kept_runes = []
    final_list = []
    with open(filename, "r") as f:
        runes = json.loads(f.read())
    new_list = []
    for rune in runes:
        max_qty = len(stat_list)
        gem_stat = check_qty(rune, stat_list, max_qty)
        if not(gem_stat) or rune.get("IsGemmed"):
            rune["NewEff"] = rune["Eff"]
            rune["Gemmed"] = "None"
            new_list.append(rune)
            continue
        new_eff, stat = get_gem_stats(gem_stat)
        rune["NewEff"] = rune["Eff"] + new_eff
        rune["Gemmed"] = stat
        new_list.append(rune)
    runes = sorted(new_list, key=lambda x: x["NewEff"])
    runes = [convert_rune(d) for d in runes]
    for item in fast_obj.get("compare", []):
        with open(item, "r") as f:
            data = json.loads(f.read())
        converted_data = [convert_rune(d) for d in data]
        kept_runes = kept_runes + converted_data
    for i in range(len(runes) - 1, -1, -1):
        if runes[i] not in kept_runes:
            final_list.append({k: v for k, v, in custom_asdict(runes[i]).items() if v is not None})
            if len(final_list) >= rune_qty:
                break
    gemmed_f = k.split(".")[0]
    with open(f"./kept_runes/Gemmed_{gemmed_f}.json", "w") as f:
        f.write(json.dumps(final_list, indent = 4, ensure_ascii = False, cls=DecimalEncoder))
