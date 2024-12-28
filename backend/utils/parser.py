# import json

# def parse_poker_log(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     hands = data.get("hands", [])
#     for hand in hands:
#         print(f"Hand ID: {hand['hand_id']}")
#         print(f"Players: {[player['name'] for player in hand['players']]}")
#         print(f"Winner: {hand['winner']}")


import json

def parse_poker_log(file):
    """
    Parses a poker log JSON file and extracts hand details.
    """
    # Read and decode the uploaded file content
    file_content = file.read().decode('utf-8')  # Read the file and decode it to a string
    
    try:
        # Load the JSON content
        data = json.loads(file_content)

        # Extract information about hands
        hands = []
        for hand in data.get("hands", []):
            hand_details = {
                "hand_id": hand.get("hand_id"),
                "players": [
                    {"name": player["name"], "chips": player["chips"]}
                    for player in hand.get("players", [])
                ],
                "actions": [
                    {"player": action["player"], "action": action["action"], "amount": action.get("amount")}
                    for action in hand.get("actions", [])
                ],
                "winner": hand.get("winner"),
                "pot": hand.get("pot"),
            }
            hands.append(hand_details)

        return hands
    except json.JSONDecodeError as e:
        # Handle invalid JSON format
        raise ValueError(f"Invalid JSON file: {e}")
