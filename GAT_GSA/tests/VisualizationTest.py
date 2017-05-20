import shapefile as shp
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import pysal
import numpy as np
#import kartograph

np.set_printoptions(threshold=np.inf)

sf = shp.Reader("us_income/us48.shp")

# need to figure out why there is a line in some spots.
# get rid of different colors.
'''
plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y)
#plt.show()
'''
#neighbors = {0: [3, 1], 1: [0, 4, 2], 2: [1, 5], 3: [0, 6, 4], 4: [1, 3, 7, 5], 5: [2, 4, 6, 8], 6: [3, 5, 7], 7: [4, 6, 8], 8: [5, 7]}
#weights = {0: [1, 1], 1: [1, 1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 1, 1, 1], 5: [1, 1, 1, 1], 6: [1, 1, 1], 7: [1, 1, 1], 8: [1, 1]}
#w = pysal.W(neighbors, weights)

w = pysal.queen_from_shapefile("us_income/us48.shp")
#observations = [10, 20, 30, 40, 50, 60, 70, 80, 90]
full, ids = w.full()
print(full)
connections = []
for x in range(0, len(full)):
    for y in range(0, len(full[x])):
        if full[x][y] != 0:
            connections.append([x, y])

print(connections)
#print(connections)
'''graph = nx.Graph()
graph.add_edges_from(connections)
#print(len(pysal.weights.get_points_array_from_shapefile("us_income/us48.shp")))'''
coordinates = pysal.weights.get_points_array_from_shapefile("us_income/us48.shp")
print(coordinates.tolist())
'''
nx.draw_networkx(graph, coordinates, node_size=300)
#nx.draw_networkx(graph, node_size=300)
plt.show()
'''
#for
'''
edgelist = [(u,v,(u+v)%2) for u,v in itertools.product(range(3),range(3,6))]
G = nx.Graph()
for u,v,t in edgelist:
    G.add_edge(u,v,attr_dict={'t':t})
ecolors = tuple('g' if G[u][v]['t'] == 1 else 'm' for u,v in G.edges())
nx.draw_networkx(G,node_color='rrrccc',edge_color=ecolors)
plt.show()
'''
'''
np.random.seed(1234)
pos = np.random.rand(10, 2) #coordinates, (x, y) for 10 nodes
print(pos)
connect = [tuple(np.random.random_integers(0, 9, size=(2))) for x in range(8)] #random connections
print(connect)
#creation of the graph
graph = nx.Graph()
#adding nodes/connections in the graph
for node in range(10):
    graph.add_node(node)
graph.add_edges_from(connect)

#plot of the nodes using the (x,y) pairs as coordinates
nx.draw(graph, pos, node_size=50)
plt.show()

'''