import main


def find_player_matches(file_path, player_id):
    matches = {}
    current_week = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('Week '):
                current_week = "Division " + str(main.division) + " - " + line
            else:
                parts = line.split(', ')
                match_id, player1, player2 = parts[0], parts[1], parts[2]

                if player1 == player_id or player2 == player_id:
                    other_player = player2 if player1 == player_id else player1
                    if current_week:
                        matches.setdefault("tournaments", []).append({
                            'id': match_id,
                            'vs': other_player,
                        })
                        print(matches)

    return matches


find_player_matches("schedule.txt", "Player1")
