import pysal
import numpy as np
'''
#regular markov
f = pysal.open(pysal.examples.get_path("usjoin.csv"), "r")
pci = np.array([f.by_col[str(y)] for y in range(1929,2010)])
q5 = np.array([pysal.Quantiles(y, k=4).yb for y in pci]).transpose()#uses 5 by default

m5 = pysal.Markov(q5)
print("transitions")
print(m5.transitions)
print(m5.p)
print(m5.steady_state)
print("CLASSES", m5.classes)
#mean passage time
print("mean passage time non spatial")
print(pysal.ergodic.fmpt(m5.p)) #how long it takes to transition (here how long it takes a state in each quintile to go to each quintile)

#spatial markov
w = pysal.open(pysal.examples.get_path("states48.gal")).read()
w.transform = 'r'
pci = np.array([f.by_col[str(y)] for y in range(1929, 2010)])
pci = pci.transpose()
rpci = pci / (pci.mean(axis = 0))
print("RPCI", rpci)
sm = pysal.Spatial_Markov(rpci, w, fixed = True, k = 5)
print("conditional transition probabilities")
print(sm.p) #conditional transition probabilities
print("steady state probabilities")
print(sm.S) #steady state probabilities
print("mean passage time")
#mean passage time; 1st matrix = poor neighboorhood 1st row = poor state transition times
for f in sm.F:
    print(f)

np.set_printoptions(threshold=np.inf)

print(np.array([pysal.Quantiles(y, k=5).yb for y in pci]).transpose())

print("SPACE")

print(np.array([pysal.Quantiles(y, k=5).yb for y in pci.transpose()]))

dbf = pysal.open("/opt/anaconda3/pkgs/pysal-1.12.0-py35_0/lib/python3.5/site-packages/pysal/examples/burkitt/burkitt.dbf")
print(len(dbf.by_col["T"]))'''
'''
f = pysal.open(pysal.examples.get_path("usjoin.csv"), "r")
pci = np.array([f.by_col[str(y)] for y in range(1929,2010)]).transpose()
w = pysal.open(pysal.examples.get_path("states48.gal")).read()
r = pysal.Maxp(w, pci, floor = 5, floor_variable = np.ones((48, 1)), initial = 99)
a = [0]*48
for i in range(0, len(r.regions)):
    for area in r.regions[i]:
        a[int(area)] = i
w = pysal.block_weights(a)
res = [pysal.SpatialTau(pci[:,i], pci[:,i+1], w, 99) for i in range(0, 48)]
for r in res:
    ev = r.taus.mean()
    print("%8.3f %8.3f %8.3f"%(r.tau_spatial, ev, r.tau_spatial_psim))
print(len(w.id_order))
'''
'''
f=pysal.open(pysal.examples.get_path("mexico.csv"))
vnames=["pcgdp%d"%dec for dec in range(1940,2010,10)]
y=np.transpose(np.array([f.by_col[v] for v in vnames]))
regime=np.array(f.by_col['esquivel99'])
w=pysal.weights.block_weights(regime)
np.random.seed(12345)
res=[pysal.SpatialTau(y[:,i],y[:,i+1],w,99) for i in range(6)]
for r in res:
    ev = r.taus.mean()
    print("%8.3f %8.3f %8.3f"%(r.tau_spatial, ev, r.tau_spatial_psim))
'''
'''
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a[:,1])'''
import SpatialDynamics, Weights
observations = Weights.extractObservations("/home/nikita/Projects/GAT/usjoin.csv", "ALL", list(range(1979, 2009)))
w = Weights.generateWeightsUsingShapefile("/home/nikita/Projects/GAT/us48.shp", idVariable="STATE_NAME")
result = SpatialDynamics.markov(observations, w, method="spatial")
print(result)