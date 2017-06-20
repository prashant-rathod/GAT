from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    with open (fname, 'rb') as infile:
         for page in PDFPage.get_pages(infile, pagenums):
             interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 
x = convert('trumpspeech.pdf')
from textblob import TextBlob
text = TextBlob(x)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
print (sid.polarity_scores(x))
dict = sid.polarity_scores(x)
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = ('Negative', 'Neutral', 'Positive')
y_pos = np.arange(len(objects))
y =[dict['neg']*100, dict['neu']*100, dict['pos']*100]
 
plt.bar(y_pos, y, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Percentage of Total Words(%)')
plt.title('Sentiment vs Total Words')
 
plt.show()
