import keyring

service_name = "silicon-sorcerers-codemark-cli"

def saveCredToKeyring(email, password):
    keyring.set_password(service_name, email, password)

def getPasswordFromKeyring(email):
    return keyring.get_password(service_name, email)

def getStudentEmail():
    pass

def getCurrentStudentID():
    return "STU001"

def getBatchID():
    return "B1"