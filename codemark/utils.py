import os

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
        print("More than one file found!")
        return -1 
    elif len(matchingFiles) == 0:
        print("No {} files found!".format(extension))
        return -2
    print("Found {} file in root file!".format(matchingFiles[0]))
    return getProgramCode(matchingFiles[0])

