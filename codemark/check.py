import os
import subprocess
import codemark.utils
from fuzzywuzzy import fuzz
import re
import resource

limit_memory = 256 * 1024 * 1024  # 256 MB in bytes
limit_time = 180 # 3 minutes in seconds
MAX_CHECK_CODE = 3 # Maximum codes to be checked

# match_io function has three modes : exact match, regex match, fuzzy match
# By default only regex match is enabled, but can be modified using functional arguments

def set_limits():
    # Set the memory limit
    resource.setrlimit(resource.RLIMIT_AS, (limit_memory, limit_memory))

    # Set the time limit
    resource.setrlimit(resource.RLIMIT_CPU, (limit_time, limit_time))


def checkCode(byPassMAXCheck = False):
    print("Checking Code......")
    print("Checks the code based on cached assignment code fetched from a file\n")

    filename = codemark.utils.smartGetFileName()

    if not filename or filename in (-1, -2):
        return False

    compileCCode(filename)
    
    test_cases = codemark.utils.readJSONFile("config.json")
    if not test_cases:
        return
    
    test_cases = test_cases['test_cases'].values()
    counter = 0
    success = 0
    final = True

    print()

    for test_case in test_cases:
        result = match_io(filename, test_case["input"], test_case["output"], regexMatch=True)
        final = final and result
        print("Match {} {}".format(counter + 1, "passed successfully!" if result else "failed"))
        counter+=1
        if (counter == MAX_CHECK_CODE  or not result) and not byPassMAXCheck:
            break
        if result:
            success += 1
    
    if final:
        print("\n\nAll tests passed successfully!")
    else:
        print("\n\nSome test cases failed. Retry harder!")
        
    if not byPassMAXCheck:
        return final
    else:
        return (success, counter)


def compileCCode(filename):
    # Compile the C file
    try:
        # filename[:-2] trims out extension
        subprocess.check_output(['gcc', filename, '-o', filename[:-2]])
    except subprocess.CalledProcessError:
        print('ERROR: Compilation error')
        exit()
    

def match_io(file, input_str, output_str, fuzzy_match=False, regexMatch=False):
    """
    Fuzzy match will take priority over regex Match
    """
    # Run the program with the input string
    executable_file = file[:-2]
    if os.name == "nt":
    # Windows platform
        executable_file += ".exe"  # add the .exe extension for Windows
        run_command = [executable_file]  # no need to prefix with './' on Windows
    else:
        # Linux platform
        run_command = ["./" + executable_file]  # prefix with './' on Linux
    try:
        output = subprocess.check_output(run_command, input=input_str.encode(), preexec_fn=set_limits)
    except subprocess.CalledProcessError:
        print('ERROR: Execution error')
        exit()


    if fuzzy_match:
       return fuzzyMatching(output, output_str)
    elif regexMatch:
        return regexIOMatching(output_str, output.decode())
    else:
        return output.decode() == output_str

def fuzzyMatching(output, output_str):
     # Perform fuzzy matching on the output string
        match_score = fuzz.ratio(output.decode(), output_str)
        print(f'Fuzzy Match score: {match_score}')
        if match_score > 80: # set a threshold for the match score
            match = True
        else:
            match = False
        return match

def regexIOMatching(output, output_str):
    pattern = ""

    output.replace('\n',' ')
    output.replace('\t', ' ')

    for i in output.split(" "):
        pattern += ".*" + i

    pattern += ".*"
    patternIOMatch = re.compile(pattern, re.MULTILINE | re.DOTALL)

    # Search for the pattern in the target string
    match = patternIOMatch.search(output_str)

    return bool(match)