from utils import calc_adjusted_score
from utils import calc_score
from eff import calc_eff


def get_data():
    with open('rune.txt', 'r') as f:
        return f.readlines()

if __name__ == "__main__":
    print(f"Adjusted Score: {calc_adjusted_score(get_data())}")
    print(f"Score: {calc_score(get_data())}")
    print(f"Boozero Eff: {calc_eff(get_data())}")
