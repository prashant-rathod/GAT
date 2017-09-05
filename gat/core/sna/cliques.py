import networkx as nx
from gat.core.sna import resilience

# Make subgraphs from central nodes
def find_subgraph(G, centralNode, subGraph, depth):
    nodeList = [(centralNode, target) for target in G.neighbors(centralNode)]
    subGraph.add_edges_from(nodeList)
    if depth > 0:
        for ancillary in G.neighbors(centralNode):
            find_subgraph(G, ancillary, subGraph, depth - 1)

### Under development:

#import igraph as ig
#import louvain

# def louvain_method(graph):
#     G = graph.G.to_undirected()
#     #igraph = resilience.iGraphConversion(G)
#     ### Louvain Algorithm for Finding Best Partition ###
#     part = louvain.find_partition(igraph, method="Modularity")
#     part.significance = louvain.quality(G, part, method='Significance')


# def iGraphConversion(graph):
    # convert via edge list
    #igraph = ig.Graph(len(graph.G), zip(*zip(*nx.to_edgelist(graph.G))[:2]))
    # nx.to_edgelist(g) returns [(0, 1, {}), (0, 2, {}), ...], which is turned
    #  into [(0, 1), (0, 2), ...] for igraph
    #return igraph
