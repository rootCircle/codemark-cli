# Setting Up Firebase and Configuration Instructions

This guide provides step-by-step instructions to set up Firebase for your project, configure secrets, meet prerequisites, and push dummy data to the Realtime Database. Additionally, it includes instructions on enabling Firebase services, obtaining API keys, and configuring Firebase Authentication, Web3 Storage, and OpenAI.

## Table of Contents

- [Setting Up Firebase and Configuration Instructions](#setting-up-firebase-and-configuration-instructions)
  - [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Requirements](#requirements)
    - [Firebase Services](#firebase-services)
    - [API Keys](#api-keys)
      - [OpenAI API Key](#openai-api-key)
      - [Web3.Storage API Key](#web3storage-api-key)
  - [Additional Configuration](#additional-configuration)
      - [Firebase Storage](#firebase-storage)
  - [Set up your secrets:](#set-up-your-secrets)
    - [Import JSON Data Using the GUI](#import-json-data-using-the-gui)
  - [File Structure](#file-structure)

# Installation
## Requirements

Before you start setting up Firebase and pushing dummy data, ensure you meet the following requirements:

### Firebase Services

1. **Google Account**: You need a Google account to create and manage Firebase projects.
2. **Get your Firebase on.** This means creating a Firebase account and downloading the JSON key file.

- Go to the Firebase console: https://console.firebase.google.com/
- Click on the **Add project** button.
- Enter a name for your project and click on the **Continue** button.
- Select the Google Cloud Platform project to associate with your Firebase project, or create a new one.
- Select the location where you want to store your Firebase project data.
- Click on the **Create project** button.
- Once your project is created, click on the **Project settings** tab.
- Click on the **Service accounts** tab.
- Click on the **Generate new private key** button.
- Click on the **Generate Key** button.
- A file named `service-account-file.json` will be downloaded to your computer.
- Save the downloaded JSON file in the `firebase/res/` directory.

### API Keys

#### OpenAI API Key

- Go to the OpenAI platform: [platform.openai.com](https://platform.openai.com/)
- Click on the Sign in button.
- Sign in with your OpenAI account.
- Click on the API Keys tab.
- Click on the Create new API key button.
- Copy the API key and save it in a safe place.

#### Web3.Storage API Key

- Go to Web3 Storage: [web3.storage](https://web3.storage)
- Click on the Sign up button.
- Create a Web3 Storage account.
- Click on the API keys tab.
- Click on the Create new API key button.
- Copy the API key and save it in a safe place.

## Additional Configuration

Before initializing Firebase and pushing dummy data, perform the following additional configurations:

#### Firebase Storage

**Enable Firebase Storage**: In the Firebase Console, navigate to your project and go to "Storage." Follow the prompts to enable Firebase Storage.
- Go to the Firebase console: https://console.firebase.google.com/
- Click on your project.
- Click on the **Storage** tab.
- Click on the **Get started** button.
- Follow the instructions to enable Firebase Storage.

## Set up your secrets:
- This involves creating a new Python file called `secrets.py` and adding the following code:

   ```python

   import os

   dir_path = os.path.dirname(os.path.realpath(__file__))
   SERVICEACCOUNTFILE = os.path.join(dir_path, "firebase", "res", "service-account-file.json")
   api_key = "sk-asjkdsakdasasdklldas"  # OPENAI KEY
   dbURL = "https://codemark-jdxknzklndkasnkldjkasljd.firebasedatabase.app/"
   firebaseConfig = {
      "apiKey": "jfdskjlksdflskfkslfk-QEhUe_bI",
      "authDomain": "codemark-hfksjdfksdf.firebaseapp.com",
      'databaseURL': dbURL,
      "projectId": "codemark-6f33a",
      "storageBucket": "codemark-sdjfkjkflsd.appspot.com",
      "messagingSenderId": "jfdskfjdsk",
      "appId": "1:lkjsdfjsdjfklsj:web:hsdfkjkdlsjfklsdj",
      "serviceAccount": SERVICEACCOUNTFILE
   }
   STORAGE_BUCKET_URL = 'codemark-jkhsdkfjskdfjlksdjf.appspot.com'

   # from web3.storage
   web3storage_api_key = 'zxjkkcljzxkc.eyJzdWIiOiJkaWQ'

   ```
   <b>note:</b> You will need to replace the `api_key` and `web3storage_api_key` values with your own API keys.


### Import JSON Data Using the GUI

If you prefer a graphical interface for importing data into Firebase, follow these steps to use the Firebase Console GUI:

1. **Go to the Firebase Console**: Navigate to the [Firebase Console](https://console.firebase.google.com/).

2. **Select Your Project**: Click on your Firebase project in the console. If you haven't created a project yet, follow the earlier instructions to create one.

3. **Access Realtime Database**: In the Firebase Console, click on the **Realtime Database** tab on the left sidebar.

4. **Import Data**: Click on the **Import JSON** button located at the top of the Realtime Database section.

5. **Choose Your JSON File**: A file selection dialog will appear. Select the `Schemas/dummy_data.json` file from your project directory.

6. **Start Import**: After selecting the file, click on the **Open** or **Import** button (the label may vary depending on your operating system).

7. **Confirm Import**: Firebase will display a preview of the data to be imported. Verify that it matches your dummy data structure.

8. **Initiate Import**: If everything looks correct, click on the **Import** button to start the data import process.

9. **Monitor Progress**: Firebase will show the progress of the data import. Once completed, you will receive a confirmation message.



<details><summary>Optional: <b>Uploading through a Python script</b></summary>

**If you prefer to upload data using a Python script, follow these steps:** creating a new Python file called `push_dummy_data.py` and adding the following code:

   ```python

   ### Optional: Uploading Data Through a Python Script

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
   
Run Script using

```python
   python upload_dummy_data.py
```

This code will push the dummy data in the `Schemas/users.json` file to the Firebase Realtime Database.


</details>

## File Structure

Here's how the file structure should look:

```lua
❯ tree                    
.
├── codemark
│   ├── account.py
│   ├── check.py
│   ├── doctor.py
│   ├── firebase
│   │   ├── database.py
│   │   └── res
│   │       └── service-account-file.json
│   ├── get.py
│   ├── initialise.py
│   ├── __int__.py
│   ├── list.py
│   ├── logout.py
│   ├── result.py
│   ├── review.py
│   ├── scripts
│   │   ├── cm_cli.py
│   │   ├── __init__.py
│   ├── secrets.py
│   ├── submit.py
│   └── utils.py
├── LICENSE
├── logo.png
├── README.md
├── Schemas
│   ├── codemark-6f33a-default-rtdb-export.json
│   ├── dummy data.json
│   ├── Schema.old.txt
│   └── Schema.txt
├── Screenshots
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
└── setup.py

```