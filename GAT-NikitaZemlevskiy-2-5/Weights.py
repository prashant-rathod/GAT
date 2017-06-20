import pysal

'''
Makes weights object from shapefile or from input data. This is basically an adjacency matrix (unweighted or weighed) of a graph representing
the locations on a map

Parameters:
shapeFilePath - path to shapefile
weights - Dictionary. the weights of each entity with respect to each neighbor. Keys can be strings or numbers, but weights must be positive real numbers.
    If no weights are supplied weights are determined from the shapefile
kind - String. Which kind of weights desired. Can be queen, rook, knn, or band
binary - Boolean. If distance band weights are picked (kind = band), picks whether binary distance band or continuous distance band.s
'''
def generateWeightsUsingShapefile(shapeFilePath, weights=None, kind="queen", k=None, binary=False):
    # use weights from shapefile for purely geographic
    w = None
    if weights == None:
        if kind == "queen":
            w = pysal.queen_from_shapefile(shapeFilePath)
        if kind == "rook":
            w = pysal.rook_from_shapefile(shapeFilePath)
        if kind == "knn" and type(k) == int:
            w = pysal.knnW_from_shapefile(shapefile=shapeFilePath, k=k)
        if kind == "band":
            threshold = pysal.min_threshold_dist_from_shapefile(shapeFilePath)
            if binary == True:
                w = pysal.threshold_binaryW_from_shapefile(shapefile=shapeFilePath, threshold=threshold)
            else:
                w = pysal.threshold_continuousW_from_shapefile(shapefile=shapeFilePath, threshold=threshold)
        if kind == "kernel":
            w = pysal.adaptive_kernelW_from_shapefile(shapeFilePath, diagonal=True, k=5)

    # else use user defined weights to create "space" instead of "place"
    else:
        if kind == "rook":
            w = pysal.rook_from_shapefile(shapeFilePath)
        if kind == "knn":
            w = pysal.knnW_from_shapefile(shapeFilePath, k = k)
        else:
            w = pysal.queen_from_shapefile(shapeFilePath)
        neighbors = w.neighbor_offsets
        w = pysal.W(neighbors, weights=weights)

    # row standardize the matrix. better to do it here and use it somewhere else.
    w.transform = 'r'
    return w

'''
Generate w object from scratch with used defined neighbors and weights between them. Can be used for counterfactual experiments.

Parameters:
neighbors - Dictionary. Defines what ares are next to what areas.
weiths - Dictionary. Defines what weight the connection between one area and another have. If none, all ones will be used.
'''
def generateWeightsFromScratch(neighbors, weights=None):
    w = None
    if weights == None:
        w = pysal.w(neighbors)
    else:
        w = pysal.W(neighbors, weights=weights)

    # row standardize the matrix. better to do it here and use it somewhere else.
    w.transform = 'r'
    return w

'''
Extract specified observations from a csv file.

Parameters:
csvobspath - String. Path to csv file.
rows - String or List. "ALL" if all rows desired. Otherwise list of desired rows.
cols - String or List. "ALL" if all cols desired. Otherwise list of desired cols.

'''
def extractObservations(csvobspath, rows, cols):
    import numpy as np
    observations = []
    csvobs = pysal.open(csvobspath, "r")
    colsRet = []
    if cols == "ALL":
        observations = np.array([csvobs.by_col[x] for x in csvobs.header])
        #print(observations)
        colsRet = csvobs.header
    else:
        observations = np.array([csvobs.by_col[i] for i in cols])
        colsRet = cols

    if rows != "ALL":
        row0 = [row[0] for row in csvobs.by_row]
        keys = {row0[i]: i for i in range(0, len(row0))}

        for col in range(0, len(observations)):
            observations[col] = [observations[col][keys[x]] if x in rows else None for x in row0]

    csvobs.close()
    return np.array(observations)#, colsRet
