import numpy as np
import scipy as sp

from gat.core.sna import excel_parser

###############
### GLOBALS ###
###############

A = (-.8,-.6)
B = (-.6,-.3)
C = (-.3,.3)
D = (.3,.6)
E = (.6,.8)
IO_keys = ["Warmth", "Affiliation", "Legitimacy", "Dominance", "Competence"]
legit_keys = ["Title","Role","Belief","Knowledge"]
dom_keys = ["Resource","Knowledge"]
role_keys = ["Hegemon", "Revisionist", "Ally", "DoF", "Dependent", "Independent", "Mediator", "Isolationist"]
role_weight_table = [ # (Hegemon, Revisionist, Ally, DoF, Dependent, Independent, Mediator, Isolationist) ^ 2
    [ # Hegemon
        [B,B,D,A,D], # Hegemon
        [A,A,B,B,C], # Revisionist
        [E,D,D,D,D], # Ally
        [C,B,B,C,B], # DoF
        [D,C,B,E,C], # Dependent
        [C,B,A,A,B], # Isolationist
        [C,C,C,B,C], # Mediator
        [D,C,B,D,C], # Independent
    ],
    [ # Revisionist
        [A,A,C,C,B], # Hegemon
        [C,C,D,A,B], # Revisionist
        [D,D,C,C,C], # Ally
        [A,B,C,B,C], # DoF
        [D,D,B,D,B], # Dependent
        [C,B,B,C,C], # Isolationist
        [C,C,B,B,D], # Mediator
        [C,C,C,B,B], # Independent
    ],
    [ # Ally
        [E,D,E,A,E], # Hegemon
        [E,D,C,B,C], # Revisionist
        [D,D,D,A,D], # Ally
        [C,C,C,C,C], # DoF
        [C,D,B,D,B], # Dependent
        [B,B,B,A,C], # Isolationist
        [C,C,D,A,D], # Mediator
        [B,B,B,B,A], # Independent
    ],
    [ #DoF
        [C,D,B,C,D], # Hegemon
        [B,C,B,B,B], # Revisionist
        [B,C,C,C,B], # Ally
        [B,C,B,A,A], # DoF
        [C,D,C,D,C], # Dependent
        [C,B,A,B,C], # Isolationist
        [B,C,C,B,C], # Mediator
        [C,B,C,B,C], # Independent
    ],
    [ # Dependent
        [E,C,E,A,E], # Hegemon
        [D,C,D,A,D], # Revisionist
        [D,C,C,A,C], # Ally
        [C,C,C,A,D], # DoF
        [D,D,A,B,B], # Dependent
        [B,A,A,B,A], # Isolationist
        [D,C,D,A,D], # Mediator
        [C,C,C,B,A], # Independent
    ],
    [ # Independent
        [B,C,D,B,D], # Hegemon
        [A,C,C,C,C], # Revisionist
        [C,C,B,C,C], # Ally
        [C,D,C,C,C], # DoF
        [C,C,B,C,C], # Dependent
        [D,D,C,C,D], # Isolationist
        [C,C,D,B,D], # Mediator
        [E,D,D,A,E], # Independent
    ],
    [ # Mediator
        [B,C,D,B,E], # Hegemon
        [C,C,D,C,C], # Revisionist
        [D,D,C,D,C], # Ally
        [C,C,C,D,C], # DoF
        [C,C,B,D,B], # Dependent
        [B,B,B,D,B], # Isolationist
        [C,E,D,A,D], # Mediator
        [C,C,B,D,C], # Independent
    ],
    [ # Isolationist
        [C,B,D,A,C], # Hegemon
        [A,A,C,A,B], # Revisionist
        [C,B,C,C,B], # Ally
        [B,A,B,B,B], # DoF
        [A,B,A,D,A], # Dependent
        [D,B,D,B,D], # Isolationist
        [B,C,C,B,C], # Mediator
        [C,C,D,B,C], # Independent
    ]
]
role_labels = [ # (Hegemon, Revisionist, Ally, DoF, Dependent, Independent, Mediator, Isolationist) ^ 2
    [ # Hegemon
        ["Facilitator","Belligerent"], # Hegemon
        ["Facilitator", "Belligerent"], # Revisionist
        ["Protector", "Provacateur"], # Ally
        ["Protector", "Provacateur"], # DoF
        ["Provider", "Provacateur"], # Dependent
        ["Facilitator", "Supporter"], # Isolationist
        ["Facilitator", "Belligerent"], # Mediator
        ["Protector", "Protector"], # Independent
    ],
    [ # Revisionist
        ["Consumer", "Belligerent"], # Hegemon
        ["Facilitator", "Belligerent"], # Revisionist
        ["Protector", "Provacateur"], # Ally
        ["Supporter", "Provacateur"], # DoF
        ["Provider", "Belligerent"], # Dependent
        ["Facilitator", "Supporter"], # Isolationist
        ["Supporter", "Belligerent"], # Mediator
        ["Facilitator", "Provacateur"], # Independent
    ],
    [ # Ally
        ["Consumer", "Provacateur"], # Hegemon
        ["Facilitator", "Belligerent"], # Revisionist
        ["Supporter", "Belligerent"], # Ally
        ["Consumer", "Provacateur"], # DoF
        ["Provider", "Provacateur"], # Dependent
        ["Facilitator", "Provacateur"], # Isolationist
        ["Facilitator", "Provacateur"], # Mediator
        ["Facilitator", "Supporter"], # Independent
    ],
    [ #DoF
        ["Consumer", "Belligerent"], # Hegemon
        ["Supporter", "Belligerent"], # Revisionist
        ["Supporter", "Belligerent"], # Ally
        ["Supporter", "Provacateur"], # DoF
        ["Provider", "Provacateur"], # Dependent
        ["Facilitator", "Supporter"], # Isolationist
        ["Facilitator", "Provacateur"], # Mediator
        ["Facilitator", "Provacateur"], # Independent
    ],
    [ # Dependent
        ["Consumer", "Supporter"], # Hegemon
        ["Consumer", "Supporter"], # Revisionist
        ["Supporter", "Provacateur"], # Ally
        ["Consumer", "Supporter"], # DoF
        ["Facilitator", "Supporter"], # Dependent
        ["Consumer", "Belligerent"], # Isolationist
        ["Consumer", "Belligerent"], # Mediator
        ["Consumer", "Belligerent"], # Independent
    ],
    [ # Independent
        ["Supporter", "Belligerent"], # Hegemon
        ["Supporter", "Belligerent"], # Revisionist
        ["Facilitator", "Provacateur"], # Ally
        ["Supporter", "Belligerent"], # DoF
        ["Provider", "Provacateur"], # Dependent
        ["Facilitator", "Supporter"], # Isolationist
        ["Supporter", "Provacateur"], # Mediator
        ["Belligerent", "Provacateur"], # Independent
    ],
    [ # Mediator
        ["Consumer", "Belligerent"], # Hegemon
        ["Supporter", "Belligerent"], # Revisionist
        ["Facilitator", "Provacateur"], # Ally
        ["Supporter", "Provacateur"], # DoF
        ["Provider", "Supporter"], # Dependent
        ["Facilitator", "Supporter"], # Isolationist
        ["Supporter", "Provacateur"], # Mediator
        ["Facilitator", "Provacateur"], # Independent
    ],
    [ # Isolationist
        ["Facilitator", "Provacateur"], # Hegemon
        ["Facilitator", "Belligerent"], # Revisionist
        ["Facilitator", "Belligerent"], # Ally
        ["Facilitator", "Provacateur"], # DoF
        ["Facilitator", "Provacateur"], # Dependent
        ["Supporter", "Provacateur"], # Isolationist
        ["Belligerent", "Provacateur"], # Mediator
        ["Supporter", "Supporter"] # Independent
    ]
]
infl_weight_table = [ # influence x IO
    [D,D,C,D,D],
    [D,B,C,A,C],
    [B,A,B,A,B],
    [B,B,D,A,D],
    [E,D,D,B,D],
    [C,B,C,B,B]
]

###############
### METHODS ###
###############

def propCalc(graph, edge):
    source = graph.G.node[edge[0]]
    target = graph.G.node[edge[1]]

    IO, verboseIO = IOCalc(graph, source, target)
    emoProps = emoCalc()
    inflProps = inflCalc(IO)

    roles = (source.get("Role"),target.get("Role"))
    roleProps = roleCalc(IO,roles) if None not in roles else []

    return verboseIO, emoProps, roleProps, inflProps


# INPUT: list of propensities where last index is propensity weight
# OUTPUT: average propensity weight as float
def aggregateProps(propList):
    return np.average(propList)

def IOCalc(graph, source, target):
    IO = [np.random.random_sample() * 2 - 1 for x in range(5)] # Warmth, Affiliation, Legitimacy, Dominance, Competence
    mutualAffiliations = []  # What should the values here be?

    for attr in (target if len(source) > len(target) else source):
        if attr not in ['block', 'newNode', 'Name'] and source.get(attr) is not None and target.get(attr) is not None:
            for src_val in [x for x in source.get(attr) if len(x) > 1]:
                for trg_val in [x for x in target.get(attr) if len(x) > 1]:

                    ##############################
                    ### IO Calculation Section ###
                    ##############################

                    src_w = float(src_val[1]["W"]) if "W" in src_val[1] else None
                    trg_w = float(trg_val[1]["W"]) if "W" in trg_val[1] else None

                    aff_w = src_w ** 2 * trg_w ** 2 if src_w is not None and trg_w is not None else None  # 3d parabola

                    ### Warmth IO ###
                    # Warmth IO is simply affect of source towards target
                    if src_val == target and src_w is not None:
                        IO[0] = aff_w  # warmth IO is simple affect

                    ### Affiliation IO ###
                    # Affiliation is average index weight of affect towards a shared attribute (average calculated outside loop)
                    if src_val[0] == trg_val[0]:
                        if aff_w is not None:
                            mutualAffiliations.append(aff_w)

    ## Affiliation IO (average) ##
    if len(mutualAffiliations) > 0:
        IO[1] = np.average(mutualAffiliations) - 1 # -1 to place on -1 to 1 scale, currently on 0 to 2 scale

    ## Legitimacy IO ##
    # Get sentiment towards relevant attributes
    sentiment = graph.sentiment(types=legit_keys,key='W',operation='average')
    legit_weights = []
    for attr in legit_keys:
        if source.get(attr) is not None:
            for subattr in source[attr]:
                if len(subattr)>0 and subattr[0] in sentiment.keys():
                    # compare source actor's attribute weight to the normal scale and add the percentile as a legitimacy weight
                    scaled = sp.stats.percentileofscore([sentiment[key] for key in sentiment], float(subattr[1]['W']))/100
                    legit_weights.append(scaled * 2 - 1) # place on -1 to 1 scale, currently on a 0 to 1 scale
    if len(legit_weights) > 0:
        IO[2] = np.average(legit_weights)

    ## Dominance IO
    resources = graph.sentiment(types=dom_keys,key="AMT",operation='sum')
    dom_weights = []
    for attr in dom_keys:
        if source.get(attr) is not None:
            for subattr in source[attr]:
                if len(subattr) > 0 and subattr[0] in resources.keys():
                    # compare source actor's resource share to the total amount of that resource
                    ratio = float(subattr[1]["AMT"])/resources[subattr[0]]
                    dom_weights.append(ratio * 2 - 1)  # place on -1 to 1 scale, currently on a 0 to 1 scale
    if len(dom_weights) > 0:
        IO[3] = np.average(dom_weights)

    ## Competence IO

    verbose = {}
    for i in range(len(IO)):
        verbose[IO_keys[i]] = IO[i]
    return IO, verbose

def emoCalc():
    eventTable = excel_parser.buildJSON('static/sample/sna/CAMEO-Emotion.xlsx') #TODO create a blueprint for Excel

    return {}

def inflCalc(IO):
    inflProps = [] # reciprocity, commitment, social proof, authority, liking, scarcity
    inflKey = ["Reciprocity","Commitment","Social Proof","Authority","Liking","Scarcity"]
    output = {}
    for i in range(len(infl_weight_table)-1):
        inflProps.append(np.average([a*np.random.uniform(low=b[0],high=b[1]) for a,b in zip(IO,infl_weight_table[i])])) # influence is a weighted average of the IOs, where weight random selection from a range in the weight table
        output[inflKey[i]] = inflProps[i]
    return output

def roleCalc(IO, roles):
    src_role_key = role_keys.index(roles[0])
    trg_role_key = role_keys.index(roles[1])
    weighted_avg = np.mean([a*np.random.uniform(low=b[0],high=b[1]) for a,b in zip(IO,role_weight_table[src_role_key][trg_role_key])])
    if weighted_avg > 0.5:
        return (role_labels[src_role_key][trg_role_key][0],weighted_avg)
    else:
        return (role_labels[src_role_key][trg_role_key][1], weighted_avg)
