import pysal


# can extract more info from following objects, right now returns pseudo p-value and calculated statistic and expected value of statistic
# where applicable.

def localAutocorrelation(observations, w):
    return geary(observations, w)[0]

def globalAutocorrelation(observations, w):
    return moran(observations, w)[0]

def joinCountAutocorrelation(observations, w):
    j = pysal.Join_Counts(w=w, y=observations)
    return j.bb, j.yy


def gamma(observations, w):  # general case
    g = pysal.Gamma(observations, w, standardize='yes')

    return g.p_sim_g, g.g


def moran(observations, w):  # global
    m = pysal.Moran(observations, w, two_tailed='False')

    return m.p_sim, m.I, m.EI


def geary(observations, w):  # more sensitive to local
    g = pysal.Geary(observations, w)

    return g.p_sim, g.C, g.EC


def moranLocal(observations, w):
    m = pysal.Moran_Local(observations, w)

    return m.p_sim.mean(), m.Is, m.EI_sim


'''
examples: (must have usjoin.csv and us48.shp, us48.shx, us48.dbf in the same directory or point to them while opening them)
#create the weights matrix and extract the observations:
similarity, w = generateWeights("us_income/us48.shp", "us_income/usjoin.csv", "All", "2009")
#generate pvalue, statistic value, and statistic expected value:
m = moran(similarity, w)
#print out results
print(m)

'''
