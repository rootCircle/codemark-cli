import getpass
import codemark.firebase.database as FireDB
from codemark.utils import print_info, print_error, print_warning, print_success

db = FireDB.FirebaseDB()

def signup():
    print_info('Enter your email and password to sign up!')
    email = input('Enter email:')
    if not db.check_mail(email):
        print_error('Invalid Email')
        return False

    password = getpass.getpass("Enter Password : ")
    if len(password) < 8:
        print_warning("Please enter at-least 8 character password!")
        return False

    cred = db.register(email, password)

    if not cred:
        return False

    print_success("Registered Successfully!")
    return True