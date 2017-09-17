'''
Using PyMC for ERGM estimation
Tutorials from http://socialabstractions-blog.tumblr.com/post/53391947460/exponential-random-graph-models-in-python and https://gist.github.com/dmasad/78cb940de103edbee699
Author: Ryan Steed
10 July 2017
'''

import numpy as np
import pymc
import networkx as nx
import matplotlib.pyplot as plt
import csv

def walk(G,iters):

    pos = nx.spring_layout(G, k=0.075, scale=4)
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=100, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    ax.set_xlim(-0.25, 4.25)
    ax.set_ylim(-0.25, 4.25)
    _ = ax.axis('off')
    save_ergm_file(fig,"originalGraph.png") #print to file

    def edge_count(G):
        size = len(G)
        ones = np.ones((size, size))
        # Zero out the upper triangle:
        if not G.is_directed():
            ones[np.triu_indices_from(ones)] = 0
        return ones
    def node_match(G, attrib):
        size = len(G)
        attribs = [node[1][attrib] for node in G.nodes(data=True)]
        match = np.zeros(shape=(size, size))
        for i in range(size):
            for j in range(size):
                if i != j and attribs[i] == attribs[j]:
                    match[i, j] = 1
        if not G.is_directed():
            match[np.triu_indices_from(match)] = 0
        return match

    block_match_mat = node_match(G, "block")

    density_coef = pymc.Normal("density", 0, 0.001)
    block_coef = pymc.Normal("block_match", 0, 0.001)
    print(density_coef, block_coef, "created")
    print("# edges", edge_count(G))

    density_term = density_coef * edge_count(G)
    block_term = block_coef * block_match_mat

    term_list = [density_term, block_term]

    @pymc.deterministic
    def probs(term_list=term_list):
        probs = 1 / (1 + np.exp(-1 * sum(term_list))) # The logistic function
        probs[np.diag_indices_from(probs)] = 0
        # Manually cut off the top triangle:
        probs[np.triu_indices_from(probs)] = 0
        return probs

    # Get the adjacency matrix, and zero out the upper triangle
    matrix = nx.to_numpy_matrix(G)
    matrix[np.triu_indices_from(matrix)] = 0

    outcome = pymc.Bernoulli("outcome", probs, value=matrix, observed=True)

    sim_outcome = pymc.Bernoulli("sim_outcome", probs)

    #Fitting
    args = [outcome, sim_outcome, probs,
            density_coef, density_term,
            block_coef, block_term]
    print("MC MC Args:",args)
    model = pymc.Model(args)
    mcmc = pymc.MCMC(model)
    mcmc.sample(iters, 1000, 50) # approx. 30 seconds

    density_trace = mcmc.trace("density")[:]
    block_match_trace = mcmc.trace("block_match")[:]

    print("Density: {0:.3f}, {1:.3f}".format(np.mean(density_trace), np.std(density_trace)))
    print("Block: {0:.3f}, {1:.3f}".format(np.mean(block_match_trace), np.std(block_match_trace)))

    # Diagnostics
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(221)
    ax1.plot(density_trace)
    ax1.set_title("Density")
    ax2 = fig.add_subplot(222)
    ax2.hist(density_trace)
    ax2.set_title("Density")
    ax3 = fig.add_subplot(223)
    ax3.plot(block_match_trace)
    ax3.set_title("Block_Match")
    ax4 = fig.add_subplot(224)
    ax4.hist(block_match_trace)
    ax4.set_title("Block_Match")
    save_ergm_file(fig, 'diagnostics')

    #Goodness of fit viz
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
    save_ergm_file(fig,'new')


def save_ergm_file(fig,name):
    dir = 'out/sna/ergm/'
    fig.savefig(dir+name)


