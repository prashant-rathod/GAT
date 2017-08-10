def propCalc(graph, edge):
    emoProps = []
    roleProps = []
    inflProps = []
    emoAttrSet = ["Belief", "Symbol", "Agent"]
    roleAttrSet = ["Belief", "Resource"]
    oppPairs = [
        ("IDBNATTUR", "IDBNATKUR"),
        ("IDBNATTUR", "IDBPROUSA"),
        ('ROBMOSSUN', 'ROBMOSSHI'),
        ('IDBVEL', 'IDBSEC'),
        ('POBNOT', 'IDBNATIRQ'),
        ('POBNOT', 'IDBNATKUR'),
        ('POBNOT', 'IDBNATIRN'),
        ('IDBNATIRN', 'IDBNATIRQ'),
        ('ROBANTJEW', 'ROBMOSSHI'),
        ('TURGOVHOS_ERD', 'TURGOVHOS_ATA'),
        ('TURGOVHOS_ERD', 'FLGTUR'),
        ('IRQGOVHOS', 'IRNGOVHOG'),
        ('TURGOVHOS_ERD', 'IRNGOVHOS_KAM'),
        ('IDBJHD', 'IDBPROUSA'),
        ('IDBANT_IMGMOSISS', 'IDBJHD'),
        ('IRQGOV', 'IMGMOSISS'),
        ('IRNGOV', 'IMGMOSISS'),
        ('POBNATIRQ', 'POBNATTUR'),
        ('BELMS', 'BELSHI'),
        ('BELAMH', 'BELNEO'),
        ('BELKUR', 'BELNEO'),
        ('BELAMH', 'BELIRH'),
        ('BELPIS', 'BELIMS'),
        ('BELSHI', 'BELSUN'),
        ('BELUIQ', 'BELKUR'),
    ]
    compPairs = [
        ('IDBPROUSA', 'IDBPROEUR'),
        ('IDBANTEUR', 'IDBANTUSA'),
        ('POBNOT', 'IDBNATTUR'),
        ('FLGKUR', 'TURGOVHOS_ERD'),
        ('LANKUR', 'FLGTUR'),
        ('IRQGOVHOG_ABD', 'TURGOVHOS_ERD'),
        ('TURGOVHOS_ERD', 'IRQKURKRG_HOS'),
        ('TURGOVHOS_ERD', 'TURGOVSPM_KIL'),
        ('ROBMOSSUN', 'IDBJHD'),
        ('FLGTUR', 'POBNOT'),
        ('BELIRH', 'BELUIQ'),
        ('BELAMH', 'BELPIS'),
        ('BELAMH', 'BELKUR'),
        ('BELAMH', 'BELIMS'),
        ('BELAMH', 'BELUIQ'),
        ('BELSUN', 'BELNEO'),
    ]
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
                        # Cooperative propensities:
                        if src_val[0] == trg_val[0]:
                            # Checking to see if each node's attribute weights fall within specified ranges:
                            if src_w >= 0.6 and trg_w >= 0.6:
                                emoProps.append(("Trust", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                ]
                            else:  # all others are joy
                                emoProps.append(("Joy", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                inflProps += [
                                    ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.7),
                                    ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                ]

                        elif attr in emoAttrSet:
                            # Competitive propensities
                            if (src_val[0], trg_val[0]) in compPairs or (trg_val[0], src_val[0]) in compPairs:
                                # Checking to see if each node's attribute weights fall within specified ranges:
                                if src_w < 0.6 and trg_w < 0.6:
                                    emoProps.append(
                                        ("Surprise", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.4),
                                        ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                         0.2),
                                    ]
                                else:
                                    emoProps.append(
                                        ("Anticipation", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                        ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                        ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                        ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                        ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.7),
                                        ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                    ]

                            # Coercive propensities:
                            elif (src_val[0], trg_val[0]) in oppPairs or (trg_val[0], src_val[0]) in oppPairs:
                                # Checking to see if each node's attribute weights fall within specified ranges:
                                if (src_w >= 0.8 and trg_w >= 0.6) or (src_w >= 0.6 and trg_w >= 0.6):
                                    emoProps.append(
                                        ("Anger", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                         0.2),
                                        ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ]
                                elif (src_w >= 0.6 and trg_w >= 0.4) or (src_w >= 0.4 and trg_w >= 0.6):
                                    emoProps.append(
                                        ("Sadness", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ]
                                elif (src_w >= 0.4 and trg_w >= 0.2) or (src_w >= 0.2 and trg_w >= 0.4):
                                    emoProps.append(("Fear", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                        ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w,
                                         0.8),
                                        ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                        ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.8),
                                        ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.5),
                                    ]
                                elif (src_w >= 0.8 and trg_w >= 0.2) or (src_w >= 0.2 and trg_w >= 0.8):
                                    emoProps.append(
                                        ("Disgust", attr, src_val[0], trg_val[0], src_w, trg_w, src_w * trg_w))
                                    inflProps += [
                                        ("Reciprocation", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Commitment & Consistency", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Social Proof", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Liking", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Authority", attr, src_val[0], trg_val[0], src_w, trg_w, 0.2),
                                        ("Scarcity", attr, src_val[0], trg_val[0], src_w, trg_w, 0.4),
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