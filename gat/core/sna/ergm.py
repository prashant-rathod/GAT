'''
Using PyMC for ERGM estimation
Tutorials from http://socialabstractions-blog.tumblr.com/post/53391947460/exponential-random-graph-models-in-python and https://gist.github.com/dmasad/78cb940de103edbee699
Author: Ryan Steed
10 July 2017
'''

from scipy.stats import logistic
from scipy.misc import comb
from itertools import product
import numpy as np
import pymc
import networkx as nx
import matplotlib.pyplot as plt
import os

def probability(G):
    params = calc_params(G)
    estimates = coef_estimate(matrix=nx.to_numpy_matrix(G),params=params,iters=3000)
    estimated_coefs, estimated_term_list = create_coefs(params=params,priors=estimates)
    return coefs_to_prob(term_list=estimated_term_list)

def calc_params(G):
    return {
        "density": edge_count(G),
        "block_match": node_match(G, "ontClass"),
        # 'deltaistar2': istarDelta(adjMat, 2),
        # 'deltaistar3': istarDelta(adjMat, 3),
        # 'deltaostar2': ostarDelta(adjMat, 2),
    }

def coef_estimate(matrix,params,iters):
    # using specified set of priors, create coefficients
    coefs, term_list = create_coefs(params=params, priors={coef: pymc.Normal(coef, 0, 0.001) for coef in params})

    @pymc.deterministic
    def probs(term_list=term_list):
        probs = 1 / (1 + np.exp(-1 * sum(term_list)))  # The logistic function
        probs[np.diag_indices_from(probs)] = 0
        # Manually cut off the top triangle:
        probs[np.triu_indices_from(probs)] = 0
        return probs

    # Fitting
    matrix[np.triu_indices_from(matrix)] = 0
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        try:
            outcome = pymc.Bernoulli("outcome", probs, value=matrix, observed=True)
            break
        except:
            print("Encountered zero probability error number",attempts,", trying again...")
            if attempts >= max_attempts:
                raise
            attempts += 1

    sim_outcome = pymc.Bernoulli("sim_outcome", probs)
    args = [outcome, sim_outcome, probs]
    # density_coef, density_term,
    # block_coef, block_term]
    for coef, info in coefs.items():
        # Add both coefficient and term for each coefficient
        for item in info:
            args.append(item)
    model = pymc.Model(args)
    mcmc = pymc.MCMC(model)
    mcmc.sample(iters, 1000, 50)  # approx. 30 seconds

    traces = diagnostics(coefs=coefs, mcmc=mcmc)

    goodness_of_fit(mcmc=mcmc)

    return {coef: np.mean(trace) for coef, trace in traces.items()}

## Service functions ##
def draw_init(G):
    draw_init(G)
    pos = nx.spring_layout(G, k=0.075, scale=4)
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=100, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    ax.set_xlim(-0.25, 4.25)
    ax.set_ylim(-0.25, 4.25)
    _ = ax.axis('off')
    save_ergm_file(fig, "originalGraph.png")  # print to file

def create_coefs(params, priors):
    coefDict = {}
    term_list = []
    args = []
    for coef,param in params.items():
        coefVal = priors.get(coef)
        term = coefVal * param
        # value is tuple which contains both coefficient and parameter term
        coefDict[coef] = (coefVal,term)
        term_list.append(term)
    return coefDict, term_list

def diagnostics(coefs, mcmc):
    trace = {}
    fig = plt.figure(figsize=(12, 6))
    i = 1
    for coef in coefs:
        trace[coef] = mcmc.trace(coef)[:]
        print(coef+": {0:.3f}, {1:.3f}".format(np.mean(trace[coef]), np.std(trace[coef])))
        ax = fig.add_subplot(220+i)
        ax.plot(trace[coef])
        ax.set_title(coef)
        i+=1
    save_ergm_file(fig, 'diagnostics')
    return trace

def goodness_of_fit(mcmc):
    # Goodness of fit viz
    realization = mcmc.trace("sim_outcome")[-1]  # Take the last one
    sim_g = nx.from_numpy_matrix(realization)
    pos = nx.spring_layout(sim_g, k=0.075, scale=4)
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw_networkx_nodes(sim_g, pos, node_size=100, ax=ax)
    nx.draw_networkx_edges(sim_g, pos, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(sim_g, pos, ax=ax)

    ax.set_xlim(-0.25, 4.25)
    ax.set_ylim(-0.25, 4.25)
    _ = ax.axis('off')
    save_ergm_file(fig, 'new')

def save_ergm_file(fig,name):
    dir = 'out/sna/ergm/'
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    fig.savefig(dir+name)

## Covariate methods ##
def edge_count(G):
    size = len(G)
    ones = np.ones((size, size))
    # Zero out the upper triangle:
    if not G.is_directed():
        ones[np.triu_indices_from(ones)] = 0
    return ones

def node_match(G, attrib):
    size = len(G)
    attribs = [node[1].get("block") for node in G.nodes(data=True)]
    match = np.zeros(shape=(size, size))
    for i in range(size):
        for j in range(size):
            if i != j and attribs[i] == attribs[j]:
                match[i, j] = 1
    if not G.is_directed():
        match[np.triu_indices_from(match)] = 0
    return match

# functions to get delta matrices
def istarDelta(am,k):
    if k == 1:
        # if k == 1 then this is just density
        res = np.ones(am.shape)
        return(res)
    res = np.zeros(am.shape,dtype=int)
    n = am.shape[0]
    for i,j in product(range(n),range(n)):
        if i!=j:
            nin = am[:,j].sum()-am[i,j]
            res[i,j] = comb(nin,k-1,exact=True)
    return(res)

def ostarDelta(am,k):
    if k == 1:
        # if k == 1 then this is just density
        res = np.ones(am.shape)
        return(res)
    res = np.zeros(am.shape,dtype=int)
    n = am.shape[0]
    for i,j in product(range(n),repeat=2):
        if i!=j:
            nin = am[i,:].sum()-am[i,j]
            res[i,j] = comb(nin,k-1,exact=True)
    return(res)

def coefs_to_prob(term_list):
    probs = 1 / (1 + np.exp(-1 * sum(term_list)))  # The logistic function
    probs[np.diag_indices_from(probs)] = 0
    return probs
