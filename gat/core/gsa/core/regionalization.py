import pysal
import numpy as np

'''
Spatially constrained clustering. Can impose the constraint of using observations (meaningful) or randomly generate regions.
    Three constraints are avaliable for random regions - contiguity, cardinality, and number of regions. Any combination of these can be turned on or off

Parameters:
w - Pysal w object. Must be binary contiguity matrix. w defines n areas. These areas will be broken into p regions with
    at least nimAreas areas in each region.
observations - List. List of observations if maxp method is selected.
minAreas - int. Minimum areas per region. For random region generation this defines the areas per region.
method - String. "maxp" if observations supplied. "random" if random regions desired
contiguity - Boolean. True is contiguity enforced for random region generation. Will use w as contiguity matrix
numRegs - int. Defines the number of regions to create for random region generation.
compact - Boolean. If true tries to create compact regions for random region generation.
'''


def generateRegions(w, observations=None, minAreas=5, maxp=True, contiguity=False, numRegs=None, compact=False):
    if maxp == True:
        observations = observations.transpose()
        l = len(observations)
        fv = np.ones(l)
        r = pysal.Maxp(w, observations, floor=minAreas, floor_variable=fv, initial=99)
        r.inference()
        regions = r.regions
        order = w.id_order

        return regions, r.pvalue

    else:  # maxp == False
        from pysal.region import Random_Region
        ids = w.id_order
        regions = None

        cardinalities = []
        while np.sum(cardinalities) != len(ids):  # and len(set(cardinalities))!=numRegs:
            cardinalities = [np.random.randint(minAreas, len(ids)) for i in range(numRegs)]

        if contiguity == False:
            regions = Random_Region(area_ids=ids, num_regions=numRegs, cardinality=cardinalities, compact=compact)
        else:
            regions = Random_Region(area_ids=ids, num_regions=numRegs, cardinality=cardinalities, contiguity=w,
                                    compact=compact)

        return regions, None


# TODO fix comparison to none not just here but everywhere else.
def generateRegimes(w, observations1, observations2=None, observations3=None, observations4=None, observations5=None):
    local = locals()
    observations = np.array(observations1)

    for key, value in local.items():
        if isinstance(value, np.ndarray) and key != 'observations1' and value != None:
            observations = np.append(observations, value, axis=0)

    # observations = observations.transpose() #re check double transpose issue
    regions = generateRegions(w, observations, maxp=True)[0]
    a = [0] * len([item for sublist in regions for item in sublist])

    for i in range(0, len(regions)):
        for area in regions[i]:
            a[int(area)] = i

    return a


def getNamesFromRegions(regions):
    return {r: t for t in range(0, len(regions)) for r in regions[t]}
