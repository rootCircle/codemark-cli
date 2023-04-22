import openai
import codemark.secrets
import codemark.utils
import re

speaker_remove = re.compile(r"^[a-zA-Z]+[:]", re.MULTILINE)

openai.api_key = codemark.secrets.api_key

def reviewCode():
    programCode = codemark.utils.smartGetCode()
    
    # If some error occured while getting program Code
    if isinstance(programCode, int):
       return

    print(generate_query_and_response(programCode, "Find sum of two numbers", "Print sum of two numbers", "2 3", "5"))
     


def generate_query_and_response(programCode, questionTitle, questionDescription, expectedInput, expectedOutput, extension="c"):
    query = "Review the following code given below, written in {5}. But, in no way you have to give the correct answer. Don't start with something like Answer: or ChatGPT: or Solution: etc, just plain solution."\
            "Check for any compile time as well possible runtime errors."\
            " Logical error based on question statement. As well recommend better algorithm to improve the code what don't give the corrected code."\
            "\n\nProgram Code: \n\n{0}\n\n\nQuestion: \n\n{1}\n\n{2}\n\nExpected Input:\n\n{3}\n\nExpected Output:\n\n{4}".format(programCode, questionTitle, questionDescription, expectedInput, expectedOutput, extension)
    
    response_text = response(query)
    return "RESPONSE: " + speaker_remove.sub("", response_text).strip().replace("\n\n", "\n")

def response(query):
    prompt=query
    model_engine = "text-davinci-003"
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

