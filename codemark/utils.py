import os
import json
from termcolor import colored

def detectFile(extension="c"):
    matchingFiles = []
    for file in os.listdir():
        if file.endswith(".{}".format(extension)):
            matchingFiles.append(file)
    return matchingFiles

def getProgramCode(filename):
    code = ""
    with open(filename, "r") as f:
        code += f.read()
    return code

def smartGetCode(extension="c"):
    matchingFiles = detectFile(extension)

    if len(matchingFiles) > 1:
        print_error("More than one file found!")
        return -1 
    elif len(matchingFiles) == 0:
        print_error("No {} files found!".format(extension))
        return -2
    print_success("Found {} file in current directory!".format(matchingFiles[0]))
    return getProgramCode(matchingFiles[0])

def smartGetFileName(extension="c"):
    matchingFiles = detectFile(extension)

    if len(matchingFiles) > 1:
        print_error("More than one file found!")
        return -1 
    elif len(matchingFiles) == 0:
        print_error("No {} files found!".format(extension))
        return -2

    print_success("Found {} file in current directory!".format(matchingFiles[0]))
    return matchingFiles[0]

def makeDirectory(directory):
    try:
        # Create target Directory
        os.mkdir(directory)
        return True
    except FileExistsError:
        print_error("Directory " + directory + " already exists.")
        return False


def writeToFile(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
        file.flush()

def writeJSONToFile(filename, content):
    # Open a file in write mode
    with open(filename, 'w') as f:

        # Write the dictionary to the file in JSON format
        json.dump(content, f, indent=4)

        f.flush()

def readJSONFile(filename):
    try:
        with open(filename, 'r') as f:

            # Load the JSON data from the file into a dictionary
            my_dict = json.load(f)

        return my_dict
    except FileNotFoundError:
        print_error("No " + filename + " file found!")



def print_info(message, prefix = True):
    if prefix:
        message = "[INFO] " + message
    print(colored(message, "blue"))

def print_success(message, prefix = True):
    if prefix:
        message = "[SUCCESS] " + message
    print(colored(message, "green", attrs=["bold"]))


def print_warning(message, prefix = True):
    if prefix:
        message = "[WARNING] " + message
    print(colored(message, "yellow"))

def print_error(message, prefix = True):
    if prefix:
        message = "[ERROR] " + message
    print(colored(message, "red", attrs=["bold"]))

def print_message(message):
    print(colored(message, "cyan", attrs=["bold"]))