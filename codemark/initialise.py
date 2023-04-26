import appdirs
import os
import codemark.utils
import codemark.account
import codemark.firebase.database as FireDB
import getpass
from codemark.utils import print_error, print_info, print_message, print_success, print_warning


db = FireDB.FirebaseDB()

# Get the user's local data directory
data_dir = appdirs.user_data_dir()

ACCOUNT_DATA_DIR = os.path.join(data_dir, "codemark_cli")
ACCOUNT_DATA_LOC = os.path.join(ACCOUNT_DATA_DIR, "account_cred.json")

def initApp():
    if not checkAlreadyInitialized():
        if initialiseCred():
            print_success("Credentials is initialized successfully!")
        else:
            print_error("Error initializing the credentials for app! Retry later")
    else:
        print_warning("User Credentials already initialized")
        return True

def initialiseCred():
    print_info("Initializing Configurations for User")

    email = input("Enter Email : ")
    if not db.check_mail(email):
        print_error("Invalid Email")
        return False
    
    password = getpass.getpass("Enter Password : ")
    if len(password) < 8:
        print_warning("Please enter at-least 8 character password!")
        return False

    cred = db.login(email, password)

    if not cred:
        # The login function automatically handles the messages
        return False

    # User has login-ed successfully
    print_success("Logined Successfully!")

    user_content = db.getdataOrderEqual("users", "email", email)
    student_content = db.getdataOrderEqual("students", "email", email)

    if not user_content or not student_content:
        print_error("Error! Fetching Details. Retry Later.") 
        if student_content is not None and not student_content:
            print_warning("You sure are student?")
        return False

    codemark.account.saveCredToKeyring(email, password)

    
    student_content = list(student_content.values())[0]
    user_content = list(user_content.values())[0]

    user_content.update(student_content)
    
    try:
        # Create target Directory
        os.mkdir(ACCOUNT_DATA_DIR)
    except FileExistsError:
        pass

    codemark.utils.writeJSONToFile(ACCOUNT_DATA_LOC, user_content)

    return True

def checkAlreadyInitialized():
    if not os.path.isfile(ACCOUNT_DATA_LOC):
        return False
    
    userInfo = codemark.utils.readJSONFile(ACCOUNT_DATA_LOC)

    if not isinstance(userInfo, dict):
        return False

    try: 
        email = userInfo['email']
    except KeyError:
        return False
    
    password = codemark.account.getPasswordFromKeyring(email)
    if not password:
        return False

    # Detect login cred is correct or not
    cred = db.login(email, password)

    if not cred:
        return False
    
    return True







