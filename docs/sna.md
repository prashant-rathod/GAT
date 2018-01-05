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
		1. [IOs](#ios)
		2. [Emotion](#emotion)
		3. [Influence](#influence)
		4. [Role](#role)
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
>- `excel_file`: a **string** with a path to an Excel file
>- `nodeSheet`: a **string** with the name of the node sheet in that Excel file
>- `attrSheet` (optional): a **string** with the name of the attribute sheet in that Excel file

#### `excel_parser`

The `excel_parser` library script provides methods for parsing the custom Excel templates used for SNA.

`excel_parser.readFile(subAttrs, excel_file, sheet)`
> Reads a specified sheet in an SNA Excel template and return the first row (without repeats) and a list of lists, each containing dictionaries for each cell. The dictionary has two keys: 'val', the value in that cell, and 'header', the column to which that cell belongs by column title. If there are subattributes (e.g. an attribute weight), these are not included in the list of column headers. 
>
> *Arguments:*
>- `subAttrs`: a **list of strings** containing column headers that are subattributes
>- `excel_file`: a **string** with the path to an SNA Excel template
>- `sheet`: a **string** with the name of the sheet to parse)

`excel_parser.buildJSON(excel_file)`
> Creates a jsonifiable dictionary in which the keys are the last-parsed cell in the second column (parsing left to right, top to bottom) and the values are lists of dictionaries. Each dictionary represents a row, where the keys are column headers and the values are cell values corresponding to each header. Repeated headers are permitted but not expected. 
>
> *Arguments:*
>- `excel_file`: a **string** path to an Excel document with a single sheet

### Network
`sna.createNodeList(nodeSet)`
> Using list of **node** sheet cells generated during [instantation](#parsing), adds nodes to `SNA.G` graph object with attribute 'block' equal to the node's header in the Excel sheet (see also [excel_parser](#excel_parser)). Only includes nodes in the user-selected columns specified by `nodeSet`, and excludes repeated node names. 
>
> *Arguments:*
>- `nodeSet`: a **list** of the node columns to include in the network by column header

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
>- `sourceSet`: a **string** with the source column header

`sna.loadOntology()(source, classAssignments[, weight])`
> Using a user-provided set of class assignments for each column of nodes parsed during [instantation](#parsing), adds the attribute `"ontClass"` to each node with the value equal to the ontology class assigned to that node by the user. The ontology classes are hardcoded strings and can be any one of the following:
```python
ontological_elements = ["Actor","Belief","Symbol","Resource","Agent","Organization","Event","Audience","Role","Knowledge"]
```
>
> *Arguments:*
>- `source`: a **string** with the source column header
>- `classAssignments`: a **dict** of class assignments keyed by node column header **strings**
>- `weight` (optional): a **string** denoting the key used to access edge weights, if used

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
> A node-dependent custom measure that iterates through all node attributes and sums the weight towards every node of the given types. If `operation` is set to `"average"`, the weights are averaged instead. 
>
> *Returns:*
>- a **dict** of sentiment values keyed by node
>
> *Arguments:*
>- `types`: a **list** of **strings**, one for each ontology class to be analyzed (e.g. `"Belief"`)
>- `key`: a **string** with the attribute key containing the weight to be analyzed (e.g. `"W"`)

### Propensities

The propensities model assigns *a priori* probabilities and descriptions to edges in the network based on the attributes and properties of dyads. Specifically, propensities are formulated using attributes and the Intersubjective Orientation vector, which contains values representing the level of five different qualities of a subjective relationship: 
- [Warmth](#warmth)
- [Affiliation](#affiliation)
- [Legitimacy](#legitimacy)
- [Dominance](#dominance)
- [Competence](#competence)

Specifically, propensities are split into three independent categories:
- [Emotion](#emotion)
- [Influence](#influence)
- [Role](#role)

`sna.calculatePropensities([propToggle])`
> The primary class method for calculating propensities. Iterates through network edges and assigns propensity calculation output (see `propensities.propCalc`) in the attribute dictionary (see also [attribute assignment](#network)). Filters which propensities are included based on user toggle input.
>
> *Arguments:*
>- `propToggle` (optional): a **dict** keyed by propensity type (one of `"emo"`, `"infl"`, or `"role"`) with Boolean values (`True` if propensity should be calculated, else `False`)

`propensities.propCalc(graph, edge[, propToggle])`
> For a given edge, calculates IO (see [IOs](#ios)) and required propensity types using helper functions (see [Emotion](#emotion), [Influence](#influence), and [Role](#role)).
>
>*Returns:*
>- a **dict** keyed by IO descriptor (e.g. `"Warmth"`) with values for each IO calculated
>- a **list** of [emotional](#emotional) propensities
>- a **list** of [influence](#influence) propensities
>- a **list** of [role](#role) propensities
>
> *Arguments:*
>- `graph`: a NetworkX **graph object**
>- `edge`: a **tuple** containing two **strings**, one for each node name in the dyad to be analyzed
>- `propToggle` (optional): a **dict** keyed by propensity type (one of `"emo"`, `"infl"`, or `"role"`) with Boolean values (`True` if propensity should be calculated, else `False`)

#### IOs

`propensities.IOCalc(graph, source, target)`
> A helper function used to calculate intersubjective orientation (IO) for a directed dyad. First creates a **list** of random floats, one for each IO value, then assigns new floats to each place according to their respective model (see [Warmth](#warmth), [Affiliation](#affiliation), [Legitimacy](#legitimacy), [Dominance](#dominance), and [Competence](#competence)). Uses globally stored list of IO descriptors to generate a verbose output **dict** as well as a condensed **list**:
```python
IO_keys = ["Warmth", "Affiliation", "Legitimacy", "Dominance", "Competence"]
```
>
>*Returns:*
>- a **list** of floats, one for each IO value, from -1 to 1
>- a **dictionary** with the same length, keyed by **strings** describing each value, where values are **floats**
>
>*Arguments:*
>- `graph`: a NetworkX **graph object**
>- `source`: a **string** with the name of source node in dyad
>- `target`: a **string** with the name of target/subject node in dyad

##### Warmth

Warmth is simply the affect of the source node towards the target node, accessed by iterating through every attribute value in the source node's attribute **dict** and checking for the name of the target node. If both the target node's name and a subattribute `"W"` are present, the value of `"W"` is added to the IO **list** as warmth.

##### Affiliation

Affiliation is the *average index weight* of affect towards any shared attribute value (e.g. `"Nationalism"`). Index weight is calculated according to the following equation, which creates a hyperboloid from -1 to 1 in all dimensions:
```python
w_index = w_src ** 2 + w_trg ** 2 - 1
```
![hyperboloid](./resources/hyperboloid.png)

A combination of any two extreme affects will produce an accordingly extreme affect index weight (either positive or negative).

##### Legitimacy

Legitimacy accounts for the network-wide sentiment towards various attributes that are also represented as nodes in the network. Using the `sna.sentiment` function (see [Measures](#measures)), the average sentiments for all nodes with acceptable ontology classes for legitimacy measurement are calculated. Currently, the acceptable ontology classes are defined by a global variable:
```python
legit_keys = ["Title","Role","Belief","Knowledge"]
```
If a node belonging to one of these classes appears in the source node's attribute **dict**, it is given a percentile according to the distribution of average sentiments across all nodes for which average sentiment was calculated. This percentile is rescaled. Once all relevant attributes are scored and rescaled, legitimacy is assigned the average percentile average sentiment towards nodes appearing in the source node's attributes.

##### Dominance

Dominance is simply the source node's average percent share of a network resource. Network resources belong to ontology classes defined by a global variable:
```python
dom_keys = ["Resource","Knowledge"]
```
Total resource amounts are collected using the `sna.sentiment` function (see [Measures](#measures)) where the types assessed are given by `dom_keys` and the attribute key used is `"AMT"`. The final resource share is rescaled from [0,1] to [-1 to 1].

##### Competence

Competence is assigned randomly for each dyad pending progress on Task Models for SNA.

#### Emotion

Emotion propensities are aggreggated in two stages.

For every neighboring event, a "simple" emotion is collected according to the CAMEO category of that event. The CAMEO-emotion associations are provided by an Excel spreadsheet, reproduced below and stored in the global variable `emo_key`:

|CAMEO Category|Emotion|
|---|---|
|Assault|Rage|
|Use unconventional mass violence|Terror|
|Fight|Anger|
|Coerce|Vigilance|
|Exhibit force posture|Amazement|
|Reduce relations|Disgust|
|Threaten|Fear|
|Reject|Loathing|
|Disapprove|Surprise|
|Investigate|Interest|
|Control information|Distraction|
|Yield|Acceptance|
|Protest|Grief|
|Refuse to build infrastructure|Sadness|
|Demand|Annoyance|
|Appeal|Acceptance|
|Make a public statement|Interest|
|Build energy infrastructure|Trust|
|Build social infrastructure|Trust|
|Build political infrastructure|Trust|
|Build military infrastructure|Trust|
|Build information infrastructure|Trust|
|Build economic infrastructure|Trust|
|Gather/mine for materials|Joy|
|Change price|Apprehension|
|Government funds|Joy|
|Express intent|Pensiveness|
|Appeal to build infrastructure|Trust|
|Express intent to cooperate|Joy|
|Express intent to build infrastructure|Serenity|
|Consult|Admiration|
|Accede|Ecstasy|
|Use social following|Anticipation|
|Demand to build infrastructure|Anticipation|
|Engage in material cooperation|Admiration|
|Engage in diplomatic cooperation|Ecstasy|
|Provide aid|Ecstasy|

Each of these emotions can be placed on Plutchik's wheel of emotions as in the diagram below.
![plutchik](./resources/plutchik.png)

An emotion is positioned on any of three concentric circles and is surrounded by two "refined" emotions. 

To determine which of the two "refined" emotions is associated with a neighboring event, threat level is calculated. Threat level depends on the IO values of Warmth and Competence. Here, **high** is defined as any positive value, while **low** is any negative value.

|Warmth\Competence|High|Low
|---|---|---|
|**High**|`threat = -1`|`threat = 0`|
|**Low**|`threat = 1`|`threat = 0`|

This threat level determines which direction the "simple" emotion will "snap" to determine a "refined" emotion. Put simply, a higher threat pushes emotion towards the Fear/Anger axis.

Programmatically, the snapping function separates all possible emotions into six semicircles spanning from Fear to Anger on each side of each tier. These semicircles are stored as **lists** in a global **dict** keyed by tier:
```python
threatRanking = {
    "low":[
        [
	        "Annoyance", "Anxiety","Interest","Resignation","Serenity",
	        "Content","Acceptance","Worry", "Apprehension"
        ],
        [
	        "Annoyance", "Curiosity","Boredom","Disgruntled","Pensiveness",
	        "Apathy","Distraction","Dismay", "Apprehension"
        ]
    ],
    "medium": [
        [
	        "Anger","Despair","Anticipation","Vulnerability","Joy",
	        "Love","Trust","Paranoia","Fear"
        ],
        [
	        "Anger","Excitement","Disgust","Hatred","Sadness",
	        "Broodiness","Surprise","Melancholy","Fear"
        ]
    ],
    "high": [
        [
	        "Rage","Hopeless","Vigilence","Envy","Ecstasy",
	        "Adoration","Admiration","Wonder","Terror"
        ],
        [
	        "Rage","Dread","Loathing","Cruel","Grief",
	        "Resentment","Amazement","Hopeful","Terror"
        ]
    ]
}
```
For each list, lowest index is closest to anger, while the highest index is closest to fear.

If threat level is high, the "simple" emotion snaps to the neighboring "refined" emotion that is closest to the Fear/Anger axis. If threat level is low, the "simple" emotion snaps to the neighboring "refined" emotion that is farthest from the Fear/Anger axis. The distance from the axis is determined by index level in the semicircle list. If threat level is medium, there is a 50% chance the "simple" emotion will snap to either neighboring "refined" emotion.

Thus, every neighboring event produces a simple emotion, which is snapped to a refined emotion. A given node has as many emotion propensities as there are neighboring events.

`emoCalc(G, edge, IO)`
> A helper function that uses the model above to formulate a **list** of subjective emotions within a dyad. Finds all source node neighbors that are also event nodes and gets the emotion associated with each event. The emotion associations are provided by a spreadsheet stored globally as JSON (`GAT/static/sample/sna/CAMEO-Emotion.xlsx`) which is parsed using the `excel_parser.buildJSON` function (see [Parsing](#parsing)). Refines emotion using snapping function (above). Outputs a list of refined emotions, one for each neighboring event.
>
>*Returns:*
>- a **list** of **strings**, each with one refined emotion
>
>*Arguments:*
>- `G`: a NetworkX **graph object**
>- `edge`: a **tuple** containing two **strings**, one for each node name in the dyad to be analyzed
>- `IO`: a **list** of floats, one for each IO value, from -1 to 1

#### Influence

Influence propensities have six components, each represented by a numerical value from -1 to 1:
- Reciprocity
- Commitment
- Social proof
- Authority
- Liking
- Scarcity

Each component is determined by a weighted average of the IO values, where the weights are provided by the table below (stored in the global variable `infl_weight_table`). Weights are chosen randomly from a range of values, also provided below.
```python
## weights ##
A = (-.8,-.6)
B = (-.6,-.3)
C = (-.3,.3)
D = (.3,.6)
E = (.6,.8)
```

| | Warmth | Affiliation | Legitimacy | Dominance | Competence |
|---|---|---|---|---|---|
| **Reciprocity**  |D|D|C|D|D|
| **Commitment**   |D|B|C|A|C|
| **Social Proof** |B|A|B|A|B|
| **Authority**    |B|B|D|A|D|
| **Liking**       |E|D|D|B|D|
| **Scarcity**     |C|B|C|B|B|

The meaning of a particular influence propensity (e.g. Reciprocity) is derived from the arrangement of weights used to produce it. For example, the IO value "Warmth" matters much more to the influence propensity "Liking" than it does to "Authority".

Each influence propensity is represented by a single numerical value, which is the weighted average of all five IO values using a random weight selection from the ranges provided for that particular influence propensity.

`inflCalc(IO)`
> A helper function that uses the model above to generate vectors of six weighted average values each, one for each influence propensity. Adds to a verbose dictionary keyed by influence propensity.
>
>*Returns:*
>- a **dict** keyed by **strings** with influence propensity descriptors, where values are floats from -1 to 1
> 
>*Arguments:*
>- `IO`: a **list** of floats, one for each IO value, from -1 to 1

#### Role

Role propensities operate on a similar weighted average, but take into account the role of both the source and target nodes. Thus, role propensities depend on both IO and the roles of each node in the dyad.

Stored in the global **list** `role_weight_table`, the following table establishes the weight ranges for any combination of roles. Each list corresponds to the five IO values (sequentially, [Warmth](#warmth), [Affiliation](#affiliation), [Legitimacy](#legitimacy), [Dominance](#dominance), and [Competence](#competence)).
```python
## weights ##
A = (-.8,-.6)
B = (-.6,-.3)
C = (-.3,.3)
D = (.3,.6)
E = (.6,.8)

IO_keys = ["Warmth", "Affiliation", "Legitimacy", "Dominance", "Competence"]
```

| | Hegemon | Revisionist | Ally | Defender of the Faith | Dependent | Independent | Mediator | Isolationist |
|---|---|---|---|---|---|---|---|---|
| **Hegemon**  |[B,B,D,A,D]|[A,A,B,B,C]|[E,D,D,D,D]|[C,B,B,C,B]|[D,C,B,E,C]|[C,B,A,A,B]|[C,C,C,B,C]|[D,C,B,D,C]
| **...**  | ... | ... | ... | ... | ... | ... | ... | ... |
| **Isolationist**  |[C,B,D,A,C]|[A,A,C,A,B]|[C,B,C,C,B]|[B,A,B,B,B]|[A,B,A,D,A]|[D,B,D,B,D]|[B,C,C,B,C]|[C,C,D,B,C]|

The weight ranges for a given role pairing are used to take a weighted average of the IO values for a given dyad, producing the role weight. Role labels depend on the role weight. For every role pairing, there are two possible role labels, provided in the table below:

| | Hegemon | Revisionist | Ally | Defender of the Faith | Dependent | Independent | Mediator | Isolationist |
|---|---|---|---|---|---|---|---|---|
| **Hegemon**  |Facilitator/Belligerent|Facilitator/Belligerent|Protector/Provacateur|Protector/Provacateur|Provider/Provacateur|Facilitator/Supporter|Facilitator/Facilitator|Protector/Protector|
| **...**  | ... | ... | ... | ... | ... | ... | ... | ... |
| **Isolationist**  |Facilitator/Provacateur|Facilitator/Belligerent|Facilitator/Belligerent|Facilitator/Provacateur|Facilitator/Provacateur|Supporter/Provacateur|Belligerent/Provacateur|Supporter/Supporter|

If the role weight is positive, the first role label is used. If role weight is negative, the second role label is used.

For each dyad, one role weight is calculated and one role label is determined.

`roleCalc(IO, roles)`
>A helper function which calculates role weighted average and role label according to the method described above. Outputs a simple tuple (not verbose).
>
>*Returns:*
>- a **string** with the role label (see table above)
>- a **float**, the weighted average of the IO values
>
>*Arguments:*
>- `IO`: a **list** of floats, one for each IO value, from -1 to 1
>- `roles`: a **tuple** containing two **strings** describing the role of the source node and target node, sequentially

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

*Laboratory for Unconventional Conflict Analysis and Simulation*

*ryansteed@gwu.edu*

[- Top -](#contents)