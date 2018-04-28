from __future__ import division, print_function, absolute_import

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
import tflearn
from tflearn.data_utils import to_categorical
import tflearn.data_utils as du
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import matplotlib.pyplot as plt
import matplotlib as matplot
import seaborn as sns
import random


trainx = pd.read_csv("/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/Arabic Handwritten Characters Dataset CSV/csvTrainImages 13440x1024.csv",header=None)
trainy = pd.read_csv("/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/Arabic Handwritten Characters Dataset CSV/csvTrainLabel 13440x1.csv",header=None)

testx = pd.read_csv("/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/Arabic Handwritten Characters Dataset CSV/csvTestImages 3360x1024.csv",header=None)
testy = pd.read_csv("/home/cheesecake/GAT/gat/scraping/ArabicTextExtractor/Arabic Handwritten Characters Dataset CSV/csvTestLabel 3360x1.csv",header=None)
# Split data into training set and validation set
#training images
trainx = trainx.values.astype('float32')
#training labels
trainy = trainy.values.astype('int32')-1
#testing images
testx = testx.values.astype('float32')
#testing labels
testy = testy.values.astype('int32')-1
original_trainy = trainy
#One Hot encoding of train labels.
trainy = to_categorical(trainy[:,0],28)
original_testy = testy
#One Hot encoding of test labels.
testy = to_categorical(testy[:,0],28)
# reshape input images to 28x28x1
trainx = trainx.reshape([-1, 32, 32, 1])
testx = testx.reshape([-1, 32, 32, 1])

arabic_labels = ['alef', 'beh', 'teh', 'theh', 'jeem', 'hah', 'khah', 'dal', 'thal',
                'reh', 'zain', 'seen', 'sheen', 'sad', 'dad', 'tah', 'zah', 'ain',
                'ghain', 'feh', 'qaf', 'kaf', 'lam', 'meem', 'noon', 'heh', 'waw', 'yeh']

#size of images should be 1200 by 2300


#@return - trainy_new: List of tuples that represent the corners of the 32x32 character box in clockwise order starting from top left
def get_image_batch(trainx, num_images):
    pad_left = random.randint(5,2265)
    pad_right = 2300-32-pad_left
    pad_top = random.randint(5,1165)
    pad_bottom = 1200-32-pad_top
    trainx_new = np.empty((num_images, pad_left + pad_right + 32, pad_top + pad_bottom + 32, 1))
    for i in range(num_images):
        index = random.randint(0 ,len(trainx)-1)
        trainx_new[i] = np.pad(trainx[index], ((pad_left, pad_right), (pad_top, pad_bottom), (0, 0)), 'constant')
    trainy_new = [(pad_left,pad_top),(2300-pad_right,pad_top),(2300-pad_right,1200-pad_bottom),(pad_left,1200-pad_bottom)]
    return trainx_new, trainy_new



for i in range(10):
    images, labels = get_image_batch(trainx,1)
    plt.imshow(images[0].squeeze().T)
    print(labels)
    plt.show()

#x = random.randint(0, 13440)
#plt.imshow(trainx_new[x].squeeze().T)
#plt.title(arabic_labels[original_trainy[x][0]])
#plt.show()

#Zero center every sample with specified mean. If not specified, the mean is evaluated over all samples.
trainx, mean1 = du.featurewise_zero_center(trainx)
testx, mean2 = du.featurewise_zero_center(testx)

print(trainx.shape, trainy.shape, testx.shape, testy.shape)

# Building convolutional network
network = input_data(shape=[None, 32, 32, 1], name='input')
network = conv_2d(network, 80, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = fully_connected(network, 1024, activation='relu')
network = dropout(network, 0.8)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.8)
network = fully_connected(network, 28, activation='softmax')
network = regression(network, optimizer='sgd', learning_rate=0.01,
                     loss='categorical_crossentropy', name='target')

#model complile
model = tflearn.DNN(network, tensorboard_verbose=0)
#model fitting
scores = []

for i in range(100):
    model.fit({'input': trainx}, {'target': trainy}, n_epoch=1,
           validation_set=({'input': testx}, {'target': testy}),
           snapshot_step=100, show_metric=True, run_id='convnet_arabic_digits')
    score = model.evaluate(testx, testy)
    print('Test accuracy: %0.2f%%' % (score[0] * 100))
    scores.append(score[0]*100)
    print(scores)
    x = list(range(len(scores)))
    y = []
    for el in x:
        y.append(el + 1)
    plt.plot(y, scores, 'k-')
    plt.title("Accuracy vs Epochs Trained")
    plt.xlabel("Num Epochs")
    plt.ylabel("Accuracy on Testing Data")
    plt.grid()
    plt.show(block=False)
    plt.pause(.1)

plt.savefig('AccuracyGraph.pdf')

print(scores)
