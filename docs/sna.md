![LUCAS Logo](http://css-lucas.com/wp-content/uploads/2016/07/cropped-Lucas-Header-for-website.png)

# SNA Documentation
Last updated: January 15, 2017

## Contents

1. [Overview](#overview)
	1. [Requirements](#requirements)
	2. [Codebase](#codebase)
2. [Construction](#construction)
	1. [Parsing](#parsing)
	2. [Network](#network)
3. [Analysis](#analysis)
	1. [Measures](#measures)
	2. [Propensities](#propensities)
	3. [Communities](#communities)
	4. [ERGM](#ergm)
	5. [Resilience](#resilience)
4. [Forecasting](#forecasting)
	1. [Simple](#simple)
	2. [Smart](#smart)
5. [Utilities](#utilities)
6. [Future Features](#future-features)

## Overview

SNA is the social network analysis portion of Project Hermes 2.0. Its major features are as follows:

- constructs 2D and 3D networks based on Excel spreadsheet input from an analyst
- performs simple network analysis measures on a graph constructed using a sociology-based ontology of node classes
- performs more advanced, customized network analysis on resilience and influence community detection
- forecasts likely outcomes with stochastic probability model and psychology/political theory-based propensities model

### Requirements

SNA runs on Python 3.6.1 using the following core (non-util) packages:
- [matplotlib](https://matplotlib.org/)
- [networkx](https://networkx.github.io/documentation/networkx-1.10/index.html)
- [numpy](http://www.numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [scipy](https://www.scipy.org/)
- [python-louvain](https://pypi.python.org/pypi/python-louvain) (community)
- [pymc](https://pymc-devs.github.io/pymc/)

### Codebase

The core codebase for SNA is located at [`gat/core/sna/`](https://github.com/css-lucas/GAT/tree/master/gat/core/sna), and all subsequent path references will refer to this directory.

SNA is comprised of a main class object defined in `sna.py` and several helper library scripts. The following documentation will refer to library functions by attaching a Pythonic prefix (e.g. `cliques.louvain()` refers to the `louvain()` algorithm found in `cliques.py`). All other functions are SNA class methods (e.g. `python sna.__init__()`).

## Construction

The first stage of SNA parses an Excel sheet into a node list and an edge list. Each node is assigned an ontological class and attributes according to user data. A network is constructed using edges in the edge list.

### Parsing

`sna.__init__(excel_file, nodeSheet[, attrSheet])`
> On class instantiation, parses a list of nodes from a user-inputted Excel sheet and a list of attributes if provided to `SNA.list` and `SNA.attrList`, respectively (see also [excel_parser](#excel_parser)). Creates an empty directed NetworkX graph object (refer to [networkx](https://networkx.github.io/documentation/networkx-1.10/index.html) for documentation) at `SNA.G`. Also initializes several other class variables used in various methods, including lists of nodes, edges, and measure values. 
>
> *Arguments:*
- `excel_file`: a **string** with a path to an Excel file
- `nodeSheet`: a **string** with the name of the node sheet in that Excel file
- `attrSheet` (optional): a **string** with the name of the attribute sheet in that Excel file

#### `excel_parser`

The `excel_parser` library script provides methods for parsing the custom Excel templates used for SNA.

`excel_parser.readFile(subAttrs, excel_file, sheet)`
> Reads a specified sheet in an SNA Excel template and return the first row (without repeats) and a list of lists, each containing dictionaries for each cell. The dictionary has two keys: 'val', the value in that cell, and 'header', the column to which that cell belongs by column title. If there are subattributes (e.g. an attribute weight), these are not included in the list of column headers. 
>
> *Arguments:*
- `subAttrs`: a **list of strings** containing column headers that are subattributes
- `excel_file`: a **string** with the path to an SNA Excel template
- `sheet`: a **string** with the name of the sheet to parse)

`excel_parser.buildJSON(excel_file)`
> Creates a jsonifiable dictionary in which the keys are the last-parsed cell in the second column (parsing left to right, top to bottom) and the values are lists of dictionaries. Each dictionary represents a row, where the keys are column headers and the values are cell values corresponding to each header. Repeated headers are permitted but not expected. 
>
> *Arguments:*
- `excel_file`: a **string** path to an Excel document with a single sheet

### Network
`sna.createNodeList(nodeSet)`
> Using list of **node** sheet cells generated during [instantation](#parsing), adds nodes to `SNA.G` graph object with attribute 'block' equal to the node's header in the Excel sheet (see also [excel_parser](#excel_parser)). Only includes nodes in the user-selected columns specified by `nodeSet`, and excludes repeated node names. 
>
> *Arguments:*
- `nodeSet`: a **list** of the node columns to include in the network by column header

`sna.loadAttributes()`
> Using list of **attribute** sheet cells generated during [instantation](#parsing), adds attributes to each node (the first item in each row parsed from the attribute sheet) in an attribute dictionary. The attribute dictionary has keys for each attribute type (the column headers) and values in a list. Each item in the list of values is a list with a string, the value of that attribute for that node. If there is a subattribute header assigned to that node, it is attached as part of a dictionary in the previous list. For example:
```python
attributes = {
	'Belief': [
		["Sunni'sm",{"W":0.8}],
		["Nationalism",{"W":0.1,"SENT":0.5}]
	],
	'Hair Color': ['Black'],
	...
}
```

`sna.createEdgeList(sourceSet)`
> Using list of **node** sheet cells generated during [instantation](#parsing), creates directed edges between nodes occupying the same row. The node occupying the column specified by `sourceSet` is the source of each edge. Every other node in the row is the target of an edge from the node occupying the source column. If the target node is an attribute value (see `SNA.loadAttributes()`) of the source node, and that attribute has a weight, that weight is applied to the edge. 
>
>*Arguments:*
- `sourceSet`: a **string** with the source column header

`sna.loadOntology()(source, classAssignments[, weight])`
> Using a user-provided set of class assignments for each column of nodes parsed during [instantation](#parsing), adds the attribute "ontClass" to each node with the value equal to the ontology class assigned to that node by the user. **Warning: the ontology classes are hardcoded strings in this method**. 
>
> *Arguments:*
- `source`: a **string** with the source column header
- `classAssignments`: a **dict** of class assignments keyed by node column header **strings**
- `weight` (optional): a **string** denoting the key used to access edge weights, if used

## Analysis

The analysis phase of SNA includes several basic network measures, edge propensity analysis, a community detection function, and a resilience measurement function which uses an exponential random graph model (ERGM).

### Measures

SNA includes several basic network measures that utilize the NetworkX [API](https://networkx.github.io/documentation/networkx-1.10/index.html). Node-dependent measures output a **dict** of measures keyed by node name that are stored as SNA class variables. While not all measures are visible in the tool, the class methods for network measurement are as follows (measure for which the network is converted to an undirected networks are noted):

- System-Wide Measures
	- [`sna.center()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.distance_measures.center.html)
	- [`sna.diameter()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.distance_measures.diameter.html?highlight=diameter)
	- [`sna.periphery()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.distance_measures.periphery.html?highlight=periphery)
	- [`sna.triadic_census()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.triads.triadic_census.html?highlight=triadic_census)
	- [`sna.average_degree_connectivity()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.assortativity.average_degree_connectivity.html#networkx.algorithms.assortativity.average_degree_connectivity)
	- [`sna.degree_assortativity_coefficient()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.assortativity.degree_assortativity_coefficient.html#networkx.algorithms.assortativity.degree_assortativity_coefficient)
	- [`sna.node_connectivity()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.connectivity.connectivity.node_connectivity.html#networkx.algorithms.connectivity.connectivity.node_connectivity)
	- [`sna.average_clustering()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.approximation.clustering_coefficient.average_clustering.html?highlight=average%20clustering#networkx.algorithms.approximation.clustering_coefficient.average_clustering) (undirected)
	- [`sna.attribute_assortativity(attr)`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.assortativity.attribute_assortativity_coefficient.html#networkx.algorithms.assortativity.attribute_assortativity_coefficient) - *argument: a **string** with the key of the attribute to be analyzed*
	- [`sna.is_strongly_connected()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.components.strongly_connected.is_strongly_connected.html?highlight=strongly%20connected#networkx.algorithms.components.strongly_connected.is_strongly_connected)
	- [`sna.is_weakly_connected()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.components.weakly_connected.is_weakly_connected.html?highlight=weakly%20connected#networkx.algorithms.components.weakly_connected.is_weakly_connected)
- Node-Dependent
	- [`sna.clustering()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.bipartite.cluster.clustering.html?highlight=clustering#networkx.algorithms.bipartite.cluster.clustering)
	- [`sna.latapy_clustering()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.bipartite.cluster.latapy_clustering.html?highlight=latapy_clustering#networkx.algorithms.bipartite.cluster.latapy_clustering)
	- [`sna.robins_alexander_clustering()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.bipartite.cluster.robins_alexander_clustering.html?highlight=robins#networkx.algorithms.bipartite.cluster.robins_alexander_clustering)
	- [`sna.closeness_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.closeness_centrality.html#networkx.algorithms.centrality.closeness_centrality)
	- [`sna.degree_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.degree_centrality.html#networkx.algorithms.centrality.degree_centrality)
	- [`sna.betweenness_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.betweenness_centrality.html#networkx.algorithms.centrality.betweenness_centrality)
	- [`sna.eigenvector_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.eigenvector_centrality.html#networkx.algorithms.centrality.eigenvector_centrality)
	- [`sna.katz_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.katz_centrality.html#networkx.algorithms.centrality.katz_centrality)
	- [`sna.load_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.load_centrality.html#networkx.algorithms.centrality.load_centrality)
	- [`sna.communicability_centrality()`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.communicability_centrality.html#networkx.algorithms.centrality.communicability_centrality)

`sna.set_property()`
> Calls all the system-wide measures.

`sna.sentiment(types, key[, operation])`
> A node-dependent custom measure that iterates through all node attributes and sums the weight towards every node of the given types. If "operation" is set to "average", the weights are averaged instead. 
*Returns: a **dict** of sentiment values keyed by node.*
>
> *Arguments:*
- `types`: a **list** of **strings**, one for each ontology class to be analyzed (e.g. "Belief")
- `key`: a **string** with the attribute key containing the weight to be analyzed (e.g. "W")

### Propensities

### Communities

### ERGM

### Resilience

## Forecasting

### Simple

### Smart

## Utilities

## Future Features

---
Ryan Steed

Lead Modeler

Laboratory for Unconventional Conflict Analysis and Simulation

ryansteed@gwu.edu