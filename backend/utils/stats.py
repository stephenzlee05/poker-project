import json

def calculate_player_stats(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    hands = data["hands"]
    player_stats = {}


    """
    payload types:
    0: check
    2: post bb
    3: post sb
    6: post straddle
    7: call
    8: raise    
    9: show flop/turn/river
    10: win pot
    11: fold
    12: show cards
    14: run it twice?
    15: hand finished
    16: uncalled bet is returned
    """

    """
    TODO
    PFR: preflop raise
    AF: agression factor (bets + raises)/calls
    3bet %
    showdown %
    bb won /100 hands
    """

    for hand in hands:
        players = {player["seat"]: player["id"] for player in hand["players"]}
        events = hand["events"]
        pot_winners = set()
        vpip_players = set()
        limpers = set()
        pfr_players = set()
        three_bet_players = set()
        aggression_actions = {seat: {"bets_raises": 0, "calls": 0} for seat in players.keys()}
        isPreflop = True
        isRaised = False


        # Track actions in the current hand
        for event in events:
            payload = event["payload"]

            if payload["type"] == 9:
                isPreflop = False

            #preflop stats
            if isPreflop:
                if payload["type"] == 7:  # Call
                    vpip_players.add(payload["seat"])
                    if (payload["value"] == hand["bigBlind"] or  # If the player just called the BB pre-flop
                        hand["straddleSeat"] and payload["value"] == 2 * hand["bigBlind"]):  # If the player just called the straddle pre-flop
                        limpers.add(payload["seat"])

                elif payload["type"] == 8:  # preflop raise
                    vpip_players.add(payload["seat"])
                    pfr_players.add(payload["seat"])

                    if isRaised:
                        three_bet_players.add(payload["seat"])
                    isRaised = True

            #postflop stats
            if not isPreflop:
                if payload["type"] == 8:  # Raise
                    aggression_actions[payload["seat"]]["bets_raises"] += 1
                elif payload["type"] == 7:  # Call
                    aggression_actions[payload["seat"]]["calls"] += 1


            if payload["type"] == 10:  # Pot won
                pot_winners.add(payload["seat"])

        # Update stats for each player in the hand
        for seat, player_id in players.items():
            if player_id not in player_stats:
                player_stats[player_id] = {
                    "name": next(player["name"] for player in hand["players"] if player["id"] == player_id),
                    "hands_played": 0,
                    "vpip_count": 0,
                    "limp_count": 0,
                    "pfr_count": 0,
                    "three_bet_count": 0,
                    "bets_raises": 0,
                    "calls": 0,
                    "pots_won": 0,
                }
            player_stats[player_id]["hands_played"] += 1
            if seat in vpip_players:
                player_stats[player_id]["vpip_count"] += 1
            if seat in limpers:
                player_stats[player_id]["limp_count"] += 1
            if seat in pot_winners:
                player_stats[player_id]["pots_won"] += 1
            if seat in pfr_players:
                player_stats[player_id]["pfr_count"] += 1
            if seat in three_bet_players:
                player_stats[player_id]["three_bet_count"] += 1
            player_stats[player_id]["bets_raises"] += aggression_actions[seat]["bets_raises"]
            player_stats[player_id]["calls"] += aggression_actions[seat]["calls"]

    # Calculate percentages
    for stats in player_stats.values():
        stats["vpip_percentage"] = (stats["vpip_count"] / stats["hands_played"]) * 100
        stats["limp_percentage"] = (stats["limp_count"] / stats["hands_played"]) * 100
        stats["pfr_precentage"] = (stats["pfr_count"] / stats["hands_played"]) * 100
        stats["three_bet_percentage"] = (stats["three_bet_count"] / stats["hands_played"]) * 100
        stats["aggression_factor"] = (stats["bets_raises"] / stats["calls"]
                                        if stats["calls"] > 0 else float('inf'))  # Avoid division by zero


    return player_stats


# Example Usage
#file_path = r"C:\Users\steph\OneDrive\Desktop\data\poker-now-hands-game-pglT6LMW0tP4tv_bBO9wwmIet.json"  # Replace with your JSON file path
file_path = r"C:\Users\steph\Downloads\poker-now-hands-game-pglaiAy4PX1Yv7lat4HKJlNCB.json"
stats = calculate_player_stats(file_path)

# Display stats
for player_id, player_stat in stats.items():
    print(f"Player: {player_stat['name']} (ID: {player_id})")
    print(f"  Hands Played: {player_stat['hands_played']}")
    print(f"  VPIP: {player_stat['vpip_percentage']:.2f}%")
    print(f"  Limp Percentage: {player_stat['limp_percentage']:.2f}%")
    print(f"  PFR Percentage: {player_stat['pfr_precentage']:.2f}%")
    print(f"  3bet Percentage: {player_stat['three_bet_percentage']:.2f}%")
    print(f"  Aggression Factor (AF): {player_stat['aggression_factor']:.2f}")
    print(f"  Pots Won: {player_stat['pots_won']}")
    print()
