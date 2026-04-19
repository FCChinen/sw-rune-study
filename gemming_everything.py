from post_analysis_dps import DecimalEncoder, Rune, custom_asdict, convert_rune

import json

fast = {
        "Everything_Slot1.txt" : {
            "filename": "./analysis/Everything_Slot1.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot1.json",
                        "./kept_runes/Gemmed_FastDPS_Slot1.json"]
        },
        "Everything_Slot2.txt" : {
            "filename": "./analysis/Everything_Slot2.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot2.json",
                        "./kept_runes/Gemmed_FastDPS_SPD_Slot2.json"]
        },
        "Everything_Slot3.txt" : {
            "filename": "./analysis/Everything_Slot3.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot3.json",
                        "./kept_runes/Gemmed_FastDPS_Slot3.json"]
        },
        "Everything_Slot4.txt" : {
            "filename": "./analysis/Everything_Slot4.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot4.json",
                        "./kept_runes/Gemmed_FastDPS_Slot4.json"]
        },
        "Everything_Slot5.txt" : {
            "filename": "./analysis/Everything_Slot5.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot5.json",
                        "./kept_runes/Gemmed_FastDPS_Slot5.json"]
        },
        "Everything_Slot6.txt" : {
            "filename": "./analysis/Everything_Slot6.txt",
            "compare": ["./kept_runes/Gemmed_SlowDPS_Slot6.json",
                        "./kept_runes/Gemmed_FastDPS_Slot6.json"]
        },
}

for k, v in fast.items():
    fast_obj = fast[k]
    filename = fast_obj["filename"]
    rune_qty = 75
    kept_runes = []
    final_list = []
    with open(filename, "r") as f:
        runes = json.loads(f.read())
    new_list = []
    for rune in runes:
        if rune["MainStat"] == "SPD":
            rune["NewEff"] = rune["AdjustedScore"] + 25
        else:
            rune["NewEff"] = rune["AdjustedScore"]
        rune["Gemmed"] = "None"
    runes = sorted(runes, key=lambda x: x["NewEff"])
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
    with open(f"./kept_runes/{gemmed_f}.json", "w") as f:
        f.write(json.dumps(final_list, indent = 4, ensure_ascii = False, cls=DecimalEncoder))
