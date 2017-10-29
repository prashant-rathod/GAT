import numpy as np

def propCalc(graph, edge):
    emoProps = []
    roleProps = []
    inflProps = []
    roleAttrSet = ["Belief","Resource"]
    source = graph.G.node[edge[0]]
    target = graph.G.node[edge[1]]
    src_role = source.get("Role")
    trg_role = target.get("Role")

    for attr in (target if len(source) > len(target) else source):
        if attr not in ['block', 'newNode', 'Name'] and source.get(attr) is not None and target.get(attr) is not None:
            for src_val in [x for x in source.get(attr) if len(x) > 1]:
                for trg_val in [x for x in target.get(attr) if len(x) > 1]:

                    #####################################
                    ### Propensity assignment section ###
                    #####################################

                    ### Emotion & Influence Propensities ###
                    src_w = float(src_val[1]["W"]) if "W" in src_val[1] else None
                    trg_w = float(trg_val[1]["W"]) if "W" in trg_val[1] else None

                    ### Relationship Categories for Roles ###
                    # Check if role attribute is present; if not, no role propensities calculated
                    roleRelation = 0 if source.get("Role") is not None and target.get("Role") is not None else None
                    if roleRelation == 0 and attr in roleAttrSet:
                        ## Calculate relationship type: 0 for neutral, 1 for friend, -1 for adversary
                        # Friends
                        if src_role == "Developer" and trg_role == "Developer":
                            roleRelation += 1
                        if src_role not in ["Model","Defender of the Faith","Nonaffiliated Independent","Mediator"] and trg_role in ["Ally","Supporter","Dependent"]:
                            roleRelation += 1
                        # Adversary
                        if src_role == "Hegemon" and trg_role == "Revisionist" or src_role == "Revisionist" and trg_role == "Hegemon":
                            roleRelation -= 1
                        # If a hegemon/revisionist is a neighbor of the target node, adversarial
                        if src_role == "Hegemon" and "Revisionist" in [neighbor.get("Role") for neighbor in graph[edge[0]]] or src_role == "Revisionist" and "Hegemon" in [neighbor.get("Role") for neighbor in graph[edge[0]]]:
                            roleRelation -= 1
                        # Could be using resources, but not yet
                        # src_amt = float(src_val[1]["AMT"]) if attr == "Resource" and "AMT" in src_val[1] else None
                        # trg_amt = float(trg_val[1]["AMT"]) if attr == "Resource" and "AMT" in trg_val[1] else None

                    index_w = src_w * trg_w if src_w is not None and trg_w is not None else None
                    # Cooperative propensities
                    if src_val[0] == trg_val[0]:
                        if index_w is not None:
                            # Checking to see if each combo's attribute weight index fall within specified ranges:
                            if index_w > 0.36:
                                emoProps.append(("Trust", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                ]
                            elif index_w > 0.09:
                                emoProps.append(("Joy", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.7),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                ]
                            elif (src_w >= 0.9 and trg_w <= 0.09) or (src_w <= 0.09 and trg_w >= 0.9): # if very different weights, disgust
                                emoProps.append(
                                    ("Disgust", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.4),
                                ]
                            else:
                                emoProps.append(
                                    ("Anticipation", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.7),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                ]
                            ## Role Propensities ##
                            if roleRelation is not None and roleRelation > -1:
                                if attr == "Resource":
                                    roleProps.append(("Consumer-Provider Relationship", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                if attr == "Belief":
                                    roleProps.append(("Protector", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))

                    # Coercive and competitive propensities:
                    else:
                        if index_w is not None:
                            # Checking to see if each node's attribute weights fall within specified ranges:
                            if index_w > 0.62:
                                emoProps.append(
                                    ("Anger", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                     0.2),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                ]
                            elif index_w > 0.25:
                                emoProps.append(("Fear", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                     0.8),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                ]
                            elif index_w > 0.06:
                                emoProps.append(
                                    ("Sadness", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                ]
                            else: # anything under 0.06 is surprise
                                emoProps.append(
                                    ("Surprise", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.4),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                     0.2),
                                ]
                            ## Role Propensities ##
                            if roleRelation is not None and roleRelation < 0:
                                if attr == "Belief":
                                    roleProps.append(("Belligerent", attr, src_val[0], trg_val[0], src_w, trg_w, index_w))
    return emoProps, roleProps, inflProps

# INPUT: list of propensities where last index is propensity weight
# OUTPUT: average propensity weight as float
def aggregateProps(propList):
    data = [prop[-1] for prop in propList]
    return np.average(data)