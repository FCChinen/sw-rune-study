def get_data():
    with open('rune.txt', 'r') as f:
        return f.readlines()

def calc_eff(data: list):
    eff = float(0)
    grindCount = 0
    critCount = 0
    for line in data:
        stat, val = line.split(" ")
        float_val = float(val)
        stat_val = 0
        if "spd" == stat:
            stat_val = (float_val+5.0)*1.66
            grindCount+=1
        elif "spdi" == stat:
            stat_val = float_val*1.66
        elif "cd" == stat or "cdi" == stat:
            stat_val = float_val+float_val/7
            critCount += 1
        elif "res" == stat or "resi" == stat:
            stat_val = float_val
        elif "acc" == stat or "acci"== stat:
            stat_val = float_val
        elif "cr" == stat or "cri" == stat:
            stat_val = float_val*1.33
            critCount += 1
        elif "hp" == stat or "atk" == stat or "def" == stat:
            stat_val = 10.0 + float_val
            grindCount+=1
        elif "hpi" == stat or "atki" == stat or "defi" == stat:
            stat_val = float_val
            grindCount+=1
        elif "hpm" == stat:
            stat_val = (float_val+550)/100
        elif "hpmi" == stat:
            stat_val = (float_val)/100
        elif "atkm" == stat:
            stat_val = (float_val+30)/10
        elif "atkmi" == stat:
            stat_val = (float_val)/10
        elif "defmi" == stat:
            stat_val = (float_val)/10
        elif "defm" == stat:
            stat_val = (float_val+30)/10
        else:
            print(f"stat {stat} not found")
        eff += stat_val
        
        # print(f"{stat}: {int(float_val)} {stat_val}")
    if grindCount == 4:
        eff -= 10.0
        # print("-10")
    if critCount == 2:
        eff += 10.0
        # print("bonus crit: +10")
    return eff

if __name__ == "__main__":
    print(f"Eff: {calc_eff(get_data())}")
