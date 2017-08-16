import networkx as nx
import random
import numpy as np
import scipy as sp

def averagePathRes(cliques_found, ta=20, iters=5):
    scaledResilienceDict = {}
    toScale = []
    cliques, selected = cliques_found
    # Find resilience of subgraphs
    for clique in cliques:
        initShortestPath = nx.average_shortest_path_length(clique)
        t0 = 0
        finShortestPathList = []

        # function to estimate integral
        def integral(x0, x1, rectangles):
            width = (float(x1) - float(x0)) / rectangles
            sum1 = 0
            for i in range(rectangles):
                height = qw_shortestPath * (float(x0) + i * width)
                area = height * width
                sum1 += area
            return sum1

        # creating perturbation by removing random 10% of nodes and averaging result of x iterations
        for k in range(0, iters):  # x can be changed here
            G = clique.copy()
            nList = G.nodes()
            nNumber = G.number_of_nodes()
            sample = int(nNumber * 0.1)  # percent of nodes removed can be changed here
            rSample = random.sample(nList, sample)
            G.remove_nodes_from(rSample)
            # finding shortest path of largest subgraph in G after perturbation:
            # (average shortest path cannot be calculated if a graph has unconnected nodes)
            l = []
            for g in nx.connected_component_subgraphs(G):
                l.append(len(g.edges()))
                if len(g.edges()) == max(l) and len(g.edges()) != 0:
                    finShortestPathList.append(nx.average_shortest_path_length(g, weight='Salience'))
        # find mean of average shortest path from each iteration:
        finShortestPath = np.mean(finShortestPathList)
        # solve for resilience using integral function:
        qw_shortestPath = float(finShortestPath) / float(initShortestPath)
        t1 = t0 + ta
        resilience = integral(t0, t1, 5) / t1
        # add to list: resilience measure for each clique
        toScale.append(resilience)
    # scale resilience measures on a normal scale
    for i in range(len(cliques)):
        # scaledResilienceDict[cliques[i].nodes()[0]] = sp.stats.percentileofscore(toScale,toScale[i])
        scaledResilienceDict[selected[i]] = sp.stats.percentileofscore(toScale, toScale[i])
    return scaledResilienceDict


# Resilience function based on Laplacian Spectrum of G:
def laplacianRes(cliques_found, ta=20, iters=5, ):
    toScale = []
    scaledResilienceDict = {}
    cliques, selected = cliques_found
    for clique in cliques:
        t0 = 0
        index_0 = np.mean(nx.laplacian_spectrum(clique))
        index_1List = []

        # function to estimate integral
        def integral(x0, x1, rectangles):
            width = (float(x1) - float(x0)) / rectangles
            sum1 = 0
            for i in range(rectangles):
                height = qw_shortestPath * (float(x0) + i * width)
                area = height * width
                sum1 += area
            return sum1

        # creating perturbation by removing random 10% of nodes and averaging result of x iterations
        for k in range(0, iters):  # x can be changed here
            G = clique.copy()
            nList = nx.nodes(G)
            nNumber = nx.number_of_nodes(G)
            sample = int(nNumber * 0.1)  # percent of nodes removed can be changed here:
            rSample = random.sample(nList, sample)
            G.remove_nodes_from(rSample)
            index_1List.append(np.mean(nx.laplacian_spectrum(G)))
        # find mean of Laplacian spectra from each iteration:
        index_1 = np.mean(index_1List)
        # solve for resilience using integral function:
        qw_shortestPath = float(index_1) / float(index_0)
        qw_shortestScale = 1

        # function to create baseline resilience to scale measure from 0:1:
        def integralScale(x0, x1, rectangles):
            width = (float(x1) - float(x0)) / rectangles
            sum1 = 0
            for i in range(rectangles):
                height = qw_shortestScale * (float(x0) + i * width)
                area = height * width
                sum1 += area
            return sum1

        # Calculating Laplacian Resilience:
        t1 = t0 + ta
        resilience = integral(t0, t1, 50) / t1
        baseResilience = integralScale(t0, t1, 50) / t1
        scaledResilience = resilience / baseResilience
        toScale.append(scaledResilience)
    # scale resilience measures on a normal scale
    for i in range(len(cliques)):
        # scaledResilienceDict[cliques[i].nodes()[0]] = sp.stats.percentileofscore(toScale,toScale[i])
        scaledResilienceDict[selected[i]] = sp.stats.percentileofscore(toScale, toScale[i])
    return scaledResilienceDict
