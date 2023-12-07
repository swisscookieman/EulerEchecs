import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import main

cred = credentials.Certificate(
    "newkey.json")
firebase_admin.initialize_app(cred, None, "2")
db = firestore.client()


def PlayerPrep(playerlist):
    division = main.division
    for player in playerlist:
        doc_ref = db.collection("users_s2").document(str(player))
        doc_ref.set({"fullname": str(player), "poule": int(
            division), 'tournaments': firestore.ArrayUnion([1])})
