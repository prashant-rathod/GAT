############################## FILE RETRIEVAL ##############################

import os

# opens a file
def openFile(pathname):
    f = open(pathname, mode='r')
    try:
        raw = f.read()
    except UnicodeDecodeError:
        print('UnicodeDecodeError: ' + pathname)
        return ''
    return raw

# finds all txt files in the inputted directory and returns a list of their locations
def getFiles(path):
    pathnames = []
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        if file_list[i][-4:] == '.txt' or '.rtf':
            pathnames.append(os.path.join(path, file_list[i]))
    return pathnames

# finds all txt files in the inputted directory and returns a list of their locations (recurse one level)
def getFilesRecurse(path, fileType):
    pathnames = []
    file_list = os.listdir(path)
    for i in range(len(file_list)):
        if file_list[i][- len(fileType):] == fileType:
            pathnames.append(os.path.join(path, file_list[i]))
        elif os.path.isdir(path + '/' + file_list[i]):
            pathnames += getFiles(path + '/' + file_list[i])
    return pathnames

