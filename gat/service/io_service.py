import os
import tempfile
import pickle

from gat.dao import dao

# the following few store helper methods are used to store user-uploaded files
# tempfile is a python package
# essentially what we're doing is copying their uploaded data to a randomly named folder or filename which is how we store it on the server
# then we use these folders and files to do our analysis
# some of the storing has to be done in a specialized manner, which is the reason for the storeNLP and storeGSA methods

# tempdir is the main folder where we store temporary data, like user-uploaded files
# this is the structure of the temp folder:
# static/temp/
# 			tmp1038412/
#			tmp123t24/
# 			and all other temporary folders
#
# a temporary folder is created for each new case
from gat.service import security_service

tempdir = 'out/generated/'


def storefile(inFile):
    if inFile is None or inFile.filename == '':
        return
    suffix = '.' + inFile.filename.split('.')[-1]
    f = tempfile.NamedTemporaryFile(
        dir=tempdir,
        suffix=suffix,
        delete=False)
    inFile.save(f)
    return f.name


def storeNLP(file_list):
    if len(file_list) == 0 or file_list[0].filename == '':
        return
    source_dir = tempfile.mkdtemp(dir=tempdir) + '/'
    for f in file_list:
        f.save(source_dir + f.filename)
    # this line is necessary because of how AWS creates default permissions for newly created files and folders
    os.chmod(source_dir, 0o755)
    return source_dir


def storeGSA(file_list):
    # saves everything but only returns the shapefile. Nice
    if len(file_list) == 0 or file_list[0].filename == '':
        return
    source_dir = tempfile.mkdtemp(dir=tempdir) + '/'
    shapefile = None
    for f in file_list:
        f.save(source_dir + f.filename)
        if f.filename.endswith(".shp"):
            shapefile = source_dir + f.filename
    # see previous comment
    os.chmod(source_dir, 0o755)
    return shapefile


def checkExtensions(case_num):
    errors = []
    fileDict = dao.getFileDict(case_num)
    gsa_csv_file = fileDict['GSA_Input_CSV']
    if gsa_csv_file != None:
        if not gsa_csv_file.endswith('.csv'):
            errors.append("Error: please upload csv file for GSA.")

    gsa_file_list = fileDict['GSA_file_list']
    exts = ['.shp', '.shx', '.dbf']
    if gsa_file_list is not None and len(gsa_file_list) > 0 and gsa_file_list[0].filename != '':
        for ext in exts:
            ext_in = False
            for f in gsa_file_list:
                if f.filename.endswith(ext):
                    ext_in = True
            if not ext_in:
                errors.append("Error: please upload shp, shx, and dbf file for GSA.")
                break

    sna_file = fileDict['SNA_Input']
    if sna_file != None:
        if not sna_file.endswith(('.xls', '.xlsx')):
            errors.append("Error: please upload xls OR xlsx file for SNA.")

    nlp_file = fileDict['NLP_Input_LDP']
    # terms = fileDict.get('NLP_LDP_terms')
    # if nlp_file != None:
    #    if not nlp_file.endswith('.txt'):
    #        errors.append("Error: please upload txt file for NLP Lexical Dispersion Plot.")

    sentiment_file = fileDict["NLP_Input_Sentiment"]
    if sentiment_file != None:
        if not sentiment_file.endswith('.txt'):
            errors.append("Error: please upload txt file for Sentiment Analysis.")

    return errors


def storeFiles(case_num, email=None, files = None):
    tempDir ='out/generated/' if email is None else 'data/' + str(security_service.getData(email)[0]) + '/'
    #TODO: save files

    fileDict = dao.getFileDict(case_num)

    fileDict['GSA_Input_CSV'] = storefile(files.get('GSA_Input_CSV'))
    fileDict['GSA_Input_SHP'] = storeGSA(files.getlist('GSA_Input_map'))
    fileDict['NLP_Input_corpus'] = storeNLP(files.getlist('NLP_Input_corpus'))
    fileDict['NLP_Input_LDP'] = storefile(files.get('NLP_Input_LDP'))
    fileDict['NLP_Input_Sentiment'] = storefile(files.get('NLP_Input_Sentiment'))


    fileDict['SNA_Input'] = storefile(files.get('SNA_Input'))
    fileDict['GSA_Input'] = storefile(files.get('GSA_Input'))
    if email is not None:

        with open(tempDir + 'fileDict.pickle', 'wb+') as file:
            pickle.dump(fileDict, file, protocol=pickle.HIGHEST_PROTOCOL)

def loadDict(uidpk):
    with open('data/' + str(uidpk) + 'fileDict.pickle', 'rb') as file:
        dao.setFileDict(pickle.load(file), case_num)