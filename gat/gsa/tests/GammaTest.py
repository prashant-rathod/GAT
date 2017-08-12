import pysal
import numpy as np

'''
csv = pysal.open(pysal.examples.get_path("usjoin.csv"))
w = pysal.rook_from_shapefile(pysal.examples.get_path("us48.shp"))
incomes = dict()
i = 0
while (i < 48):
    line = csv.read(1)
    #print(line[1])
    array = line[0]
    #print(array[0])
    incomes[array[0]] = np.mean([x for x in array[2:(2009-1929)]])
    i += 1


#print(incomes)
keys = sorted(incomes.keys())
print(keys)
array = []
for key in keys:
    #print(incomes[key])
    array.append(incomes[key])
array1 = np.ndarray((len(array), len(array)))
print(array1)
f = pysal.open(pysal.examples.get_path("us48.dbf"))
#print(f.header)

#cross product, ##cross product with self yeilds self
for i in range(0, len(array)):
    for j in range(0, len(array)):
        if i != j:
            array1[i][j] = array[i]*array[j]
        #else:
         #   array1[i][j] = array[i]
g = pysal.Gamma(array, w)
#print(w.full())
print(g.p_sim_g)
print(g.g_z)
'''
w = pysal.queen_from_shapefile("us_income/us48.shp")
w1 = pysal.rook_from_shapefile("us_income/us48.shp")

print(w.neighbor_offsets,"\n", w1.neighbor_offsets)
'''
print(array1)
g = pysal.Gamma(array1, w)
print("p_sim_g:")
print(g.p_sim_g)
#gc = pysal.Geary(array1, w)
mi = pysal.Moran(array1, w)
#print("gc")
#print(gc.p_sim)
#print(gc.EC)
print("mi")
print(mi.p_sim)
print(mi.EI)
'''
#coordinates:: print(pysal.weights.get_points_array_from_shapefile(shapefilepath))
#test


'''similarity, w = generateWeights("us_income/us48.shp", "us_income/usjoin.csv", "All", "2009")
g = gamma(similarity, w)
m = moran(similarity, w)
ge = geary(similarity, w)
print(g, m, ge)
g = pysal.Moran_Local(similarity, w)
#print(g.p_sim.mean())
#(0.28100000000000003, 0.57139265339558643) (0.037418055539430693, -0.02127659574468085, 0.23899999999999999, 0.65070840158891985) (0.17799999999999999, -0.93088252317912579, 0.9071630959061564, 1.0)
#0.270854166667
#test fillempty
#[ 0.,  1.,  0.],
#[ 1.,  0.,  1.],
#[ 0.,  1.,  0.]
#w.ids = [first, second, third]'''

neighbors = {0: [3, 1], 1: [0, 4, 2], 2: [1, 5], 3: [0, 6, 4], 4: [1, 3, 7, 5], 5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}
weights = {0: [1, 1], 1: [1, 1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 1, 1, 1], 5: [1, 1, 1], 6: [1, 1], 7: [1, 1, 1], 8: [1, 1]}
w = pysal.W(neighbors, weights)
print(w.neighbor_offsets)
'''
observations = [3.0, 3.0, 3.0, 3.0, 3.0, None, 3.0, 3.0, None]

print(fillEmpty(observations, w), "TEST")
#print(pysal.lag_spatial(w, observations))
'''

#np.set_printoptions(threshold=np.inf)
'''
##########################
#How to extract centroids from polygons:
#sids = pysal.open('../pysal/examples/sids2.shp', 'r')
#sids_d = np.array([i.centroid for i in sids])
'''