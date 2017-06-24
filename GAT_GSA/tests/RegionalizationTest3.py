import Regionalization
import Weights
import numpy as np
import pysal

#This is how it is done in GSA.py under the regionalization app route
w = Weights.generateWeightsUsingShapefile("us48.shp", idVariable="STATE_NAME")
def testObs():
    observations = Weights.extractObservations("usjoin.csv", "ALL", list(range(1979, 2009)))
    regions = Regionalization.generateRegions(w=w, observations=observations)[0]
    regions = Regionalization.getNamesFromRegions(regions)
    print(regions)

#Regions should be roughly the same - may be different because of randomness. but should be roughly the same each time
testObs()
testObs()
testObs()
