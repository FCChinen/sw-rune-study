import json
import os
import glob
from typing import Tuple

def get_review_file(filename: str) -> Tuple[int, int]:
    with open(filename, "r") as f:
        runes = json.loads(f.read())
    runes = sorted(runes, key=lambda x: x["NewEff"])
    return runes[0]["NewEff"], runes[-1]["NewEff"]

def create_file() -> None:
    path_pattern = os.path.join("./kept_runes/", "*.json")
    txt_files = glob.glob(path_pattern)
    final_txt = ""
    score_list = []
    for file in txt_files:
        lowest, highest = get_review_file(file)

        treated_file = file.split("/")[-1].split(".")[0]
        score_dict = {
                "Filename": treated_file,
                "Highest": highest,
                "Lowest": lowest
        }
        score_list.append(score_dict)

    score_list = sorted(score_list, key=lambda x: x["Filename"])
    for s in score_list:
        final_txt += f"""{s["Filename"]} Lowest: {s["Lowest"]} Highest: {s["Highest"]}\n"""

    with open("./review.txt", "w") as f:
        f.write(final_txt)

def main() -> None:
    create_file()

if __name__ == "__main__":
    main()
