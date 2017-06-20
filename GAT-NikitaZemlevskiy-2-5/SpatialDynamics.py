import pysal
import numpy as np

# TODO test all three functions more.
# TODO do doc

# observations can be of the form np.array([['b','a','c'],['c','c','a'],['c','b','c'],['a','a','b'],['a','b','c']])
# method = regular, spatial, lisa.
# TODO: extract relevant statistics and decide which numbers to include in the return.
# transition counts, transition probabilities, steady state distributions, mean passage times
def markov(observations, w=None, numQuints=5, method="regular"):
    result = None
    s = None
    if method == "regular":  # non spatial analysis
        quintiles = np.array([pysal.Quantiles(y, k=numQuints).yb for y in observations]).transpose()
        result = pysal.Markov(quintiles)
        s = result.steady_state

    else:
        observations = observations.transpose()

        if method == "spatial":
            # standardize observations for smoother calculations:
            observations = observations / (observations.mean(axis=0))
            result = pysal.Spatial_Markov(observations, w, fixed=True, k=numQuints)
            s = result.S

        else:  # method == lisa
            result = pysal.LISA_Markov(observations, w)
            s = result.steady_state

    return result.transitions, result.p, s, result.stpysal.ergodic.fmpt(result.p)


# TODO: extract relevant statistics and decide which numbers to include in the return.
def rank(observations, w=None, regimes=None, method="tau"):
    originalObs = observations
    observations = observations.transpose()
    w = None
    a = None
    if regimes == None:  # generate regimes endogeneously.
        import Regionalization
        #TODO fix double transpose issue. fixed
        a = Regionalization.generateRegimes(w, originalObs)
        w = pysal.block_weights(a)
    else:  # regimes provided by user.
        w = pysal.block_weights(regimes)
    if method == "tau":
        result = [pysal.SpatialTau(observations[:, i], observations[:, i + 1], w, 100) for i in
                  range(0, len(w.id_order))]
        ret = [(r.tau_spatial, r.taus.mean(), r.tau_spatial_psim) for r in result]

    else:  # method == "theta"
        if regimes == None:
            result = pysal.Theta(regime=a, y=observations)
        else:
            result = pysal.Theta(regime=regimes, y=observations)
        ret = [(r.theta, r.pvalue_left, r.pvalue_right) for r in result]
    return ret


# when you have a set of observations, each on different location, and each with a different timestamp associated with it
# example data set could be homicides and their location and time of occurrence.
# observations can be counts of occurrences.
# Should not be called with data like amount of money spent, etc. Will be useless.
def interaction(locations, times, observations=None, method="modifiedKnox", delta=20, tau=5):
    result = None
    if observations != None:
        for i in range(0, len(observations)):
            if observations[i] > 1:
                locations.append([locations[i]] * (observations[i]))
                times.append([times[i]] * (observations[i]))

    if method == "modifiedKnox":
        result = pysal.spatial_dynamics.interaction.modified_knox(locations, times, delta=delta, tau=tau)
    if method == "knox":
        result = pysal.spatial_dynamics.interaction.knox(locations, times, delta=delta, tau=tau)

    return result["stat"], result["pvalue"]
