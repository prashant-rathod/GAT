import os
import tempfile

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
