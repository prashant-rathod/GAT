![LUCAS Logo](http://css-lucas.com/wp-content/uploads/2016/07/cropped-Lucas-Header-for-website.png)

# SNA Documentation
Last updated: January 15, 2017

## Overview

SNA is the social network analysis portion of Project Hermes 2.0. Its major features are as follows:

- constructs 2D and 3D networks based on Excel spreadsheet input from an analyst
- performs simple network analysis measures on a graph constructed using a sociology-based ontology of node classes
- performs more advanced, customized network analysis on resilience and influence community detection
- forecasts likely outcomes with stochastic probability model and psychology/political theory-based propensities model

### Specifications

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

SNA is comprised of a main class object defined in `sna.py` and several helper library scripts. The following documentation will refer to library functions by attaching a Pythonic prefix (e.g. `cliques.louvain()` refers to the `louvain()` algorithm found in `cliques.py`). All other functions are SNA class methods (e.g. `python SNA.__init__()`).

### Contents

1. [Construction](#construction)
	1. [Parsing](#parsing)
	2. [Network](#network)
2. [Analysis](#analysis)
	1. [Measures](#measures)
	2. [Communities](#communities)
	3. [ERGM](#ergm)
	4. [Resilience](#resilience)
3. [Forecasting](#forecasting)
	1. [Simple](#simple)
	2. [Smart](#smart)
4. [Future Features](#future-features)

## Construction

The first stage of SNA parses an Excel sheet into a node list and an edge list. Each node is assigned an ontological class and attributes according to user data. A network is constructed using edges in the edge list.

### Parsing

`SNA.__init__(excel_file, nodeSheet[, attrSheet])`
> On class instantiation, parses a list of nodes from a user-inputted Excel sheet and a list of attributes if provided to `SNA.list` and `SNA.attrList`, respectively (see also [excel_parser](#excel_parser)). Creates an empty directed NetworkX graph object (refer to [networkx](https://networkx.github.io/documentation/networkx-1.10/index.html) for documentation) at `SNA.G`. Also initializes several other class variables used in various methods, including lists of nodes, edges, and measure values. *Arguments: a path to an Excel file, the name of the node sheet in that Excel file[, the name of the attribute sheet in that Excel file].*

#### excel_parser

The `excel_parser` library script provides methods for parsing the custom Excel templates used for SNA.

`excel_parser.readFile(subAttrs, excel_file, sheet)`
> Read a specified sheet in an SNA Excel template and return the first row (without repeats) and a list of lists, each containing dictionaries for each cell. The dictionary has two keys: 'val', the value in that cell, and 'header', the column to which that cell belongs by column title. If there are subattributes (e.g. an attribute weight), these are not included in the list of column headers. *Arguments: a list of column headers that are subattributes, a path to an SNA Excel template, and the name of the sheet to parse).*

`excel_parser.buildJSON(excel_file)`
> Creates a jsonifiable dictionary in which the keys are the last-parsed cell in the second column (parsing left to right, top to bottom) and the values are lists of dictionaries. Each dictionary represents a row, where the keys are column headers and the values are cell values corresponding to each header. Repeated headers are permitted but not expected. *Arguments: a path to an Excel document with a single sheet*.

### Network
`SNA.createNodeList(nodeSet)`
> Using list of node sheet cells generated during [instantation](#parsing), adds nodes to `SNA.G` graph object with attribute 'block' equal to the node's header in the Excel sheet (see also [excel_parser](#excel_parser)). Only includes nodes in the user-selected columns specified by `nodeSet`. *Arguments: a list of the node columns to include in the network by column header.*

`SNA.loadAttributes()`
> Using list of attribute sheet cells generated during [instantation](#parsing), adds attributes to each node (the first item in each row parsed from the attribute sheet) in an attribute dictionary. The attribute dictionary has keys for each attribute type (the column headers) and values in a list. Each item in the list of values is a list with a string, the value of that attribute for that node. If there is a subattribute header assigned to that node, it is attached as part of a dictionary in the previous list. For example:
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

`SNA.createEdgeList(sourceSet)`
> 

## Analysis

### Measures

### Communities

### ERGM

### Resilience

## Forecasting

### Simple

### Smart

## Future Features

---
Ryan Steed

Lead Modeler

Laboratory for Unconventional Conflict Analysis and Simulation

ryansteed@gwu.edu