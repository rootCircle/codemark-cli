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
    - Click on the **Create project** button.
    - Once your project is created, click on the **Project settings** tab.
    - Click on the **Service accounts** tab.
    - Click on the **Generate new private key** button.
    - Click on the **Generate Key** button.
    - A file will be downloaded to your computer rename to `service-account-file.json`.
    - Save the downloaded JSON file in the `./codemark/firebase/res/` directory.

3. **Enable Firebase Authentication (with email and password):**
    - Go to the Firebase Console: Firebase Console.
    - Select your Firebase project.
    - In the left sidebar, click on "Authentication."
    - In the "Authentication" section, click on the "Sign-in method" tab.
    - Find the "Email/Password" sign-in method and click the "Edit" button (pencil icon).
    - Enable the "Email/Password" sign-in method by toggling the switch to the "Enabled" position.
    - Click the "Save" button to save your changes.

4. **Enable Firebase Realtime Database:**
    - In the Firebase Console, select your Firebase project.
    - In the left sidebar, click on "Realtime Database."
    - Click the "Create Database" button.
    - Choose the "Start in test mode" option for now. You can adjust the security rules later as needed for your application.
    - Click the "Next" button.
    - Choose a location for your database and click the "Done" button.
    - Your Realtime Database is now created and accessible from the Firebase Console.
    - Go to the Rules Section, and put the below data and publish
  
```json
{
  "rules": {
    "assignments" :{
      ".indexOn":["batch_id", "assignment_id"],
    },
    "submissions" : {
      ".indexOn":["student_id", "submission_id"],
    },
    "users" : {
      ".indexOn" : ["email"],
    },
    "students" : {
      ".indexOn" : ["email"],
    },
    "plagcache" : {
      ".indexOn" : ["assignment_id"],
    },
  
    ".read": "true",  // Testing, change it later
    ".write": "true",  // Testing, Change it later
  }
}
```

These steps should help you enable Firebase Authentication with email and password and set up the Realtime Database for your Firebase project.


### API Keys

1. #### OpenAI API Key

    - Go to the OpenAI platform: [platform.openai.com](https://platform.openai.com/)
    - Click on the Sign in button.
    - Sign in with your OpenAI account.
    - Click on the API Keys tab.
    - Click on the Create new API key button.
    - Copy the API key and save it in a safe place.

2. #### Web3.Storage API Key
    - Go to Web3 Storage: [web3.storage](https://web3.storage)
    - Click on the Sign up button.
    - Create a Web3 Storage account.
    - Click on the API keys tab.
    - Click on the Create new API key button.
    - Copy the API key and save it in a safe place.

### Additional Configuration
Before initializing Firebase and pushing dummy data, perform the following additional configurations:

1. #### Firebase Storage
    - Enable Firebase Storage: In the Firebase Console, navigate to your project and go to "Storage." Follow the prompts to enable Firebase Storage.
    - Go to the Firebase console: https://console.firebase.google.com/
    - Click on your project.
    - Click on the **Storage** tab.
    - Click on the **Get started** button.
    - Follow the instructions to enable Firebase Storage.


2. #### Set up your secrets:
    - To get your firebase config:
    - Go to Project Setting
    - Click on General
    - Scroll to bottom Section 
    - Select Your Apps and Add new App in web 
    - copy the key, values and place them selectively in firebaseConfig

| Name of env variable | Type | Description | Source |
| -------------------- | ---- | ----------- | ------ | 
| OPENAI_API_KEY | string | OpenAI Api Key | platform.openai.com |
| FIREBASE_DATABASE_URL | string | databaseUrl of firebaseConfig | console.firebase.google.com |
| FIREBASE_API_KEY | string | apiKey of firebaseConfig | console.firebase.google.com | 
| FIREBASE_AUTH_DOMAIN | string | authDomain of firebaseConfig | console.firebase.google.com |
| FIREBASE_PROJECT_ID | string | projectID of firebaseConfig | console.firebase.google.com | 
| FIREBASE_MESSAGEING_SENDER_ID | string | messagingSenderId of firebaseConfig | console.firebase.google.com |
| FIREBASE_APP_ID | string | appId of firebaseConfig | console.firebase.google.com |
| FIREBASE_STORAGE_BUCKET_URL | string | storageBucket of firebaseConfig | console.firebase.google.com |
| WEB3_STORAGE_API_KEY | string | Web3 Storage API Key | web3.storage |

## Import JSON Data Using the GUI

If you prefer a graphical interface for importing data into Firebase, follow these steps to use the Firebase Console GUI:

- **Go to the Firebase Console**: Navigate to the [Firebase Console](https://console.firebase.google.com/).
- **Select Your Project**: Click on your Firebase project in the console. If you haven't created a project yet, follow the earlier instructions to create one.
- **Access Realtime Database**: In the Firebase Console, click on the **Realtime Database** tab on the left sidebar.
- **Import Data**: Click on the **Import JSON** button located at the top of the Realtime Database section.
- **Choose Your JSON File**: A file selection dialog will appear. Select the `../Schemas/dummy_data.json` file from your project directory.
- **Start Import**: After selecting the file, click on the **Open** or **Import** button (the label may vary depending on your operating system).
- **Confirm Import**: Firebase will display a preview of the data to be imported. Verify that it matches your dummy data structure.
- **Initiate Import**: If everything looks correct, click on the **Import** button to start the data import process.
- **Monitor Progress**: Firebase will show the progress of the data import. Once completed, you will receive a confirmation message.



<details><summary>Optional: <b>Uploading through a Python script</b></summary>

**If you prefer to upload data using a Python script, follow these steps:** creating a new Python file called `dummy_data.py` and adding the following code:

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
   with open("../Schemas/dummy_data.json", "r") as file:
       dummy_data = json.load(file)

   # Push the dummy data to the Firebase Realtime Database
   ref.update(dummy_data)

   print("Dummy data has been pushed to the Firebase Realtime Database.")

```
   
Run Script using

```python
   python upload_dummy_data.py
```

This code will push the dummy data in the `dummy_data.json` file to the Firebase Realtime Database.

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
