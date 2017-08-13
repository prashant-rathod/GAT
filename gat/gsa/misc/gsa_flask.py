import csv
import json

import pysal
from GAT_GSA.GSA import Weights, Regionalization, SpatialDynamics
from flask import Flask, render_template

from gat.gsa.core import autocorrelation
from gat.gsa.misc import MapGenerator

app = Flask(__name__)

'''
Econometrics and smoothing modules are not included in here yet, but can do
'''

@app.route('/')
def index():
    gsaCSV = []
    # enter csv file uploaded here
    with open("usjoin.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gsaCSV.append(row)
    # need to render map automatically as well. need to call kartograph code here.

    MapGenerator.generateMap("us48.shp", "mymap.svg")

    # enter path to generated file here
    with open('mymap.svg', 'r') as myfile:
        data = myfile.read()

    data = data.replace('"', "'")

    shp = pysal.open('us48.shp', 'r')
    centers = [i.centroid for i in shp]
    print(centers)

    return render_template("kartograph-test.html",
                           gsaCSV=json.dumps(gsaCSV), mymap=json.dumps(data), centersPy=json.dumps(centers))

@app.route('/regionalization')
def regionalization():

    #enter csv file uploaded here and enter year inputted by user.
    #TODO: make it so all years are available to the regionalization code.

    #TODO:put in variable instead of path and instead of range.
    observations = Weights.extractObservations("usjoin.csv", "ALL", list(range(1979, 2009)))
    #or:
    #observations = Regionalization.extractObservations("usjoin.csv", "ALL", list(range(1929, 2009)) #can give range of years

    #TODO: put in variable name instead of "STATE_NAME" here
    w = Weights.generateWeightsUsingShapefile('us48.shp', idVariable="STATE_NAME")
    #w = pysal.open(pysal.examples.get_path("states48.gal")).read()

    regions = Regionalization.generateRegions(w=w, observations=observations)[0]
    regions = Regionalization.getNamesFromRegions(regions)

   #generate map automatically
    MapGenerator.generateMap("us48.shp")
    with open('mymap.svg', 'r') as myfile:
        data = myfile.read()

    data = data.replace('"', "'")
    '''
    shp = pysal.open('us48.shp', 'r')
    centers = [i.centroid for i in shp]'''


    return render_template("zoomtest.html",
                           mymap=json.dumps(data), regionsPy = json.dumps(regions))

@app.route('/autocorrelation')
def autocorrelation():
    #replace variables here as above.
    observations = Weights.extractObservations("usjoin.csv", "ALL", [2008])
    w = Weights.generateWeightsUsingShapefile("us48.shp", idVariable="STATE_NAME")
    globalAutocorrelation = autocorrelation.globalAutocorrelation(observations, w)
    localAutocorrelation = autocorrelation.localAutocorrelation(observations, w)
    print(globalAutocorrelation, localAutocorrelation)
    return str(globalAutocorrelation) + " " + str(localAutocorrelation)

def get_autocorrelation(csvfile, shpfile, year):
    observations = Weights.extractObservations(csvfile, "ALL", [year])
    w = Weights.generateWeightsUsingShapefile(shpfile, idVariable="STATE_NAME")
    globalAutocorrelation = autocorrelation.globalAutocorrelation(observations, w)
    localAutocorrelation = autocorrelation.localAutocorrelation(observations, w)
    print(globalAutocorrelation, localAutocorrelation)
    return str(globalAutocorrelation), str(localAutocorrelation)

@app.route('/spatialdynamics')
def spatialDynamics():
    #similarly, replace variables here as above
    observations = Weights.extractObservations("usjoin.csv", "ALL", list(range(1979, 2009)))
    w = Weights.generateWeightsUsingShapefile("us48.shp", idVariable="STATE_NAME")
    result = SpatialDynamics.markov(observations, w, method="spatial")
    return str(result)

if __name__ == "__main__":
    app.debug = True
    app.run()
