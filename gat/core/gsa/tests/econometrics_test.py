import pysal
import numpy as np

db = pysal.open(pysal.examples.get_path('columbus.dbf'), 'r')

hoval = db.by_col("HOVAL")
y = np.array([db.by_col("HOVAL")])
#print(len(hoval), len(y))
#y.shape = (len(hoval), 1)
#y = y.transpose()

X = []
X.append(db.by_col("INC"))
X.append(db.by_col("CRIME"))
#X = np.array(X).transpose()

#X = np.append(X, y, axis=1)
#np.column_stack([X, y])
#print(X)
#def test(a, b, c):
#    d = locals()
#    return a + b + c, d
#print(test(1, 2, 3))

w = pysal.weights.rook_from_shapefile(pysal.examples.get_path("columbus.shp"))
gwk = pysal.adaptive_kernelW_from_shapefile(pysal.examples.get_path("columbus.shp"))
import Regionalization
#X = np.append(X, y, axis=1)
#X.transpose()
#Regionalization.generateRegions(w, observations=y)
regimes = Regionalization.generateRegimes(w, X, y)
#print(regimes, len(regimes))

X = np.array(X).transpose()
y.shape = (len(hoval), 1)
#print(len(X), len(y))
olsr = pysal.spreg.OLS_Regimes(y, X, w=w, regimes=regimes)
print([olsr.multi[i].betas for i in range(0, len(olsr.multi))])
#ols = pysal.spreg.ols.OLS(y, X, w, spat_diag=True, moran=True, name_y='home value', name_x=['income', 'crime'], name_ds='columbus',gwk=gwk, robust='hac')
#ols2 = pysal.spreg.ols.OLS(y, X, w, spat_diag=True, moran=True, name_y='home value', name_x=['income', 'crime'], name_ds='columbus')
'''

#svobs = pysal.open(pysal.examples.get_path("usjoin.csv"), "r")
#print(csvobs.header)
#print(ols2.summary)
#print(ols.summary)

test1 = open("./test1", mode='w+')
test1.write(ols.summary)
test2 = open("./test2", mode='w+')
test2.write(ols2.summary)
test1.close()
test2.close()

import difflib
d = difflib.Differ()
from pprint import pprint
pprint(list(d.compare(ols2.summary, ols.summary)))
'''
#print(ols.betas)
#[[ 46.42818268]
# [  0.62898397]
# [ -0.48488854]]
#constant [[ 15.17070179]
#income [  1.61847804]]
'''
[[  323   600   310 ...,   460   673   675]
 [  267   520   228 ...,   408   588   585]
 [  224   429   215 ...,   356   469   476]
 ...,
 [31988 33470 31070 ..., 29769 35839 43453]
 [32819 33445 31800 ..., 31265 36594 45177]
 [32274 32077 31493 ..., 31843 35676 42504]]
'''