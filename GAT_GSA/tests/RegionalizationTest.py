import pysal
import numpy as np
import Weights
#import random
from pysal.region import Random_Region
f = pysal.open(pysal.examples.get_path("usjoin.csv"))
print(f.header)
#print("TEST1")
pci = np.array([f.by_col[str(y)] for y in range(1929, 2010)])
#pci = np.array([f.by_col(str(1929))])
#print(pci)
pci1 = Weights.extractObservations(pysal.examples.get_path("usjoin.csv"), rows="ALL", cols = [str(y) for y in range(1929,2010)])
print(pci)
print(pci1)
pci = pci.transpose()

w = pysal.open(pysal.examples.get_path("states48.gal")).read()

np.random.seed(100)
#random.seed(10)
r = pysal.Maxp(w, pci, floor = 5, floor_variable = np.ones((48, 1)), initial = 99)
'''
names = f.by_col('Name')
names = np.array(names)
#for region in r.regions:
#    for x in region:
#        print(names[int(x)])
#    print("")
regions = r.regions
order = w.id_order
print(order)
for region in regions:
    for area in region:
        area = order[int(area)]
print("REGIONS", regions)
a = [0]*48
for i in range(0, len(regions)):
    for area in regions[i]:
        a[int(area)] = i
print(a)
#print(r.pvalue)
r.inference()
print(r.pvalue)

#random regions - make random regions based on 3 constraints: cardinality, contiguity and # or regions.
#                  contiguity through spatial weights matrix w
np.random.seed(100)
ids = w.id_order
t0 = Random_Region(area_ids=ids, cardinality=None, contiguity=None, num_regions=None)
#print(t0.regions)
np.random.seed(100)
#t0 = Random_Region(ids, num_regions=8, cardinality=[2, 2, 2, 2, 2, 2, 2, 2])
numRegs = 8
minAreas = 2
cardinalities = []
sum = 0
np.random.seed(100)
print(len(ids))
'''
'''for i in range(0, numRegs - 1):
    print("Low", minAreas, "HIGH", len(ids) - sum - minAreas, "SUM", sum)
    cur = np.random.randint(minAreas, high=len(ids) - sum - minAreas)
    sum += cur
    cardinalities.append(cur)
    print(np.sum(cardinalities), "TEST", len(cardinalities))
    #print(cur)
    #print("cur", cur, "Low", minAreas, "HIGH", len(ids) - sum - minAreas, "SUM", sum)
'''
'''a=[]
while np.sum(a)!=len(ids):# and len(set(a))!=numRegs:
    a=[np.random.randint(minAreas, len(ids)) for i in range(numRegs)]
print(a)
#cardinalities = np.array(a)

print(np.sum(cardinalities), "TEST")
t0 = Random_Region(ids, num_regions=8, cardinality=cardinalities)
print(t0.regions)
'''
#print(list(np.ones(5)))