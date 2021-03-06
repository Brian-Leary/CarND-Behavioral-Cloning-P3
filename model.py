import csv
import cv2
import numpy as np

lines = []
with open('./day1_udacity/driving_log.csv') as csvfile:
  reader = csv.reader(csvfile)
  for line in reader:
    lines.append(line)

images = []
measurements = []
for line in lines:
    source_path = line[0]
    tokens = source_path.split('/')
    filename = tokens[-1]
    local_path = './day1_udacity/IMG/' + filename
    image = cv2.imread(local_path)
    images.append(image)
    measurement = float(line[3])
    measurements.append(measurement)

print(len(images))
print(len(measurements))

augmented_images = []
augmented_measurements = []
for image, measurement in zip(images, measurements):
  augmented_images.append(image)
  augmented_measurements.append(measurement)
  augmented_images.append(cv2.flip(image, 1))
  augmented_measurements.append(measurement * -1.0)

print()
print(len(augmented_images))
print(len(augmented_measurements))

# an alternative method for flipping images
# image_flipped = np.fliplr(image)
# measurement_flipped = -measurement

X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

import keras
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Flatten, Dense, Lambda, Dropout
from keras.layers.convolutional import Convolution2D, Cropping2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
# normalize images to a range of -0.5 to 0.5
model.add(Lambda(lambda x: (x / 255.0) - 0.5, input_shape = (160, 320, 3)))
# set up cropping2D layer; remove 70 from top and 25 from bottom
model.add(Cropping2D(cropping = ((70, 25), (0, 0))))
model.add(Convolution2D(24, 5, 5, subsample = (2, 2), activation = 'relu'))
model.add(Convolution2D(36, 5, 5, subsample = (2, 2), activation = 'relu'))
model.add(Convolution2D(48, 5, 5, subsample = (2, 2), activation = 'relu'))
model.add(Convolution2D(64, 3, 3, activation = 'relu'))
model.add(Convolution2D(64, 3, 3, activation = 'relu'))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(100))
model.add(Dropout(0.5))
model.add(Dense(50))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Dropout(0.5))
model.add(Dense(1))

# mean squared error
model.compile(optimizer = 'adam', loss = 'mse')
model.fit(X_train, y_train, validation_split = 0.2, shuffle = True, nb_epoch = 10)

# save model to download to local machine later
model.save('model.h5')
