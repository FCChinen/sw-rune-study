import json
import os

def importing_all_runes() -> list:
    with open("final_runes.json", "r") as f:
        return json.loads(f.read())

def writing_rune(runes: list) -> None:
    with open("final_runes.json", "w") as f:
        f.write(json.dumps(runes, indent=4))

def getting_rune():
    with open("rune.txt", "r") as f:
        return f.readlines()

def return_rune() -> dict:
    rune = {
            "spd": 0,
            "atk": 0,
            "def": 0,
            "hp": 0,
            "defm": 0,
            "atkm": 0,
            "hpm": 0,
            "acc": 0,
            "res": 0,
            "cdmg": 0,
            "crate": 0,
            "eff": 0
    }
    rune_stats = getting_rune()
    for stat in rune_stats:
        stat, val = stat.split(" ")
        val = int(val)
        for key in rune.keys():
            if stat == key:
                rune[stat] = val
    if rune["eff"] == 0:
        Exception("Eff cannot be zero")
    return rune

def main():
    all_runes = importing_all_runes()
    rune = return_rune()
    if rune in all_runes:
        print("rune already exists")
        os._exit(1)
    all_runes.append(return_rune())
    writing_rune(all_runes)

if __name__ == "__main__":
    main()
