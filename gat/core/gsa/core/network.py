import pysal as ps
import shapefile
import numpy as np


def create_network(input1, input2):
    '''
    create a street network
    input files should have line object
    nodes are generated between on the intersection between lines
    see the example file for reference
    '''

    #ntw = ps.Network(ps.examples.get_path('streets.shp'))

    #ntw = ps.Network('mygeodata/streets.shp')
    ntw = ps.Network(input1)

    #print(ntw.node_list)
    #print(ntw.node_coords)

    '''W Object represents the binary adjacency of the network.'''
    w = ntw.contiguityweights(graph=False)

    '''edges are represented in this way: (0, 1), (0, 2), (1, 110)'''
    edges = w.neighbors.keys()

    #print(edges)

    '''feed the crimes data point into the network
    input files should have point object '''
    #ntw.snapobservations('mygeodata/crimes.shp', 'crimes', attribute=True)
    ntw.snapobservations(input2, 'crimes', attribute=True)

    '''get the number of crimes on each street'''
    counts = ntw.count_per_edge(ntw.pointpatterns['crimes'].obs_to_edge, graph=False)

    #print(counts)

    '''number of points to generate'''
    npts = ntw.pointpatterns['crimes'].npoints
    sim = ntw.simulate_observations(npts)

    #shp_path = '../misc/gsa_test/IRQ_adm1.shp'

    w = shapefile.Writer()
    w.field('STREET_ID', 'N')
    w.field('NUM_CRIMES', 'N')
    start = 1
    points = ntw.node_coords

    print(len(edges))

    for i in edges:

        count = counts.get(i)

        if count is not None:
            count = counts[i]
        else:
            count = 0

        origin = np.array(points[i[0]])
        dest = np.array(points[i[1]])

        w.line(parts=[[origin, dest]])

        w.record(start, count)
        start += 1

    #w.save('network/street_crimes')
    savePath = 'out/gsa/street_crimes'
    w.save(savePath)

    #print(w.shapes()[0].points)

    return savePath

'''
to visualize:
call map_generator.generate_map() <- pass in the correct shapefile you want to turn into an svg
python2.7 gat/core/gsa/misc/python2.7kartograph_test.py -source /Users/fanggedeng/Downloads/GSA/geodanet/crimes.shp -proj mercator -outfile mesa.svg
'''
