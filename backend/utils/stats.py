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
    4: post missing bb
    5: post missing sb
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
        player_profit = {player["id"]: 0 for player in hand["players"]}
        new_pip = {}
        events = hand["events"]
        pot_winners = {}
        vpip_players = set()
        limpers = set()
        pfr_players = set()
        three_bet_players = set()
        missing_sb_players = set()
        aggression_actions = {seat: {"bets_raises": 0, "calls": 0} for seat in players.keys()}
        isPreflop = True
        isRaised = False


        # Track actions in the current hand
        for event in events:
            payload = event["payload"]

            if payload["type"] == 3: # Post SB
                if payload["seat"] not in new_pip:
                    new_pip[payload["seat"]] = set()
                new_pip[payload["seat"]].add(hand["smallBlind"])
            elif payload["type"] == 5:  # missing sb
                player_profit[players[payload["seat"]]] -= hand["smallBlind"]
            elif payload["type"] == 2 or payload["type"] == 4: # Post BB
                if payload["seat"] not in new_pip:
                    new_pip[payload["seat"]] = set()
                new_pip[payload["seat"]].add(hand["bigBlind"])
            elif payload["type"] == 6:  # Post Straddle
                if payload["seat"] not in new_pip:
                    new_pip[payload["seat"]] = set()
                new_pip[payload["seat"]].add(2 * hand["bigBlind"])
            elif payload["type"] == 7 or payload["type"] == 8:  # call or raise
                if payload["seat"] not in new_pip:
                    new_pip[payload["seat"]] = set()
                new_pip[payload["seat"]].add(payload["value"])

            elif payload["type"] == 16:
                player_profit[players[payload["seat"]]] += payload["value"]
            elif payload["type"] == 15 or payload["type"] == 9:
                for seat, values in new_pip.items():
                    player_profit[players[seat]] -= max(values)
                new_pip = {}

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

            if payload["type"] == 5:
                missing_sb_players.add(payload["seat"])

            if payload["type"] == 10:  # Pot won
                if payload["seat"] in pot_winners:
                    pot_winners[payload["seat"]] += payload["value"]
                else:
                    pot_winners[payload["seat"]] = payload["value"]

        for id, value in pot_winners.items():
            player_profit[players[id]] += value

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
                    "starting_stack": next(player["stack"] for player in hand["players"] if player["id"] == player_id),
                    "ending_stack": 0,
                    "profit": 0
                }
                if seat in missing_sb_players:
                    player_stats[player_id]["starting_stack"] += hand["smallBlind"]
                
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
            player_stats[player_id]["profit"] += player_profit[player_id]

    # Calculate percentages
    for stats in player_stats.values():
        stats["vpip_percentage"] = (stats["vpip_count"] / stats["hands_played"]) * 100
        stats["limp_percentage"] = (stats["limp_count"] / stats["hands_played"]) * 100
        stats["pfr_precentage"] = (stats["pfr_count"] / stats["hands_played"]) * 100
        stats["three_bet_percentage"] = (stats["three_bet_count"] / stats["hands_played"]) * 100
        stats["aggression_factor"] = (stats["bets_raises"] / stats["calls"]
                                        if stats["calls"] > 0 else stats["bets_raises"])  # Avoid division by zero


    return player_stats


# Example Usage
file_path = r"C:\Users\steph\Downloads\poker-now-hands-game-pgl6IdynqXEVNY1_A-pSoE-hC.json"  # Replace with your JSON file path
#file_path = r"C:\Users\steph\OneDrive\Desktop\poker project\uploads\poker-now-hands-game-pglNagPktmUfnbRbsz_YLXAcc.json"
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
    print(f"  Profit: {player_stat['profit']}")
    print()
