import os

#42 unique codes for arabic characters

def clean_line(line):
    cleaned = line[line.find('.tif')+4:]
    cleaned = cleaned.strip()
    return cleaned

f = open('/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/FixedTextLinesLatinTransliteration/TrainLabels_Translated.txt')
for i ,line in enumerate(f):
    line_array = line.split()
    print(line_array)