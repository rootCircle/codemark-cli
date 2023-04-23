import os
import subprocess
import codemark.utils
# from fuzzywuzzy import fuzz

def checkCode():
    print("Checking Code......")
    print("Checks the code based on cached assignment code fetched from a file")

    filename = codemark.utils.smartGetFileName()

    if not filename:
        return
    
    compileCCode(filename)


def compileCCode(filename):


    # Define the input and expected output strings
    input_str = '5\n'
    expected_output_str = 'The factorial of 5 is 120\n'

    # Compile the C file
    try:
        # filename[:-2] trims out extension
        subprocess.check_output(['gcc', filename, '-o', filename[:-2]])
    except subprocess.CalledProcessError:
        print('Compilation error')
        exit()

def match_io():
    # Run the program with the input string
    try:
        output = subprocess.check_output(['./main'], input=input_str.encode())
    except subprocess.CalledProcessError:
        print('Execution error')
        exit()

    # Perform fuzzy matching on the output string
    match_score = fuzz.ratio(output.decode(), expected_output_str)
    print(f'Match score: {match_score}')
    if match_score > 80: # set a threshold for the match score
        print('Output matches expected output')
        match = True
    else:
        print('Output does not match expected output')
        match = False

def check_io(input_str, output_str):
    pass