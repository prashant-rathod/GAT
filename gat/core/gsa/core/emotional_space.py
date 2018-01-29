
def getRelations():

    actors_val = {'A': [0.5, 0.6, 0.4, 0.1], 'B': [0.8, 0.2, 0.6, 0.6]}
    diff = {}

    actors = list(actors_val.keys())
    num_actors = len(actors)
    num_vals = len(actors_val[actors[0]])

    for i in range(num_actors - 1):
        for j in range (i + 1, num_actors):
            name = actors[i] + actors[j]
            diff[name] = []

            first_val = actors_val[actors[i]]
            second_val = actors_val[actors[j]]


            for k in range(num_vals):

                val_diff = round(abs(first_val[k] - second_val[k]), 1)
                diff[name].append(val_diff)

    print(diff)

    emoDict = [['Ecstasy', 'Joy', 'Serenity', 'Pensiveness',	'Sadness', 'Grief'],
               ['Admiration', 'Trust', 'Acceptance', 'Boredom', 'Disgust', 'Loathing'],
               ['Rage', 'Anger', 'Annoyance', 'Apprehension',	'Fear', 'Terror'],
               ['Amazement', 'Surprise', 'Distraction',	'Interest',	'Anticipation', 'Vigilance']]

    emotion = {}

    for i in list(diff.keys()):

        emotion[i] = []
        for j in range(len(diff[i])):

            val = diff[i][j]
            index = int(val // 0.35)
            emotion[i].append(emoDict[j][index])

    print(emotion)

    return actors_val, emotion




