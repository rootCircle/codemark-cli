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
        if self.connect():
            try:
                user = pauth.sign_in_with_email_and_password(email, password)
                return user
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
        else:
            print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")
            print("Warning : ","Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")

    def pushData(self, child, details, showWarning=True):
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
        :param showWarning: Shows messageBox for errors if True else not.
        :return: True : If data is successfully written
                 None : If some error arises
                 messageBox is shown if showWarning is True
        """
        if self.connect():
            try:
                results = db.reference(child).push(details)
                return True
            except (ValueError, fireexception.FirebaseError, fireexception.UnavailableError) as e:
                print("LOG : ", e)
                return
        elif showWarning:
            print("Warning : ","Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
        print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")

    def getdataOrder(self, child, ordervar, showWarning=True):
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
        :param showWarning: Shows messageBox for error if True else not.
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
                 messageBox is shown if showWarning is True
        """
        if self.connect():
            try:
                out = db.reference(child).order_by_child(ordervar).get()
                print(out)
                if out is None:
                    out = {}  # To differentiate data from errors
                return out
            except Exception as e:
                print("LOG : ", e)
                return
        elif showWarning:
            print("Warning : ", "Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
        print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")

    def getdataOrderEqual(self, child, ordervar, equalvar, showWarning=True):
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
        :param showWarning: Shows messageBox for error if True else not.
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
                 messageBox is shown if showWarning is True
        """
        if self.connect():
            try:
                out = db.reference(child).order_by_child(ordervar).equal_to(equalvar).get()
                if out is None:
                    out = {}  # To differentiate data from errors
                return out
            except Exception as e:
                print("LOG : ", e)
                return
        elif showWarning:
            print("Warning : ","Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
        print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")

    def updateData(self, child, data, identifier="Email", identifierval="", showWarning=True):
        """
        Updates data in RealTime Database with help of identifier.
        It will update all instances of data in case of multiple values found.

        In case of no identifier,function will update values for
        current user(using email by SESSION_USER.email)

        :param child: The address to the node on which data has to be fetched from
                    If one has created a table named Institute and another sub-table inside
                    the table say named Students.Idea being ,at a time all students of same
                    branch name is to be put at one branch.
                    So every new entry is defined by a random set of character allocated on data creation.
                    This key(random set of character) can be fetched using getdataOrderEqual function and
                    getting the keys of returned dictionaries using getdataOrderEqual(...).keys().
                    Each keys point of its own location in database.
        :param data: Data-Type-Dictionary Data to be updated on that node/child (Overwrite in case of data difference,
                        non-called attributes are still safe in database! Like if need to just update name ,
                        one only need to put name in data only not every other attribute.
                        Works more or less like <DICT1>.update(<DICT2>))
        :param identifier: Attribute according to which data has to be found and updated.
                            (It is recommended to use primary key type things here,
                            where there is no data duplicacy)
        :param identifierval: Value of the identifier attribute against which tuple(data) has to be found
        :param showWarning: Shows messageBox for error if True else not.

        :return: True : If data is successfully over-written
                 False : If some error arises
                 messageBox is shown if showWarning is True
        """
        try:
            if self.connect():
                if not identifierval:
                    identifierval = SESSION_USER.email
                if identifierval:
                    ref = db.reference(child).order_by_child(identifier).equal_to(identifierval).get()
                    if ref:
                        for key in list(ref.keys()):
                            result = db.reference(child).child(str(key)).update(data)
                        return True

            elif showWarning:
                print("Warning : ","Warning!",
                                       "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
                print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")
            else:
                print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")
        except Exception as e:
            print("LOG : ", e)
        return False


    def sendDataStorage(self, fileLocation, saveAsName, showWarning=True):
        """
        Stores the IMAGE into Google Cloud/ Firebase DB from a choosen local image location and return
        its database address
        Images will be stored as png file but can be modified to be used as any one.

        :param saveAsName: The name with which image would be saved on the server.(Excludes the extension)
        :param showWarning: Shows messageBox for error if True else not.

        :return:savefilename The (expected) location of image on the server. (If all goes OK!)
                False If some error occurs which is accompanied by a messageBox if allowed.
        """
        try:
            if self.connect():
                bucket = storage.bucket()
                if fileLocation and saveAsName:
                    savefilename = saveAsName
                    blob = bucket.blob(savefilename)
                    blob.upload_from_filename(fileLocation)
                    return savefilename
            elif showWarning:
                print("Warning : ","Warning!",
                                       "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
                print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")
            else:
                print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")
            return False
        except Exception as e:
            print("LOG : ", e)
            return False


    def optimiseSearchVal(self, searchVal):
        """
        This function isn't needed by devs. It just is used to optimise user entered queries
        and create various standard iterations of it.

        Standard Iteration is : Title Case, All Upper, All Lower, first word lower rest all title
                                and the searchVal itself(Cam be modified every added iteration takes extra time to complete.)
        :param searchVal: Data-Type-String The variable to contain the search query
        :return List of standard iteration of values if string is not empty
                else it just returs the string itself in list form to reduce inconsistency
        """
        if searchVal and isinstance(searchVal, str):
            x1 = searchVal.title()
            x2 = searchVal.lower()
            x3 = x1[0].lower() + x1[1:]
            x4 = searchVal.upper()

            return searchVal, x1, x2, x3, x4
        return [searchVal]

    def deepSearchData(self, child, identifier, searchVal, filtervar=None, filterval=None, showWarning=True):
        """
       A more abstracted API is provided in Apptoolsv2.itemSearch(....) which searches for data in
       relation named 'Items'

       deepSearchData function tries to search a value from database. Its main purpose is to overcome
       the limits sets by Firebase APIs as explained in FirebaseDB.searchData(...)
       Data need not to be in standard state in database for this function.

       :Functioning: It first tries normal standard Firebase searching based on Firebase API.(Lenient than
                        searchData(.....) which uses various iterations, while this doesn't).Function could be modiied
                        to give local search method also. But has not been implemented due to
                        my personal coding requirements
                    If that fails i.e. no data could be found then it forces local searching as given below:
                        It fetches all data from child table and searches them locally.(More strong and flexible)

                        This is especially not recommended if database has some sensitive information that
                        should not be in public hands and/or if the size of child node is very large(in MBs) then
                        the function would be very slow.

       For example: If one searches for "Zoo" in ["Zoo","Zooras","aZoo",""zoo","ZOO","ZoO"]
                   All the results are shown if using deepSearchData(...)

       :param child:The address to the node on which data has to be fetched from
                   If one has created a table named Institute and another sub-table inside
                   the table say named Students.Idea being ,at a time all students of same
                   branch name is to be put at one branch.
                   So every new entry is defined by a random set of character allocated on data creation.
                   This key(random set of character) can be fetched using getdataOrderEqual function and
                   getting the keys of returned dictionaries using getdataOrderEqual(...).keys().
                   Each keys point of its own location in database.
       :param identifier: The attribute against which data has to be searched.
       :param searchVal: Value of the attribute against which data has to be searched.
       :param filtervar: Acts as a seondary but optional identifier to fetched results.(Case insensitive)
                           So,it can sort and show only that data which passes a EQUALITY condition..
                           This is just a EQUALITY checker(not like search) and is done locally, not on server. Hence,
                            Firebase API's limits doesn't affect these.
                           filtervar is the name of attribute against which secondary filtering is to be done.
       :param filterval: filterval is the value of the secondary attribute against which local filtering is to be done.
       :param showWarning: Shows messageBox for error if True else not.

       :return: searchResult: Type(List nested with Dictionary of found data(no key-index just values))
                              eg.- [{'Name':Value,'Name2':Value},{.....}]
               None: If some error occured, could by followed by messageBox if allowed.
               []: If no data is found

       """
        if self.connect():
            try:
                searchResult = []
                if filterval and filtervar:
                    ref = db.reference(child).order_by_child(filtervar).equal_to(filterval).get()
                else:
                    ref = db.reference(child).order_by_child(identifier).get()
                if ref:
                    data = list(ref.values())
                    for i in data:
                        if isinstance(i[identifier], (int, float)):
                            if searchVal == i[identifier]:
                                searchResult.append(i)
                        else:
                            if isinstance(i[identifier], str) and isinstance(searchVal, str):
                                if searchVal.lower() in i[identifier].lower():
                                    searchResult.append(i)
                            else:
                                if searchVal in i[identifier]:
                                    searchResult.append(i)
                return searchResult
            except Exception as e:
                print("LOG : ", e)
                return
        elif showWarning:
            print("Warning : ","Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
        print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")

    def searchData(self, child, identifier, searchVal, filtervar=None, filterval=None, showWarning=True):
        """
        A more abstracted API is provided in Apptoolsv2.itemSearch(....) which searches for data in
        relation named 'Items'

        searchData function tries to search various standard iterations of a value from database.
        All data stored are assumed to be stored in standard state for this function.

        Firebase limit the capabilities for devs to search for data efficiently unless you pay them a
        price. The API currently allows devs to search for the values that start with parameter mandatorily.
        The given values can end with anything by the way.
        For example: If one searches for "Zoo" in ["Zoo","Zooras","aZoo",""zoo","ZOO","ZoO"]
                    Only ["Zoo","Zooras","zoo","ZOO"] is the result (ZoO is the reported due to insconsistent
                     formatting of upper and lower case)  If someone wants all of the results use
                     deepSearchData(....) function. More info is given in function docs.

        :param child:The address to the node on which data has to be fetched from
                    If one has created a table named Institute and another sub-table inside
                    the table say named Students.Idea being ,at a time all students of same
                    branch name is to be put at one branch.
                    So every new entry is defined by a random set of character allocated on data creation.
                    This key(random set of character) can be fetched using getdataOrderEqual function and
                    getting the keys of returned dictionaries using getdataOrderEqual(...).keys().
                    Each keys point of its own location in database.
        :param identifier: The attribute against which data has to be searched.
        :param searchVal: Value of the attribute against which data has to be searched.
        :param filtervar: Acts as a seondary but optional identifier to fetched results.(Case insensitive)
                            So,it can sort and show only that data which passes a EQUALITY condition..
                            This is just a EQUALITY checker(not like search) and is done locally, not on server. Hence,
                             Firebase API's limits doesn't affect these.
                            filtervar is the name of attribute against which secondary filtering is to be done.
        :param filterval: filterval is the value of the secondary attribute against which local filtering is to be done.
        :param showWarning: Shows messageBox for error if True else not.

        :return: searchResult: Type(List nested with Dictionary of found data(no key-index just values))
                               eg.- [{'Name':Value,'Name2':Value},{.....}]
                None: If some error occured, could by followed by messageBox if allowed.
                []: If no data is found

        """
        if self.connect():
            try:
                searchResult = []
                optimisedsearchval = self.optimiseSearchVal(searchVal)
                for i in optimisedsearchval:
                    ref = db.reference(child).order_by_child(identifier).start_at(i).end_at(i + "\uf8ff").get()
                    if ref:
                        searchResult.extend(list(ref.values()))

                if searchResult is None:
                    searchResult = []  # To differentiate data from errors
                if searchResult:
                    res = []
                    # Removing duplicate values due to using various iterations
                    [res.append(x) for x in searchResult if x not in res]
                    searchResult = res
                if filterval and filtervar:
                    res = []
                    for x in searchResult:
                        if isinstance(x[filtervar],str) and isinstance(filterval, str):
                            if x[filtervar].lower() == filterval.lower():
                                res.append(x)
                        elif isinstance(x[filtervar],(int,float)) and isinstance(filterval, (int,float)):
                            if x[filtervar] == filterval:
                                res.append(x)
                        else:
                            if filterval in x[filterval]:
                                res.append(x)

                    searchResult = res

                return searchResult

            except Exception as e:
                print("LOG : ", e)
                return
        elif showWarning:
            print("Warning : ","Warning!",
                                   "Failed to Connect to Server\nNo Internet Connection or Server Unreachable")
        print("LOG : ", "Failed to Connect to Server\tNo Internet Connection or Server Unreachable")

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
                    print("LOG : ", "Invalid data type 'hosts'-expected string/tuple/list\nself.connect")
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

    def logout(self):
        self.clearImgCache()
        pauth.current_user = None
        self.clearSession()
        globals()['SESSION_USER'] = None

    @staticmethod
    def writeSession(self):
        if pauth.current_user:
            try:
                os.makedirs(SESSION_FILE_FOLDER)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("LOG : ", e)
            with open(SESSION_CACHE_FILE, 'wb') as f:
                pickle.dump(pauth.current_user, f)

    @staticmethod
    def readSession(self):
        file_contents = ""
        try:
            try:
                os.makedirs(SESSION_FILE_FOLDER)
            except OSError as er:
                if er.errno != errno.EEXIST:
                    print("LOG : ", er)
            with open(SESSION_CACHE_FILE, "rb") as f:
                file_contents = pickle.load(f)
                if file_contents and self.connect():
                    pauth.current_user = ses = file_contents
                    globals()['SESSION_USER'] = auth.get_user(ses['localId'])
        except IOError as e:
            pass
            # Do nothing
        except EOFError as e:
            pass
        except firebase_admin._auth_utils.UserNotFoundError as e:
            pauth.current_user = None
            self.clearSession()
            globals()['SESSION_USER'] = None
            print("LOG : ", e)
        except fireexception.UnavailableError as e:
            print("LOG : ", e)
        except Exception as e:
            print("LOG : ", e)

    @staticmethod
    def clearSession(self):
        try:
            os.makedirs(SESSION_FILE_FOLDER)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("LOG : ", e)
        with open(SESSION_CACHE_FILE, "wb") as f:
            pass

