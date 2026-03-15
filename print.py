import csv
import json

def analyze():
    with open("runes-data.csv", "r") as f:
        reader = csv.DictReader(f, delimiter = ";")
        for row in reader:
            print(row["s1_data"])
            print(json.dumps(row, indent=4) )
            break

def main():
    analyze()

if __name__ == "__main__":
    main()
