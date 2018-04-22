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
from keras.layers import Conv2D, MaxPooling2D, GlobalMaxPooling2D
from spp.SpatialPyramidPooling import SpatialPyramidPooling
from keras import backend as K
import scipy
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF

#Yo turns out there are only 28 characters in arabic so will have to maybe delete all the
# lines with characters that aren't part of those 28?
#Potentially need to make the image reading better

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

def create_one_hot(labels):
    done_labels = {}
    for label in labels:
        if label not in done_labels:
            done_labels[label] = len(done_labels)
    return done_labels

def get_batch(image_dir, label_dict, batch_size, width, height, channels):
    image_batch = []
    label_batch = []
    for i in range(batch_size):
        image_name = random.choice(os.listdir(image_dir))
        img = load_img(image_dir+'/'+image_name, grayscale=False)
        x = img_to_array(img)
        image_batch.append(x)
        label_batch.append(label_dict[image_name[0:image_name.find(".")]])
    return image_batch, label_batch

def to_one_hot(label_list):
    for labels in label_list:
        for i, label in enumerate(labels):
            temp = np.zeros(47, dtype=int)
            temp[label] = 1
            temp = temp.tolist()
            labels[i] = temp
    ans = []
    for sublist in label_list:
        for item in sublist:
            for i in item:
                ans.append(i)
    while len(ans) < 5875:
        ans.append(0)
    return ans

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config = config)
KTF.set_session(sess)

model = Sequential()
model.add(Conv2D(32, (3,3), activation='relu', input_shape=(None, None, 3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Dropout(.5))
model.add(SpatialPyramidPooling([1, 2, 4]))
model.add(Dense(5875, activation='sigmoid'))
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.adam(),
              metrics=['accuracy'])

image_dir = "/home/cheesecake/Desktop/KHATT_v1.0/LineImages_v1.0/FixedTextLineImages/Train"
label_path = '/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/FixedTextLinesLatinTransliteration/TrainLabels_Translated.txt'
height,width,channels = 256,256,3
batch_size = 1

label_list = get_labels(label_path).values()
all_labels = []
for i in label_list:
    for j in i:
        all_labels.append(j)

one_hot_dict = create_one_hot(all_labels)
one_hot_dict[''] = len(one_hot_dict)


for i in range(10000):
    image_batch, label_batch = get_batch(image_dir, get_labels(label_path), batch_size, width, height, channels)
    for i in range(1):
        image = image_batch[i]
        print(image.shape)


for i in range(1000):
    image_batch, label_batch = get_batch(image_dir, get_labels(label_path), batch_size, width, height, channels)
    for i in range(0):
        image = image_batch[i]
        plt.imshow(image, cmap='gray')
        plt.show()
    for i, image in enumerate(image_batch):
        image_batch[i] = image_batch[i].astype('float32')
        image_batch[i] = image_batch[i] / 255
    for labels in label_batch:
        for i,label in enumerate(labels):
            labels[i] = one_hot_dict[labels[i]]
    label_batch = to_one_hot(label_batch)
    image = image_batch[0]
    new_batch = np.zeros((1,image.shape[0],image.shape[1],image.shape[2]))
    new_batch[0,:,:,:] = image
    best_batch = []
    best_batch.append(label_batch)
    best_batch = np.array(best_batch)
    print(best_batch)
    model.fit(new_batch, best_batch, epochs=1)
    print('Nice!')