import os
import json

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
        print("ERROR: More than one file found!")
        return -1 
    elif len(matchingFiles) == 0:
        print("ERROR: No {} files found!".format(extension))
        return -2
    print("INFO: Found {} file in root file!".format(matchingFiles[0]))
    return getProgramCode(matchingFiles[0])

def smartGetFileName(extension="c"):
    matchingFiles = detectFile(extension)

    if len(matchingFiles) > 1:
        print("ERROR: More than one file found!")
        return -1 
    elif len(matchingFiles) == 0:
        print("ERROR: No {} files found!".format(extension))
        return -2
    print("INFO: Found {} file in root file!".format(matchingFiles[0]))
    return matchingFiles[0]

def makeDirectory(directory):
    try:
        # Create target Directory
        os.mkdir(directory)
        return True
    except FileExistsError:
        print("ERROR: Directory ", directory, " already exists.")
        return False


def writeToFile(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def writeJSONToFile(filename, content):
    # Open a file in write mode
    with open(filename, 'w') as f:

        # Write the dictionary to the file in JSON format
        json.dump(content, f, indent=4)

def readJSONFile(filename):
    try:
        with open(filename, 'r') as f:

            # Load the JSON data from the file into a dictionary
            my_dict = json.load(f)

        return my_dict
    except FileNotFoundError as e:
        print("No", filename, "file found!")