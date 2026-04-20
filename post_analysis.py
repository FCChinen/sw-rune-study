import json

#Want to gem slow dps
#Want to gem fast dps

def get_data(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def main():
    slot = "Slot1"
    slot1_data = get_data(f'./analysis/Everything_{slot}.json')
    for rune in slot1_data:
        print(rune)

if __name__ == "__main__":
    main()