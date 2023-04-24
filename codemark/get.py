import codemark.firebase.database as FireDB
import codemark.utils
import os

# Default template for every new C files
C_CODE_TEMPLATE = "// Write your program here\n// For more help run `codemark --help`\n"


db = FireDB.FirebaseDB()

def fetch(assgn_code):
    if not fetch_and_download(assgn_code):
        print("Some Error Ocurred, while fetching and downloading file. Talk to Support for more details.")
        return
    print("Files fetched successfully!\n\nGo to", assgn_code, "directory.\n\nThen refer question.txt for question and other info\nRefer main.c to start coding.")

def fetch_and_download(assgn_code):
    print("Fetching files and resources!\n")

    assign_info = db.getdataOrderEqual("assignments", "assignment_id", assgn_code)
    
    if assign_info is None:
        return False

    if not assign_info:
        print("Enter valid Assignment Code or Retry after some time")
        return False
    
    assign_info = list(assign_info.values())[0]

    content = generateContent(assign_info)

    result = codemark.utils.makeDirectory(assgn_code)
    
    if not result:
        return False
    
    codemark.utils.writeToFile(os.path.join(assgn_code, "question.txt"), content)
    codemark.utils.writeToFile(os.path.join(assgn_code, "main.c"), C_CODE_TEMPLATE)
    codemark.utils.writeJSONToFile(os.path.join(assgn_code, "config.json"), assign_info)

    return True

def generateContent(assign_info):
    content = ""

    assgn_id = assign_info['assignment_id']
    content += "Assignment ID : " + assgn_id + "\n\n"

    title = assign_info['title']
    content += "Title : " + title.strip() + "\n"

    # Adds Title in description of question
    globals()['C_CODE_TEMPLATE'] += "// Title : " + title.replace('\n', ' ') + "\n\n"
    
    description = assign_info['description']
    content += "\nDescription\n\n" + description.strip() + "\n"

    # Adds description too
    # Description might be shown inaccurately in some cases
    globals()['C_CODE_TEMPLATE'] += "/* Description : \n" + description.replace("*/", "") + "*/\n\n" 

    due_date = assign_info['due_date']
    content += "\n\nDue Date : " + due_date + "\n"

    content += "==========I/O TESTS============" + "\n"

    input = []
    output = []

    test_cases = assign_info['test_cases']

    for test_case in test_cases:
        input.append(test_cases[test_case]['input'])
        output.append(test_cases[test_case]['output'])
    
    for i in range(len(input)):
        content += ">>>>>> TEST CASE " + str(i + 1)  + "\n"
        content += "Input\n" + input[i] + "\nOutput\n" + output[i] + "\n"

    globals()['C_CODE_TEMPLATE'] += "\n\n#include <stdio.h>\n\nint main(void)\n{\n\treturn 0;\n}\n"

    return content

