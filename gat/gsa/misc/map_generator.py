import subprocess

'''
src is path to shapefile uploaded
proj is projection.
'''
def generateMap(src, outfile, proj="mercator"):
	subprocess.call('python2.7 GAT_GSA/python2.7kartograph_test.py -source ' +   src + " -proj " + proj + " -outfile " + outfile, shell=True)
