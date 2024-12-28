import json

def parse_poker_log(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    hands = data.get("hands", [])
    for hand in hands:
        print(f"Hand ID: {hand['hand_id']}")
        print(f"Players: {[player['name'] for player in hand['players']]}")
        print(f"Winner: {hand['winner']}")
