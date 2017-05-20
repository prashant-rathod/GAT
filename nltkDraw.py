import nltk, re, pprint
import os
download_path = None
home = os.path.expanduser("~")
if home == "/home/wsgi":
    download_path =  "/opt/python/current/app/"
    print(download_path)
    nltk.data.path.append(download_path)
#os.mkdir(os.path.expanduser("/home/wsgi"))
nltk.download('punkt', download_dir = download_path)
from nltk import word_tokenize
import tempfile
#user chooses keywords
#plot tweets against time
#user inputs twitter channel name too
def plot(filename,terms):
    if filename == '':
        return
    if filename == None:
        return
    if terms == None:
        return
    if len(terms) == 0:
        return
    with open(filename, 'rb') as myfile:
        raw = myfile.read()
    raw = str(raw, errors='ignore')
    tokens = word_tokenize(raw)
    text = nltk.Text(tokens)
    print("Total text length is", len(text))
    print("Total vocabulary length is", len(set(text)))
    print("Average no of times word used is", len(text) / len(set(text)))
    return dispersion_plot(text, terms, ignore_case=True)
def dispersion_plot(text, words, ignore_case=False, title="Lexical Dispersion Plot"):
    """
    Generate a lexical dispersion plot.
    :param text: The source text
    :type text: list(str) or enum(str)
    :param words: The target words
    :type words: list of str
    :param ignore_case: flag to set if case should be ignored when searching text
    :type ignore_case: bool
    """
    try:
        from matplotlib import pylab
    except ImportError:
        raise ValueError('The plot function requires matplotlib to be installed.'
                     'See http://matplotlib.org/')
    pylab.clf()
    text = list(text)
    words.reverse()
    if ignore_case:
        words_to_comp = list(map(str.lower, words))
        text_to_comp = list(map(str.lower, text))
    else:
        words_to_comp = words
        text_to_comp = text
    points = [(x,y) for x in range(len(text_to_comp))
                    for y in range(len(words_to_comp))
                    if text_to_comp[x] == words_to_comp[y]]
    if points:
        x, y = list(zip(*points))
    else:
        x = y = ()
    pylab.plot(x, y, "b|", scalex=.1)
    pylab.yticks(list(range(len(words))), words, color="b")
    pylab.ylim(-1, len(words))
    pylab.title(title)
    pylab.xlabel("Word Offset")
    f = tempfile.NamedTemporaryFile(
            dir='static/temp',
            suffix='.png',delete=False)
    print(f)
    # save the figure to the temporary file
    f2 = open("nltkPlot.png", "w")
    pylab.savefig(f2, bbox_inches='tight')
    f2.close()
    pylab.savefig(f, bbox_inches='tight')
    f.close() # close the file
    # get the file's name
    # (the template will need that)
    plotPng = f.name.split('/')[-1]
    os.chmod(f.name, 0o644)
    return plotPng
