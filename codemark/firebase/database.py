# -*- coding: utf-8 -*-
"""
Requirements:
    libraries,
    local image files,
    service-account-file + see line @114
pyrebase:login
firebase_admin:db,registration
firebase storage:All Images are saved and retrieved as .png file
Email must always be in lower case
"""

"""
TODO : Add support for '#.$[]\' in firebase
TODO : Uncomment connect tests
"""



import os
import errno
import pyrebase
import urllib.request
import json
import pickle
import requests.exceptions
import re
import firebase_admin as firebaseadmin
import firebase_admin._auth_utils
from google.auth.exceptions import TransportError
from firebase_admin import auth, db, storage
from firebase_admin import exceptions as fireexception
import codemark.secrets



"""
Firebase Credentials
Dev need to enable login via EMAIL and PASSWORD in authentication section.
Put DB URL from RealTime Database section dashboard
FOR firebaseConfig variable : copy details from creating a web-app section in that firebase database
SERVICEACCOUNTFILE can be downloaded from setting section of Realtime database

in firebase variable:storage-bucket can be fetched from Storage section in Firebase
"""

dbURL = codemark.secrets.dbURL
SERVICEACCOUNTFILE = codemark.secrets.SERVICEACCOUNTFILE
STORAGE_BUCKET_URL = codemark.secrets.STORAGE_BUCKET_URL

firebaseConfig = codemark.secrets.firebaseConfig


pfirebase = pyrebase.initialize_app(firebaseConfig)
pauth = pfirebase.auth()

cred = firebaseadmin.credentials.Certificate(SERVICEACCOUNTFILE)
firebase = firebaseadmin.initialize_app(cred, {
    'databaseURL': dbURL,
    'storageBucket': STORAGE_BUCKET_URL
})

SESSION_USER = None
SESSION_FILE_FOLDER = "res"
SESSION_CACHE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), SESSION_FILE_FOLDER, "sessioncache.dat")


class FirebaseDB:
    def __init__(self):
        pass

    @staticmethod
    def signout(self):
        """
        Flushes pauth.current_user variable

        Returns True :after process is completed
                None :if some error occurs
        """
        try:
            pauth.current_user = None
            return True
        except Exception as e:
            print(e)

    def login(self, email, password):
        """
        Provides SESSION details and service for authentication.
        Login using username is not supported and hence should be applied using
        another table pointing to email to username as defined in function create_account(...)

        :param email: Email for authentication
        :param password: Password
        :return: User credentials(Data Type: Dictionary) after login if everything is OK!
                    Contains Keys
                    kind , localId, email, displayName, idToken, registered, expiresIn, refreshToken

                None: If any error occurred like malformed email,invalid password, no internet etc
        """
        try:
            user = pauth.sign_in_with_email_and_password(email, password)
            return user
        except requests.exceptions.ConnectionError as e:
            # Handle the "Network is unreachable" error
            print("ERROR: Network is unreachable.")
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "INVALID_PASSWORD":
                print("Warning : ","Invalid credentials", "Enter correct Password!")
            elif error == "EMAIL_NOT_FOUND":
                print("Warning : ","User not registered", "There is no user registered with this Email-Id.")
            else:
                print("Warning : ","Error",
                                        "Some Error Occured while Logging-in\nPlease Retry!\n" + str(
                                            error))
            print(error)

    def pushData(self, child, details):
        """
        Writes data to FirebaseDB
        :param child: The address to the node on which data has to be written
                    If one has created a table named Institute and another sub-table inside
                    the table say named Students.Idea being, at a time all students of same
                    branch name is to be put at one branch.
                    So every new entry is defined by a random set of character allocated on data creation.
                    This key(random set of character) can be fetched using getdataOrderEqual function and
                    getting the keys of returned dictionaries. Each keys point of its own location
                    in database.
        :param details: Data-Type-Dictionary All the details in form of dictionary, one want to push
        :return: True : If data is successfully written
                 None : If some error arises
        """
        try:
            results = db.reference(child).push(details)
            return True
        except TransportError as e:
            # Handle the "Network is unreachable" error
            print("ERROR: Network is unreachable.")
            return
        except (ValueError, fireexception.FirebaseError, fireexception.UnavailableError) as e:
            print("ERROR : ", e)
            return

    def getdataOrder(self, child, ordervar):
        """
        Gets data from FirebaseDB ordered by ordervar
        :param child: The address to the node on which data has to be fetched from
                    If one has created a table named Institute and another sub-table inside
                    the table say named Students.Idea being ,at a time all students of same
                    branch name is to be put at one branch.
                    So every new entry is defined by a random set of character allocated on data creation.
                    This key(random set of character) can be fetched using getdataOrderEqual function and
                    getting the keys of returned dictionaries using getdataOrderEqual(...).keys().
                    Each keys point of its own location in database.
        :param ordervar: The name of attribute according to which data has to be sorted
        :return: out : If data is successfully fetched
                       Data Type-Dictionary
                        {key:values pair}
                        each key:values pair correspond to a single a result found
                            This key is same as random set of character allocated on data creation.
                            and can be useful for accessing sub-child for that table.

                            The values is again a nested dictionary containing info about
                            fetched data in key:values pair where key is attribute and values is
                            the data in that attribute

                        In order to get data, say Name is the attribute and we need it
                        list(FirebaseDB.getdataOrder(...).values()) -> Contains all sets of N results found

                        To get first one:
                        list(FirebaseDB.getdataOrder(...).values())[0]['Name']

                 None : If some error arises
        """
        try:
            out = db.reference(child).order_by_child(ordervar).get()
            print(out)
            if out is None:
                out = {}  # To differentiate data from errors
            return out
        except TransportError as e:
            # Handle the "Network is unreachable" error
            print("ERROR: Network is unreachable.")
            return
        except Exception as e:
            print("ERROR : ", e)
            return

    def getdataOrderEqual(self, child, ordervar, equalvar):
        """
        Gets data from FirebaseDB ordered by ordervar
        :param child: The address to the node on which data has to be fetched from
                    If one has created a table named Institute and another sub-table inside
                    the table say named Students.Idea being ,at a time all students of same
                    branch name is to be put at one branch.
                    So every new entry is defined by a random set of character allocated on data creation.
                    This key(random set of character) can be fetched using getdataOrderEqual function and
                    getting the keys of returned dictionaries using getdataOrderEqual(...).keys().
                    Each keys point of its own location in database.
        :param ordervar: The name of attribute for which equality has to be checked
        :param equalvar: The corresponding value to which equality is to be checked
        :return: out : If data is successfully fetched
                       Data Type-Dictionary
                        {key:values pair}
                        each key:values pair correspond to a single a result found
                            This key is same as random set of character allocated on data creation.
                            and can be useful for accessing sub-child for that table.

                            The values is again a nested dictionary containing info about
                            fetched data in key:values pair where key is attribute and values is
                            the data in that attribute

                        In order to get data, say Name is the attribute and we need it
                        list(FirebaseDB.getdataOrderEqual(...).values()) -> Contains all sets of N results found

                        To get first one:
                        list(FirebaseDB.getdataOrder(...).values())[0]['Name']


                 None : If some error arises
        """
        try:
            out = db.reference(child).order_by_child(ordervar).equal_to(equalvar).get()
            if out is None:
                out = {}  # To differentiate data from errors
            return out
        except TransportError as e:
            # Handle the "Network is unreachable" error
            print("ERROR: Network is unreachable.")
            return
        except Exception as e:
            print("ERROR : ", e)
            return

    def sendDataStorage(self, fileLocation, saveAsName):
        """
        Stores the IMAGE into Google Cloud/ Firebase DB from a choosen local image location and return
        its database address
        Images will be stored as png file but can be modified to be used as any one.

        :param saveAsName: The name with which image would be saved on the server.(Excludes the extension)

        :return:savefilename The (expected) location of image on the server. (If all goes OK!)
                False If some error occurs which is accompanied by a messageBox if allowed.
        """
        try:
            bucket = storage.bucket()
            if fileLocation and saveAsName:
                savefilename = saveAsName
                blob = bucket.blob(savefilename)
                blob.upload_from_filename(fileLocation)
                return savefilename
            return False
        except TransportError as e:
                # Handle the "Network is unreachable" error
                print("ERROR: Network is unreachable.")
                return False
        except Exception as e:
            print("ERROR : ", e)
            return False

    
    def connect(self, hosts=['http://google.com', dbURL], check = False):
        """
        Tries to connect to various hosts (By default Google and Firebase Server)
        and check if user has valid internet connection or not.
        It is recommended to include dbURL to check if server is down or not with
        a recommended popular website like wikipedia, google etc.

        :param hosts: (DataType-List/Tuple/String) A list of hosts against which connection has
                                                to be checked.

        return: True if successfully connects to server
                False if failed to connect to server

        warning: unless check is set to True, this will always return True
        """
        try:
            if check:
                if isinstance(hosts, (list, tuple)):
                    for host in hosts:
                        urllib.request.urlopen(host)
                    return True
                elif isinstance(hosts, str):
                    urllib.request.urlopen(hosts)
                    return True
                else:
                    print("ERROR : ", "Invalid data type 'hosts'-expected string/tuple/list")
                    return False
            else:
                return True
        except:
            return False

    def check_mail(self, email):
        if email and isinstance(email, str):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(regex, email):
                return True
        return False



