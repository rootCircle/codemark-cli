import os
import subprocess
import codemark.utils as cmutils
from fuzzywuzzy import fuzz
import re
import sys
import psutil
import threading


"""
match_io function has three modes : exact match, regex match, fuzzy match
# By default only regex match is enabled, but can be modified using functional arguments


TODO : Add option to prof to write regex to match output by themselves, can be implemented in match_io easily
"""

limit_memory = 256 * 1024 * 1024  # 256 MB in bytes
limit_time = 180 # 3 minutes in seconds
MAX_CHECK_CODE = 3 # Maximum codes to be checked
FUZZY_MATCH_THRESHOLD = 80 # Threshold when doing fuzzy matching
MEMORY_EXCEEDED = False # Keeps tracks of memory exceeding in Windows only, not for POSIX

def set_limits():
    process = psutil.Process()
    process.rlimit(psutil.RLIMIT_DATA, (limit_memory, limit_memory))

def check_memory_limit_win(pid, limit, process):
    """
    Since we can check by default in POSIX systems, this function is implemented for windows only
    This function runs in a separate process and monitors the memory usage of the specified process.
    If the memory usage exceeds the specified limit, it terminates the process and prints a message.
    """
    while True:
        try:
            process_memory = psutil.Process(pid).memory_info().rss
            if process_memory > limit:
                process.terminate()
                cmutils.print_warning("Process terminated due to exceeding memory limit.")
                break
        except psutil.NoSuchProcess:
            # The process has already exited, so we can stop monitoring its memory usage.
            break

def checkCode(byPassMAXCheck = False):
    cmutils.print_info("Checking Code......")
    cmutils.print_info("Checking the code based on cached assignment code fetched from a file\n")

    filename = cmutils.smartGetFileName()

    if not filename or filename in (-1, -2):
        return False

    compileCCode(filename)
    
    config_info = cmutils.readJSONFile("config.json")
    if not config_info:
        return
    
    test_cases = config_info['test_cases'].values()
    counter = 0
    success = 0
    final = True

    print()

    for test_case in test_cases:
        result = match_io(filename, test_case["input"], test_case["output"], matchType = config_info['match_type'])
        final = final and result
        cmutils.print_message("Match {} {}".format(counter + 1, "passed successfully!" if result else "failed"))
        counter+=1
        if (counter == MAX_CHECK_CODE  or not result) and not byPassMAXCheck:
            break
        if result:
            success += 1
    
    if final:
        cmutils.print_success("\nAll tests passed successfully!")
    elif not byPassMAXCheck:
        # Called from submit
        cmutils.print_message("\nSome test cases failed. Retry harder!")
    elif byPassMAXCheck:
        cmutils.print_message("\n{} of {} test passed!\n".format(success, counter))

    if not byPassMAXCheck:
        return final
    
    return (success, counter)


def compileCCode(filename):
    # Compile the C file
    try:
        # filename[:-2] trims out extension
        subprocess.check_output(['gcc', filename, '-o', filename[:-2]])
    except subprocess.CalledProcessError:
        cmutils.print_error('Compilation error')
        sys.exit()
    

def match_io(file, input_str, output_str, matchType = "regex"):
    """
    Match type
    1. Exact Match
    2. Fuzzy Match with 80 % threshold
    3. Regex Match
    """
    print()
    cmutils.print_info("Matching output using " + matchType + " match algorithm.")

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
        # Hotfix for preexec_fn support on Windows, Memory limit check is not supported on windows
        if os.name == "nt":
            globals()['MEMORY_EXCEEDED'] = False
            with subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
                # Using daemon may have unexpected effects 
                # See this for info : https://stackoverflow.com/questions/20596918/python-exception-in-thread-thread-1-most-likely-raised-during-interpreter-shutd/20598791#20598791
                thread = threading.Thread(target=check_memory_limit_win, args=(process.pid, limit_memory, process), daemon=True)
                thread.start()
    
                output, _ = process.communicate(input=input_str.encode(), timeout=limit_time)
                thread.join() # Wait for the memory monitoring thread to stop
                
                if MEMORY_EXCEEDED:
                    sys.exit() # In case of memory limit is breached
        else:
            # For POSIX system
            # We don't require multithreading in this case
            result = subprocess.run(run_command, input=input_str.encode() ,stdout=subprocess.PIPE, preexec_fn=set_limits, timeout=limit_time)
            output = result.stdout
    except subprocess.CalledProcessError:
        cmutils.print_error('Execution error')
        sys.exit()
    except subprocess.TimeoutExpired:
        cmutils.print_error("TIMEOUT: Codes takes more than {} seconds to execute.".format(limit_time))
        sys.exit()
    

    matchType = matchType.lower()

    if matchType == "fuzzy":
        return fuzzyMatching(output, output_str)
    elif matchType == "regex":
        return regexIOMatching(output_str, output.decode())
    
    # Matches to matchType == "exact"
    return output.decode() == output_str

def fuzzyMatching(output, output_str):
    # Perform fuzzy matching on the output string
    match_score = fuzz.ratio(output.decode(), output_str)
    cmutils.print_message(f'Fuzzy Match score: {match_score}')
    if match_score > FUZZY_MATCH_THRESHOLD: # set a threshold for the match score
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