import os
import random
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image

#42 unique codes for arabic characters
#Up to 125 characters per line
#So do 43 codes (one for empty) and then have a 43 row softmax output with 125 columns?
#Potential problem, all the pictures with whitespace at the top?

def clean_line(line):
    cleaned = line[line.find('.tif')+4:]
    cleaned = cleaned.strip()
    return cleaned

def get_labels(path):
    training_labels = open(path)
    line_array = {}
    for i ,line in enumerate(training_labels):
        temp_array = line.split()
        image_name = temp_array[0]
        image_name = image_name[0:image_name.find(".")]
        line_array[image_name] = temp_array[1:]
    return line_array

def get_batch(image_dir, label_dict, batch_size):
    image_batch = []
    label_batch = []
    for i in range(batch_size):
        image_name = random.choice(os.listdir(image_dir))
        img = load_img(image_dir+'/'+image_name) # this is a PIL image
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        x = x.reshape((1,) + x.shape) # this is a Numpy array with shape (1, 3, 150, 150)
        image_batch.append(x)
        label_batch.append(label_dict[image_name[0:image_name.find(".")]])
    return image_batch, label_batch

image_dir = "/home/cheesecake/Desktop/KHATT_v1.0/LineImages_v1.0/FixedTextLineImages/Train"
label_path = '/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/FixedTextLinesLatinTransliteration/TrainLabels_Translated.txt'

image_batch, label_batch = get_batch(image_dir, get_labels(label_path), 1)
print(image_batch)
print(label_batch)

