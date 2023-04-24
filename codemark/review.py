import openai
import codemark.secrets
import codemark.utils
import re

"""
Model used : ChatGPT text-davinci-003
Currently the review system, only gives only first I/O case to CHATGPT
This is solely done to reduce chances of accessing hidden I/O's.
Chances that program code will be shown in code is minimal but not zero
"""


speaker_remove = re.compile(r"^[a-zA-Z]+[:]", re.MULTILINE)
EXTENSION = "c"
openai.api_key = codemark.secrets.api_key

def reviewCode():
    programCode = codemark.utils.smartGetCode()

    assignment_info = codemark.utils.readJSONFile("config.json")
    
    # If some error occured while getting program Code
    if isinstance(programCode, int) or assignment_info is None:
        if assignment_info is None:
            print("Did you used `codemark get <ASSIGNMENT-CODE>` before reviewing it?")
        return
    
    questionTitle = assignment_info['title']
    questionDescription = assignment_info['description']
    input = []
    output = []

    test_cases = assignment_info['test_cases']

    for test_case in test_cases:
        input.append(test_cases[test_case]['input'])
        output.append(test_cases[test_case]['output'])

    expectedInput = input[0]
    expectedOutput = output[0]
    extension = EXTENSION

    response_report = generate_query_and_response(programCode,  questionTitle, questionDescription, expectedInput, expectedOutput, extension)
    if response_report:
        print("\n\n" + response_report)
     


def generate_query_and_response(programCode, questionTitle, questionDescription, expectedInput, expectedOutput, extension="c"):
    query = "Review the following code given below, written in {5}."\
            " But, in no way you have to give the correct answer or program code in part or in full."\
            " Don't start with something like Answer: or ChatGPT: or Solution: etc, just plain solution."\
            " Check for any compile time as well possible runtime errors."\
            " Also, check for Logical error based on question statement."\
            " As well recommend better algorithm to improve the code, but don't give the program code in part or full, just the explanation only."\
            "\n\nProgram Code to be reviewed: \n\n{0}\n\n\nQuestion: \n\n{1}\n\n{2}\n\nExpected Input:\n\n{3}\n\nExpected Output:\n\n{4}".format(programCode, questionTitle, questionDescription, expectedInput, expectedOutput, extension)
    
    response_text = response(query)
    if response_text:
        return "RESPONSE\n\n" + speaker_remove.sub("", response_text).strip().replace("\n\n", "\n").replace(". ", ".\n\n")
    else:
        return


#TODO: Handle no internet issues
def response(query):
    prompt=query
    model_engine = "text-davinci-003"
    try:
        completion=openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer=completion.choices[0].text
        return answer.strip()
    except openai.error.APIConnectionError:
        print("ERROR: Network is unreachable.")
        return

