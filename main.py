import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import MatchGen
from datetime import datetime


division = 1

# firebase shite
cred = credentials.Certificate(
    "echecseuler-firebase-adminsdk-25xs4-89c7756f0f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# main code - opens the players
with open('div1players.txt') as f:
    playerlist = f.readlines()
    playerlist = [s.strip('\n') for s in playerlist]


week1start = datetime(2024, 1, 10, 12, 0)
week1end = datetime(2024, 1, 17, 23, 59)

week2start = datetime(2024, 1, 17, 12, 0)
week2end = datetime(2024, 1, 24, 23, 59)

week3start = datetime(2024, 1, 24, 12, 0)
week3end = datetime(2024, 1, 31, 23, 59)

week4start = datetime(2024, 1, 31, 12, 0)
week4end = datetime(2024, 2, 7, 23, 59)

week5start = datetime(2024, 2, 7, 12, 0)
week5end = datetime(2024, 2, 14, 23, 59)

week6start = datetime(2024, 2, 14, 12, 0)
week6end = datetime(2024, 2, 21, 23, 59)

week6start = datetime(2024, 2, 21, 12, 0)
week6end = datetime(2024, 2, 28, 23, 59)

week6start = datetime(2024, 2, 28, 12, 0)
week6end = datetime(2024, 3, 6, 23, 59)

week7start = datetime(2024, 3, 6, 12, 0)
week7end = datetime(2024, 3, 13, 23, 59)

week8start = datetime(2024, 3, 13, 12, 0)
week8end = datetime(2024, 3, 20, 23, 59)

week9start = datetime(2024, 3, 20, 12, 0)
week9end = datetime(2024, 3, 27, 23, 59)


def PlayerPrep(playerlist):

    if division == 1:
        info = "Match en BO2 avec format 10|5"
    elif division == 2 or division == 3:
        info = "Match en BO1 avec format 10|5"
    for player in playerlist:
        doc_ref = db.collection("users_s2").document(str(player))
        thelist = [{"when": week1start, "end": week1end, "name": "Division "+str(division)+" - Semaine 1", "info": info}, {"when": week2start, "end": week2end, "name": "Division "+str(division)+" - Semaine 2", "info": info}, {"when": week3start, "end": week3end, "name": "Division "+str(division)+" - Semaine 3", "info": info}, {"when": week4start, "end": week4end, "name": "Division "+str(division)+" - Semaine 4", "info": info}, {"when": week5start, "end": week5end, "name": "Division "+str(
            division)+" - Semaine 5", "info": info}, {"when": week6start, "end": week6end, "name": "Division "+str(division)+" - Semaine 6", "info": info}, {"when": week7start, "end": week7end, "name": "Division "+str(division)+" - Semaine 7", "info": info}, {"when": week8start, "end": week8end, "name": "Division "+str(division)+" - Semaine 8", "info": info}, {"when": week9start, "end": week9end, "name": "Division "+str(division)+" - Semaine 9", "info": info}]
        print("Prepping player account of " + str(player) + "...")
        newlist = merge_lists(find_player_matches(
            "schedule.txt", player), thelist)
        print("Parsing the schedule for " + str(player) + "'s matches...")
        array = {"fullname": str(player), "poule": int(
            division), 'tournaments': firestore.ArrayUnion(newlist)}
        doc_ref.set(array)
        print("Setting new values for " + str(player) + "'s Account...")


def find_player_matches(file_path, player_id):
    matches = {}
    current_week = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('Week '):
                current_week = "Division " + str(division) + " - " + line
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
    return matches["tournaments"]


def merge_lists(list1, list2):
    merged_list = []

    for i in range(len(list1)):
        merged_dict = {}

        # Copy values from the first list
        merged_dict.update(list1[i])
        merged_dict.update(list2[i])
        merged_list.append(merged_dict)

    return merged_list


# generates the schedule.txt
MatchGen.MG(playerlist)
print("Generating Matches...")
# preps the firebase accounts with dates and infos
PlayerPrep(playerlist)
print("All Done!")
