import getpass
import codemark.firebase.database as FireDB
from codemark.utils import print_info, print_error, print_warning, print_success
from codemark.submit import generate_hash

db = FireDB.FirebaseDB()

def signup():
    print_info("Are you a student or a professor? ((s)tudent/(p)rofessor")
    resp = input('Response: ')
    
    # if the user is a student
    if resp.lower() == 's' or resp.lower() == 'student':
        print_info('Enter your details to sign up!')
        email = input('Enter email: ')
        if not db.check_mail(email):
            print_error('Invalid Email')
            return False

        password = getpass.getpass("Enter Password : ")
        if len(password) < 8:
            print_warning("Please enter at-least 8 character password!")
            return False

        student_id = generate_hash()
        
        name = input('Enter your name: ')
        college_name = input('Enter the name of your college: ')
        passing_year = input('Enter your year of passing: ')
        if not passing_year.isnumeric():
            print_error("The passing year must be in digit format (eg. 2021, 2022)")
            return False
        field_of_study = input('Enter your field of study: ')
        batch_semester = input('Enter your batch semester (1-8): ')
        
        if not batch_semester.isnumeric():
            print_error('Please enter a valid number in digit format (e.g., 1, 2, 3).')
            return False
        if int(batch_semester) not in list(range(1, 9)):
            print_error('Batch Semester must be in the range 1-8')
            return False

        user_config = {
            'email': email,
            'user_type': 'student',
            'name': name,
            'college_name': college_name,
            'student_id': student_id
        }
        student_config = {
            'batch_id': 'B'+batch_semester,
            'batch_semester': batch_semester,
            'college_name': college_name,
            'email': email,
            'field_of_study': field_of_study,
            'name': name,
            'passing_year': passing_year,
            'student_id': student_id
        }

        cred = db.register(email, password, 'students', user_config, student_config)
        if not cred:
            return False

        print_success("Registered Successfully!")
        return True
    
    # if the user is a professor
    elif resp.lower() == 'p' or resp.lower() == 'professor':
        print_info('Enter your details to sign up!')
        email = input('Enter email: ')
        if not db.check_mail(email):
            print_error('Invalid Email')
            return False

        password = getpass.getpass("Enter Password : ")
        if len(password) < 8:
            print_warning("Please enter at-least 8 character password!")
            return False

        name = input('Enter your name: ')
        college_name = input('Enter the name of your college: ')
        professor_id = generate_hash()


        user_config = {
            'email': email,
            'user_type': 'professor',
            'name': name,
            'college_name': college_name,
            'professor_id': professor_id
        }
        professor_config = {
            'college_name': college_name,
            'name': name,
            'professor_id': professor_id
        }
        cred = db.register(email, password, 'professors', user_config, professor_config)
        if not cred:
            return False

        print_success("Registered Successfully!")
        return True
    else:
        print_error('Please enter either "s" or "student" for student or "p" or "professor" for professor.')
        return False