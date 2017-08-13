import Regionalization
import Weights
import pysal
import numpy as np
import json
np.set_printoptions(threshold=np.nan)
f = pysal.open(pysal.examples.get_path("usjoin.csv"))
#print("TEST1")
pci = np.array([f.by_col[str(y)] for y in range(1929, 2009)])
#pci = np.array([f.by_col(str(1929))])
#print(pci)
w = pysal.open(pysal.examples.get_path("states48.gal")).read()


w = Weights.generateWeightsUsingShapefile("us_income/us48.shp", kind="queen")
dbf = pysal.open("us_income/us48.dbf").header
print(dbf)
w = pysal.queen_from_shapefile("us_income/us48.shp", idVariable="STATE_NAME")


regions = Regionalization.generateRegions(w, observations=pci)[0]
'''names = np.array(f.by_col["Name"])
for i in range(0, len(regions)):
    for j in range(0, len(regions[i])):
        regions[i][j] = names[int(regions[i][j])]
d = {r : i for i in range(0, len(regions)) for r in regions[i]}'''
#{'Colorado': 0, 'Iowa': 7, 'Missouri': 3, 'Illinois': 7, 'Utah': 2, 'Tennessee': 5, 'Nebraska': 4, 'Wyoming': 0, 'Alabama': 2, 'Wisconsin': 7, 'Vermont': 6, 'Oklahoma': 2, 'Michigan': 7, 'Mississippi': 2, 'Arizona': 0, 'Delaware': 1, 'Virginia': 1, 'New Hampshire': 6, 'Ohio': 3, 'Pennsylvania': 3, 'Connecticut': 1, 'California': 0, 'New Mexico': 2, 'West Virginia': 3, 'North Carolina': 5, 'Montana': 4, 'Nevada': 0, 'North Dakota': 4, 'Maryland': 1, 'Massachusetts': 6, 'Idaho': 4, 'Louisiana': 2, 'Florida': 5, 'Rhode Island': 6, 'South Carolina': 5, 'Maine': 6, 'Washington': 0, 'Texas': 2, 'Arkansas': 2, 'Minnesota': 7, 'Indiana': 3, 'Kentucky': 3, 'New York': 1, 'New Jersey': 1, 'Kansas': 3, 'Georgia': 5, 'South Dakota': 4, 'Oregon': 0}

#print(d)
#regions = Regionalization.generateRegions(w, observations=pci)[0]
#for i in range(0, len(regions)):
#    for j in range(0, len(regions[i])):
#        regions[i][j] = names[int(regions[i][j])]
#d = {r : i for i in range(0, len(regions)) for r in regions[i]}
#d = {i: regions[i] for i in range(0, len(regions))}
d = {r : i for i in range(0, len(regions)) for r in regions[i]}
print(d)
#print(json.dumps(Regionalization.generateRegions(w, observations=pci)))
#print(Regionalization.generateRegions(w, observations=pci)[0])

#print(pci)
#pci.transpose()
#print(pci)
#r = pysal.Maxp(w, pci, floor = 5, floor_variable = np.ones((48, 1)), initial = 99)
#l = [1, 2, 3, 4, 5]
#print(l[:-1])
#l = np.array(l)
