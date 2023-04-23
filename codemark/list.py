import codemark.account
import codemark.firebase.database as FireDB
from tabulate import tabulate


db = FireDB.FirebaseDB()

def listSmart(completed, pending):
    assignments = listAssignments(completed, pending)
    if assignments:
        if not completed:
            for assignment in assignments:
                del assignment['test_cases']
                del assignment['batch_id']
        print(tabulate(assignments, headers="keys", tablefmt="fancy_grid", 
               numalign="center", stralign="center"))

def listAssignments(completed, pending):
    assignment = getAllAssignment()

    if assignment is None:
        return
    
    if not assignment:
        print("No Assignments found! Relax")
        return
    
    if completed:
        return getCompleted()
    elif pending:
        return getPending()
    else:
        return assignment

def getPending():
    assignments = getAllAssignment()
    completed_assignments = getCompleted(printto=False)
    pending = [item for item in assignments if item['assignment_id'] not in [completed_assignment['assignment_id'] for completed_assignment in completed_assignments]]
    if not pending:
        print("No Pending Assignment! What a relief!")
    return pending  


def getCompleted(printto=True):
    student_id = codemark.account.getCurrentStudentID()
    if not student_id:
        print("O o....Somes issues\nRun codemark doctor for resolving")
        return
    assignments = db.getdataOrderEqual("submissions", "student_id", student_id)

    if assignments is None:
        print("Some error occurred, while fetching assignments")
        return

    if not assignments and printto:
        print("Nothing here yet!")

    return list(assignments.values())

def getAllAssignment():
    batch_id = codemark.account.getBatchID()
    if not batch_id:
        print("O o....Somes issues\nRun codemark doctor for resolving")
        return
    assignments = db.getdataOrderEqual("assignments", "batch_id", batch_id)

    if assignments is None:
        print("Some error occurred, while fetching assignments")
        return

    return list(assignments.values())


