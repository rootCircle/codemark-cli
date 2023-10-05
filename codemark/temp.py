import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate("firebase/res/service-account-file.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project.firebaseio.com'
})

# Reference to the Firebase Realtime Database
ref = db.reference("/")

# Load the dummy data from the schema file
with open("../schemas/dummy_data.json", "r") as file:
    dummy_data = json.load(file)

# Push the dummy data to the Firebase Realtime Database
ref.update(dummy_data)

print("Dummy data has been pushed to the Firebase Realtime Database.")
