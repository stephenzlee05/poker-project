def calculate_vpip(actions, player_name):
    total_hands = len(actions)
    vpip_hands = sum(1 for action in actions if action['player'] == player_name and action['action'] in ['call', 'raise'])
    return vpip_hands / total_hands * 100
