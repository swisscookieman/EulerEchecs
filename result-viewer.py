import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
import re


# SETUP HERE ------------------

week = 9   # current week here (int 1-9)
thediv = 3

# SETUP END -------------------

cred = credentials.Certificate(
    "echecseuler-firebase-adminsdk-25xs4-89c7756f0f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get the collection reference.
collection_ref = db.collection('tournaments')

# Get all documents in the collection.
documents = collection_ref.get()


def getmatches(division):
    list = []
    for document in documents:
        weekid = "s" + str(week)
        divisionid = "d" + str(division)
        if weekid in document.id and divisionid in document.id:
            doc = document.to_dict()
            doc = doc['result']
            list.append(doc)
    return list


getmatches(1)


def parse_match_result(match_result):
    # Define a regular expression pattern to capture the four pieces
    pattern = re.compile(r'([^0-9]+)([0-9]+)-([0-9]+)(.*)')

    # Use the pattern to match the input string
    match = pattern.match(match_result)

    if match:
        # Extract the four pieces from the match groups
        before_first_number = match.group(1).strip()
        first_number = match.group(2)
        second_number = match.group(3)
        after_second_number = match.group(4).strip()

        # Return the parsed pieces
        return before_first_number, first_number, second_number, after_second_number
    else:
        # Return None if the input string does not match the pattern
        return None


def convert_to_csv(match_results, output_filename):
    # Create a CSV file and write the header
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Player 1 Name', 'Player 1 Score',
                      'Player 2 Score', 'Player 2 Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write the match results to the CSV file
        for match_result in match_results:
            data = dict(zip(fieldnames, parse_match_result(match_result)))
            writer.writerow(data)


# Call
match_results = getmatches(thediv)
convert_to_csv(match_results, "matchoutputs/outputd" +
               str(thediv) + "s" + str(week) + ".csv")
