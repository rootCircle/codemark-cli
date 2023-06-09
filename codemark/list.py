import codemark.account
import codemark.firebase.database as FireDB
from tabulate import tabulate
import textwrap as twp
from codemark.utils import print_error, print_message, print_warning

db = FireDB.FirebaseDB()

def listSmart(submitted, pending):
    assignments = listAssignments(submitted, pending)
    if assignments:
        if not submitted:
            for assignment in assignments:
                del assignment['test_cases']
                del assignment['batch_id']
                assignment['description'] = twp.fill(assignment['description'], 50)
                assignment['title'] = twp.fill(assignment['title'], 20)

        else:
            for assignment in assignments:
                del assignment['cid']
                del assignment['code_url']
                del assignment['student_id']

        print_message(tabulate(assignments, headers="keys", tablefmt="fancy_grid", 
               numalign="center", stralign="center"))

def listAssignments(submitted, pending):
    assignment = getAllAssignment()

    if assignment is None:
        return
    
    if not assignment:
        print_message("No Assignments found! Relax")
        return
    
    if submitted:
        return getSubmitted()
    elif pending:
        return getPending()
    return assignment

def getPending():
    assignments = getAllAssignment()
    submitted_assignments = getSubmitted(printto=False)
    pending = [item for item in assignments if item['assignment_id'] not in [submitted_assignment['assignment_id'] for submitted_assignment in submitted_assignments]]
    if not pending:
        print_message("No Pending Assignment! What a relief!")
    return pending  


def getSubmitted(printto=True):
    student_id = codemark.account.getCurrentStudentID()
    if not student_id:
        print_error("O o....Somes issues\nRun codemark doctor for resolving")
        return
    assignments = db.getdataOrderEqual("submissions", "student_id", student_id)

    if assignments is None:
        print_error("Some error occurred, while fetching assignments")
        return

    if not assignments and printto:
        print_warning("Nothing here yet!")

    return list(assignments.values())

def getAllAssignment():
    batch_id = codemark.account.getBatchID()
    if not batch_id:
        print_error("O o....Somes issues\nRun codemark doctor for resolving")
        return
    assignments = db.getdataOrderEqual("assignments", "batch_id", batch_id)

    if assignments is None:
        print_error("Some error occurred, while fetching assignments")
        return

    return list(assignments.values())


