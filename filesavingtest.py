import tempfile
import shutil
tempdir = 'static/temp/'

def storefile(inFile):
	suffix = '.' + inFile.split('.')[-1]
	f = tempfile.NamedTemporaryFile(
            dir=tempdir,
            suffix=suffix,
            delete=False)
	shutil.copyfile(inFile, f.name)
	return f.name

print(storefile('trumpspeech.txt'))