## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
- [Initialize Firebase](#initialize-firebase)
  - [File Structure](#file-structure)

# Installation

## Prerequisites

Before you start setting up Firebase and pushing dummy data, make sure you have the following prerequisites:

1. **Google Account**: You need a Google account to create and manage Firebase projects.

2. **Python 3 Environment**: Ensure you have Python 3 installed on your machine.

3. **Firebase Project**: Create a Firebase project with the Realtime Database enabled. You can set up a project in the [Firebase Console](https://console.firebase.google.com/).

4. **Firebase Admin SDK**: Install the Firebase Admin SDK in your project using `pip`:

   ```bash
   pip install firebase-admin
   ```

# Initialize Firebase

To initialize Firebase and push dummy data to the Realtime Database, follow these steps:

1. Create a Python script (e.g., `dummy_data.py`) to push the dummy data to Firebase. Here's an example script:

   ```python
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
   with open("schemas/dummy_data.json", "r") as file:
       dummy_data = json.load(file)

   # Push the dummy data to the Firebase Realtime Database
   ref.update(dummy_data)

   print("Dummy data has been pushed to the Firebase Realtime Database.")
   ```

2. Create a new Python file called `secrets.py` and add your Firebase credentials:

   ```python
   import os

   # Get the current directory path
   dir_path = os.path.dirname(os.path.realpath(__file__))

   # Firebase configuration
   SERVICEACCOUNTFILE = os.path.join(dir_path, "firebase", "res", "service-account-file.json")
   dbURL = "https://your-firebase-project.firebaseio.com/"
   firebaseConfig = {
       "apiKey": "your-api-key",
       "authDomain": "your-firebase-project.firebaseapp.com",
       'databaseURL': dbURL,
       "projectId": "your-firebase-project-id",
       "storageBucket": "your-firebase-project.appspot.com",
       "messagingSenderId": "your-messaging-sender-id",
       "appId": "your-app-id",
       "serviceAccount": SERVICEACCOUNTFILE
   }

   # OpenAI API key
   api_key = "your-openai-api-key"

   # Firebase Storage Bucket URL
   STORAGE_BUCKET_URL = 'your-firebase-storage-bucket-url'

   # Web3.Storage API key (if needed)
   web3storage_api_key = 'your-web3storage-api-key'
   ```

3. Run your script to push the dummy data:

   ```bash
   python dummy_data.py
   ```

## File Structure

Here's how the file structure should look:

```plaintext
project_directory/
|-- firebase/
|   |-- res/
|   |   |-- service-account-file.json
|   |   +-- ...
|   +-- ...
|-- schemas/
|   |-- dummy_data.json
|   +-- ...
|-- secrets.py
|-- dummy_data.py
```

With these steps, you'll be able to set up Firebase and push dummy data to the Realtime Database for your project.