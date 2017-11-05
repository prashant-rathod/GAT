import os
import random
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import scipy


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
    line_dict = {}
    for i ,line in enumerate(training_labels):
        temp_array = line.split()
        image_name = temp_array[0]
        image_name = image_name[0:image_name.find(".")]
        line_dict[image_name] = temp_array[1:]
    return line_dict

def get_batch(image_dir, label_dict, batch_size, width, height, channels):
    image_batch = np.empty((batch_size,width,height,channels))
    label_batch = []
    for i in range(batch_size):
        image_name = random.choice(os.listdir(image_dir))
        img = load_img(image_dir+'/'+image_name) # this is a PIL image
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        x = scipy.misc.imresize(x, (width,height,channels)) # this is a Numpy array with shape (1, 3, 150, 150)
        print(x.shape)
        image_batch[i,:,:,:] = x
        label_batch.append(label_dict[image_name[0:image_name.find(".")]])
    print(image_batch.shape)
    return image_batch, label_batch

image_dir = "/home/cheesecake/Desktop/KHATT_v1.0/LineImages_v1.0/FixedTextLineImages/Train"
label_path = '/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/FixedTextLinesLatinTransliteration/TrainLabels_Translated.txt'
width,height,channels = 400,256,3


image_batch, label_batch = get_batch(image_dir,get_labels(label_path), 16, width,height,channels)
for i in range(16):
    image = image_batch[i,:,:,:]
    image = image.reshape(width,height,channels)
    plt.imshow(image)
    plt.show()

image_batch = image_batch.astype('float32')
image_batch /= 255
print('x_train shape:', image_batch.shape)
print(image_batch.shape[0], 'train samples')

# convert class vectors to binary class matrices

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(43, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.adam(),
              metrics=['accuracy'])
