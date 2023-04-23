import codemark.initialise
import codemark.firebase.database as FireDB
import codemark.secrets
import os
import subprocess


SECRET_FILE_LOC = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secrets.py")

db = FireDB.FirebaseDB()

def doctor():
    print("Running Doctor for CodeMark!\n")

    if not check_internet():
        return

    # Checks database is up or not
    if not check_server_connection():
        return

    if not check_user_cred_config():
        return

    # Checking Secrets
    if not check_secrets():
        return


    if not check_compiler():
        return

    # Directory Check
    if not check_dir():
        return

    print("\nEverything seem to look fine!\nHowever, in case of error, contact support.")


def check_internet():
    print("1. Checking Internet Connection.")
    if db.connect(hosts=["https://google.com"], check=True):
        print("INFO: Internet is working fine!")
    else:
        print("ERROR: Internet Issue! Contact your network providers")
        return False
    return True

def check_server_connection():
    print("2. Checking Server Connectivity")
    if db.connect(check=True):
        print("INFO: Server is UP!")
    else:
        print("ERROR: Server is down!")
        print("ERROR: Retry after some time. If issue persist, contact support")
        return False
    return True
    

def check_user_cred_config():
    print("3. Checking User Credential Configuration")
    if not codemark.initialise.checkAlreadyInitialized():
        print("WARNING: User credentials are not initialised")
        print("Trigerring user init")

        if codemark.initialise.initialiseCred():
            print("Credentials is initialized successfully!")
        else:
            print("ERROR: Error initializing the credentials for app! Retry later")
            return False
    else:
        print("User already initialized!")
    return True
    

def check_secrets():
    # Check if compiler is installed and is on system path
    print("4. Checking Config Files are present or not")
    if not (os.path.exists(codemark.secrets.SERVICEACCOUNTFILE) and os.path.exists(SECRET_FILE_LOC)):
        print("Secrets file does not exists. Please re-download the program.")
    print("Secret file exists")
    return True


def check_compiler():

    print("5. Checking if C compilers are installed or not.")
    
    # List of C compilers to check for
    compilers = ['gcc', 'clang', 'cl']

    hasCompiler = False
    # Check if each compiler is available on the system
    for compiler in compilers:
        if command_exists(compiler):
            print(compiler + ' is installed')
            hasCompiler = True
        else:
            print(compiler + ' is not installed')

    if hasCompiler:
        print("Compiler is installed on system!")
    else:
        print("Install C Compiler\nWindows: https://www.mingw-w64.org/downloads/\nLinux: apt install build-essentials\nMac: brew install gcc")
        return False
    return True
    

def check_dir():
    print("6. Checking config files for current assignment")
    if not os.path.exists("config.json"):
        print("You're not in downloaded assignment folder or few files are corrupted.")
        print("Re-fetch and copy the contents there")
        return False
    else:
        print("config files for assignments are present")
    return True


    

# Function to check if a command is available on the system
def command_exists(command):
    if os.name == 'nt': # For Windows
        try:
            subprocess.check_output(['where', command])
            return True
        except subprocess.CalledProcessError:
            return False
    else: # For Linux/Mac
        try:
            subprocess.check_output(['which', command])
            return True
        except subprocess.CalledProcessError:
            return False


