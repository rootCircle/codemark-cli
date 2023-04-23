import keyring
import codemark.utils
import codemark.initialise

service_name = "silicon-sorcerers-codemark-cli"

def saveCredToKeyring(email, password):
    keyring.set_password(service_name, email, password)

def getPasswordFromKeyring(email):
    return keyring.get_password(service_name, email)

def getStudentEmail():
    pass

def getCurrentStudentID():
    student_info = codemark.utils.readJSONFile(codemark.initialise.ACCOUNT_DATA_LOC)
    return student_info['student_id']

def getBatchID():
    student_info = codemark.utils.readJSONFile(codemark.initialise.ACCOUNT_DATA_LOC)
    return student_info["batch_id"]