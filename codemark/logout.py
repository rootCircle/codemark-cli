import keyring
import codemark.utils
import codemark.account
import codemark.initialise
import os
import codemark.firebase.database as FireDB

db = FireDB.FirebaseDB()

def logout():
    # Replace 'service_name' and 'account_name' with your own values
    email = codemark.utils.readJSONFile(codemark.initialise.ACCOUNT_DATA_LOC)
    if email:
        try: 
            email = email['email']
            if email:
                keyring.delete_password(codemark.account.service_name, email)
        except KeyError:
            pass

    if os.path.isfile(codemark.initialise.ACCOUNT_DATA_LOC):
        os.remove(codemark.initialise.ACCOUNT_DATA_LOC)

    db.signout()

    codemark.utils.print_success("Logout successful!")