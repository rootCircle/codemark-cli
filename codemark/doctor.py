import codemark.initialise
import codemark.firebase.database as FireDB
import codemark.secrets
import os
import subprocess
from codemark.utils import print_error, print_info, print_message, print_success, print_warning


SECRET_FILE_LOC = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secrets.py")

db = FireDB.FirebaseDB()

def doctor():
    print_info("Running Doctor for CodeMark!\n")

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

    print_success("\nEverything seem to look fine!\nHowever, in case of error, contact support.")


def check_internet():
    print_info("1. Checking Internet Connection.")
    if db.connect(hosts=["https://google.com"], check=True):
        print_message("Internet is working fine!")
    else:
        print_error("Internet Issue! Contact your network providers")
        return False
    return True

def check_server_connection():
    print_info("2. Checking Server Connectivity")
    if db.connect(check=True):
        print_message("Server is UP!")
    else:
        print_error("Server is down!")
        print_error("Retry after some time. If issue persist, contact support")
        return False
    return True
    

def check_user_cred_config():
    print_info("3. Checking User Credential Configuration")
    if not codemark.initialise.checkAlreadyInitialized():
        print_warning("User credentials are not initialised")
        print_info("Trigerring user init")

        if codemark.initialise.initialiseCred():
            print_success("Credentials is initialized successfully!")
        else:
            print_error("Error initializing the credentials for app! Retry later")
            return False
    else:
        print_message("User already initialized!")
    return True
    

def check_secrets():
    # Check if compiler is installed and is on system path
    print_info("4. Checking Config Files are present or not")
    if not (os.path.exists(codemark.secrets.SERVICEACCOUNTFILE) and os.path.exists(SECRET_FILE_LOC)):
        print_error("Secrets file does not exists. Please re-download the program.")
    print_message("Secret file exists")
    return True


def check_compiler():

    print_info("5. Checking if C compilers are installed or not.")
    
    # List of C compilers to check for
    # compilers = ['gcc', 'clang', 'cl']
    compilers = ['gcc']

    hasCompiler = False
    # Check if each compiler is available on the system
    for compiler in compilers:
        if command_exists(compiler):
            print_info(compiler + ' is installed')
            hasCompiler = True
        else:
            print_warning(compiler + ' is not installed')

    if hasCompiler:
        print_message("Compiler is installed on system!")
    else:
        print_message("Install C Compiler\nWindows: https://www.mingw-w64.org/downloads/\nLinux: apt install build-essentials\nMac: brew install gcc")
        return False
    return True
    

def check_dir():
    print_info("6. Checking config files for current assignment")
    if not os.path.exists("config.json"):
        print_error("You're not in downloaded assignment folder or few files are corrupted.")
        print_error("Re-fetch and copy the contents there")
        return False
    else:
        print_message("config files for assignments are present")
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


