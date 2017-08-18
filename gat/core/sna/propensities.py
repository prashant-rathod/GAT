def propCalc(graph, edge):
    emoProps = []
    roleProps = []
    inflProps = []
    roleAttrSet = ["Belief", "Resource"]
    source = graph.G.node[edge[0]]
    target = graph.G.node[edge[1]]
    # Check if role attribute is present; if not, no role propensities calculated
    roleFlag = True if source.get("Role") is not None and target.get("Role") is not None else False
    for attr in (target if len(source) > len(target) else source):
        if attr not in ['block', 'newNode', 'Name'] and source.get(attr) is not None and target.get(attr) is not None:
            for src_val in [x for x in source.get(attr) if len(x) > 1]:
                for trg_val in [x for x in target.get(attr) if len(x) > 1]:

                    #####################################
                    ### Propensity assignment section ###
                    #####################################

                    ## Emotion & Influence Propensities ##
                    src_w = float(src_val[1]["W"]) if "W" in src_val[1] else None
                    trg_w = float(trg_val[1]["W"]) if "W" in trg_val[1] else None
                    if src_w is not None and trg_w is not None:
                        index_w = src_w * trg_w # index weight: product of src and trg weights, used to evaluate propensities
                        # Cooperative propensities:
                        if src_val[0] == trg_val[0]:
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

                        # Coercive propensities:
                        else:
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
                    # Still need to add conditional opposites, like in emotion
                    src_amt = float(src_val[1]["AMT"]) if attr == "Resource" and "AMT" in src_val[1] else None
                    trg_amt = float(trg_val[1]["AMT"]) if attr == "Resource" and "AMT" in trg_val[1] else None
                    if roleFlag and attr in roleAttrSet:
                        if src_val[0] == trg_val[0]:
                            roleProps.append(["Consumer or Provider", .5] if attr == "Resource" else None)
                            # print("Appended Cons. or Prov. using attribute", attr, "(", src_val, "&", trg_val, ")",
                            #       "for node pair (", source, ",", target, ")")
                            roleProps.append(["Protector", .75] if attr == "Belief" else None)
                            # print("Appended Protector using attribute", attr, "(", src_val, "&", trg_val, ")",
                            #       "for node pair (", source, ",", target, ")")

    return emoProps, roleProps, inflProps