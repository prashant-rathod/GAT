import numpy as np
import pysal

from GSA import Regionalization


# independent can be n x j np.array where j is the number of independent variables
# dependent is n x 1 np.array
# TODO figure out what to return

def optionsDecider(dependent, independent, w, gwk=None, endogeneous=None, instrument=None):
    dependent.shape = (len(dependent), 1)
    independent = independent.transpose()
    if endogeneous != None:
        endogeneous = endogeneous.transpose()
    if instrument != None:
        instrument = instrument.transpose()
    spatial = (w != None)
    robust = 'white' if (gwk == None) else 'hac'
    return dependent, independent, spatial, robust, endogeneous, instrument


# non spatial ordinary least squares (with/without regimes)
def ols(dependent, independent, w=None, gwk=None, regime=False, regimes=None):
    dependent1, independent1, spatial, robust, foo, bar = optionsDecider(dependent, independent, w, gwk)
    if regime == False:
        ols = pysal.spreg.ols.OLS(y=dependent1, x=independent1, w=w, spat_diag=spatial, moran=spatial, robust=robust,
                                  gwk=gwk)
    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent)
        ols = pysal.spreg.ols_regimes.OLS_Regimes(y=dependent1, x=independent1, regimes=regimes, w=w,
                                                  spat_diag=spatial,
                                                  moran=spatial, robust=robust, gwk=gwk)

    # print(ols.summary)
    return ols.betas, ols.r2


# non spatial two stage least squares (with/without regimes)
def tsls(dependent, independent, endogeneous, instrument, w=None, gwk=None, regime=False, regimes=None):
    dependent1, independent1, spatial, robust, endogeneous1, instrument1 = optionsDecider(dependent, independent, w,
                                                                                          gwk)
    if regime == False:
        tsls = pysal.spreg.TSLS(dependent1, independent1, endogeneous1, instrument1, w=w, spat_diag=spatial,
                                robust=robust, gwk=gwk)
    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent, endogeneous, instrument)
        tsls = pysal.spreg.TSLS_Regimes(dependent1, independent1, endogeneous1, instrument1, regimes=regimes,
                                        spat_diag=spatial, robust=robust, gwk=gwk)

    return tsls.betas, tsls.pr2


# spatial least squares or spatial two stage least squares
# TODO: add regimes option-chapter 13
def gm(dependent, independent, w, endogeneous=None, instrument=None, gwk=None, regime=False, regimes=None):
    dependent1, independent1, spatial, robust, endogeneous1, instrument1 = optionsDecider(dependent, independent, w,
                                                                                          gwk=gwk,
                                                                                          endogeneous=endogeneous,
                                                                                          instrument=instrument)
    qlag = (endogeneous != None)
    if regime == False:
        reg = pysal.spreg.GM_Lag(dependent1, independent1, yend=endogeneous1, q=instrument1, lag_q=qlag,
                                 spat_diag=spatial, robust=robust, gwk=gwk)

    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent, endogeneous, instrument)
        reg = pysal.spreg.GM_Lag_Regimes(w=w, y=dependent1, x=independent1, yend=endogeneous1, q=instrument1,
                                         regimes=regimes, lag_q=qlag, spat_diag=spatial, robust=robust, gwk=gwk)

    return reg.betas, reg.pr2

    # maximum likelihood model


def ml(dependent, independent, w, regime=False, regimes=None):
    dependent1, independent1, spatial, foo1, foo2, foo3 = optionsDecider(dependent, independent, w)

    if regime == False:
        reg = pysal.spreg.ML_Lag(y=dependent1, x=independent1, w=w, method='ord', spat_diag=spatial)
    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent)
        reg = pysal.spreg.ML_Lag_Regimes(y=dependent1, x=independent1, w=w, regimes=regimes, method='ord',
                                         spat_diag=spatial)

    return reg.betas, reg.pr2


def gmError(dependent, independent, w, regime=False, regimes=None):
    dependent1, independent1, foo0, foo1, foo2, foo3 = optionsDecider(dependent, independent, w)

    if regime == False:
        reg = pysal.spreg.GM_Error_Het(y=dependent1, x=independent1, w=w, )
    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent)
        reg = pysal.spreg.GM_Error_Het_Regimes(w=w, y=dependent1, x=independent1, regimes=regimes)

    return reg.betas, reg.pr2


#
def gmErrorEnd(dependent, independent, w, endogeneous, instrument, regime=False, regimes=None):
    dependent1, independent1, foo1, foo2, endogeneous1, instrument1 = optionsDecider(dependent, independent, w,
                                                                                     endogeneous=endogeneous,
                                                                                     instrument=instrument)

    if regime == False:
        reg = pysal.spreg.GM_Endog_Error_Het(y=dependent1, x=independent1, yend=endogeneous1, q=instrument1)
    else:
        if regimes == None:
            regimes = Regionalization.generateRegimes(w, dependent, independent, endogeneous, instrument)
        reg = pysal.spreg.GM_Endog_Error_Het_Regimes(y=dependent1, x=independent1, yend=endogeneous1, q=instrument1,
                                                     regimes=regimes)

    return reg.betas, reg.pr2


def gmCombo(dependent, independent, w, endogeneous, instrument, regime=False, regimes=None):
    dependent1, independent1, foo1, foo2, endogeneous1, instrument1 = optionsDecider(dependent, independent, w,
                                                                                     endogeneous=endogeneous,
                                                                                     instrument=instrument)
    qlag = (endogeneous != None)
    if regime == False:
        reg = pysal.spreg.GM_Combo_Het(y=dependent1, x=independent1, w=w, yend=endogeneous1, q=instrument1, lag_q=qlag)
    else:
        if regimes == None:
            retimes = Regionalization.generateRegimes(w, dependent, independent, endogeneous, instrument)
        reg = pysal.spreg.GM_Combo_Het_Regimes(y=dependent1, x=independent1, w=w, yend=endogeneous1, q=instrument1,
                                               lag_q=qlag, regimes=regimes)

    return reg.betas, reg.pr2


def predict(betas, cur):
    if len(betas[1:]) != len(cur):
        betas = betas[:-1]
    return np.sum(betas[1:] * cur) + betas[0]
