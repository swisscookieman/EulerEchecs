def schedule_gen(players):
    num_players = len(players)
    num_weeks = num_players - 1

    matches_per_week = num_players // 2

    schedule = []

    for week in range(1, num_weeks + 1):
        week_schedule = []
        for match_num in range(1, matches_per_week + 1):
            player1 = players[match_num - 1]
            player2 = players[-match_num]
            match_id = f'd1w{week}m{match_num}'
            match_info = f'{match_id}, {player1}, {player2}'
            week_schedule.append(match_info)
        schedule.append(week_schedule)

        # Rotate
        players = [players[0]] + players[-1:] + players[1:-1]

    return schedule


def schedule_write(schedule, filename):
    with open(filename, 'w') as file:
        for week, week_schedule in enumerate(schedule, start=1):
            file.write(f'Week {week}\n')
            for match_info in week_schedule:
                file.write(match_info + '\n')
            file.write('\n')


def MG(playerlist):
    schedule = schedule_gen(playerlist)
    schedule_write(schedule, 'schedule.txt')
