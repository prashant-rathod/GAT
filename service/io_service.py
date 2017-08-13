import tempfile
import os

# the following few store helper methods are used to store user-uploaded files
# tempfile is a python package
# essentially what we're doing is copying their uploaded data to a randomly named folder or filename which is how we store it on the server
# then we use these folders and files to do our analysis
# some of the storing has to be done in a specialized manner, which is the reason for the storeNLP and storeGSA methods
def storefile(inFile, tempdir):
    if inFile.filename == '':
        return
    suffix = '.' + inFile.filename.split('.')[-1]
    f = tempfile.NamedTemporaryFile(
            dir=tempdir,
            suffix=suffix,
            delete=False)
    inFile.save(f)
    return f.name

def storeNLP(file_list, tempdir):
    if file_list[0].filename == '':
        return
    source_dir = tempfile.mkdtemp(dir=tempdir) + '/'
    for f in file_list:
        f.save(source_dir + f.filename)
    # this line is necessary because of how AWS creates default permissions for newly created files and folders
    os.chmod(source_dir, 0o755)
    return source_dir

def storeGSA(file_list, tempdir):
    #saves everything but only returns the shapefile. Nice
    if file_list[0].filename == '':
        return
    source_dir = tempfile.mkdtemp(dir=tempdir) + '/'
    shapefile = None
    for f in file_list:
        f.save(source_dir + f.filename)
        if f.filename.endswith(".shp"):
            shapefile = source_dir + f.filename
    #see previous comment
    os.chmod(source_dir, 0o755)
    return shapefile