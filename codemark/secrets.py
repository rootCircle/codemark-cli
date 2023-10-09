import os
from dotenv import load_dotenv

load_dotenv()
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICEACCOUNTFILE = os.path.join(dir_path,"firebase", "res", "service-account-file.json")
api_key= os.getenv("OPENAI_API_KEY")# OPENAI KEY
dbURL = os.getenv("FIREBASE_DATABASE_URL")
FIREBASE_STORAGE_BUCKET_URL = os.getenv("FIREBASE_STORAGE_BUCKET_URL")
firebaseConfig = {
    "apiKey":os.getenv("FIREBASE_API_KEY") ,
    "authDomain":os.getenv("FIREBASE_AUTH_DOMAIN"),
    'databaseURL': dbURL,
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket":FIREBASE_STORAGE_BUCKET_URL ,
    "messagingSenderId":os.getenv("FIREBASE_MESSAGEING_SENDER_ID") ,
    "appId":os.getenv("FIREBASE_APP_ID") ,
    "serviceAccount": SERVICEACCOUNTFILE
}

# from web3.storage
web3storage_api_key = os.getenv("WEB3_STORAGE_API_KEY")