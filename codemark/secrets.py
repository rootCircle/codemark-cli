import os
from dotenv import load_dotenv

load_dotenv()
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICEACCOUNTFILE = os.path.join(dir_path,"firebase", "res", "service-account-file.json")
api_key= os.getenv("API_KEY")# OPENAI KEY
dbURL = os.getenv("DBURL")
firebaseConfig = {
    "apiKey":os.getenv("FBAPIKEY") ,
    "authDomain":os.getenv("AUTHDOMAIN"),
    'databaseURL': dbURL,
    "projectId": os.getenv("PROJECTID"),
    "storageBucket":os.getenv("STORAGEBUCKET") ,
    "messagingSenderId":os.getenv("MESSAGEINGSENDERID") ,
    "appId":os.getenv("APPID") ,
    "serviceAccount": SERVICEACCOUNTFILE
}
STORAGE_BUCKET_URL = os.getenv("STORAGEBUCKETURL")

# from web3.storage
web3storage_api_key = os.getenv("WEB3STORAGEAPIKEY")