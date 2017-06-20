import pysal
import numpy as np

'''
Replaces a missing observation with observations with average (weighted or unweighted) or median of the spatially neighboring observations.
Observations that are already present are left unaltered

Parameters:
observations- List. list of observations ordered in same way as w.id_order.
w - pysal weights object
kind - String. average if simple average is desired. weightedAverage if spatially weighted average is desired. median if median is desired

Returns original set of observations with missing ones filled in and a list of the locations at which the observations were missing.

Examples:
neighbors = {0: [3, 1], 1: [0, 4, 2], 2: [1, 5], 3: [0, 6, 4], 4: [1, 3, 7, 5], 5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}
weights = {0: [1, 1], 1: [1, 1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 1, 1, 1], 5: [1, 1, 1], 6: [1, 1], 7: [1, 1, 1], 8: [1, 1]}
observations = [3.0, 3.0, 3.0, 3.0, 3.0, None, 3.0, 3.0, None]
observations at locations 5 and 8 will be replaced with the average of the neighbors to which they are connected.
w = pysal.W(neighbors, weights)
print(replaceMissing(observations, w)[0])
([3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0])

neighbors = {'a': ['b'], 'b': ['a', 'c'], 'c': ['b']}
weights = {'a': [1], 'b': [1, 1], 'c': [1]}
observations = [1, None, 1]
w = pysal.W(neighbors, weights)
print(replaceMissing(observations, w)[0])
[1, 1.0, 1]
'''


def replaceMissing(observations, w, kind="average"):
    observationstemp = [np.nan if x is None else x for x in observations]
    full, ids = w.full()
    nans = np.where(np.isnan(observationstemp))
    nans = list(nans[0])
    cards = w.cardinalities
    order = w.id_order
    cards = {i: cards[order[i]] for i in range(0, len(order))} #convert in the case where ids in w are strings

    if kind.contains("average") or kind.contains("Average"):
        for nan in nans:
            row = list(full[nan])
            numnans = 0
            curtotal = 0
            for i in range(0, len(row)):
                curw = row[i]
                if curw != 0:
                    if kind == "average": curw = 1
                    if np.isnan(observationstemp[i]):
                        numnans += 1
                    else:
                        curtotal += observationstemp[i] * curw
            avg = curtotal / (cards[nan] - numnans)
            observationstemp[nan] = avg

    else:  # kind == median
        for nan in nans:
            row = list(full[nan])
            neighborObs = []
            for i in len(row):
                if row[i] != 0:
                    neighborObs += observations[i]
            observationstemp[nan] = np.median(neighborObs)

    locations = [ids[x] for x in nans]  # return places where observations were missing and were filled
    return observationstemp, locations

'''
If there is a suspicion that the data may be have abnormalities, apply smoothing to smooth out the data before doing analysis.
Observations shouldn't have any nans in it.

Returns list of observations smoothed by the requested methods and parameters.

Parameters:
observations - List. List of observations in the same order as w.id_order
w - pysal weights object.
kind - String. mean or median depending on what smoothing method is desired.
iterations - int. if median smoothing specified can iterate over data to smooth more and more.

'''
def smooth(observations, w, whole=None, kind="mean", iterations=1):
    sm = pysal.esda.smoothing
    if whole==None: whole = np.ones(len(observations))
    result = []
    if kind == "mean":
        result = sm.Disk_Smoother(observations, whole, w)
    else: #kind == median
        result = sm.Spatial_Median_Rate(observations, whole, w, iteration=iterations)
    return result

