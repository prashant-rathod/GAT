import os
import random
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

#42 unique codes for arabic characters
#Up to 125 characters per line
#So do 43 codes (one for empty) and then have a 43 row softmax output with 125 columns?
#Potential problem, all the pictures with whitespace at the top?

image_dir = "/home/cheesecake/Desktop/KHATT_v1.0/LineImages_v1.0/FixedTextLineImages/Train"

def clean_line(line):
    cleaned = line[line.find('.tif')+4:]
    cleaned = cleaned.strip()
    return cleaned

training_labels = open('/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/FixedTextLinesLatinTransliteration/TrainLabels_Translated.txt')

line_array = []
for i ,line in enumerate(training_labels):
    line_array.append(line.split())

print(line_array)

def get_batch(batch_size):
    image_batch = []
    label_batch = []
    for i in range(batch_size):
        imagename = random.choice(os.listdir(image_dir))
        img = load_img(image_dir+'/'+imagename) # this is a PIL image
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        x = x.reshape((1,) + x.shape)
        image_batch.append(x)

    return image_batch

print(get_batch(1))