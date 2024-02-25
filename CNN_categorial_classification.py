"""
This model will extract feature and labeling different feature of images
"""
import numpy as np  # linear algebra
from keras import Model
from keras.src.applications import VGG16
from keras.src.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import os


# list folder/directories in to the train path
os.listdir('dataset_model2')
os.listdir('dataset_model2/model2_train')

# test file loader
# get all the paths to each file in the folder
def get_files(directory):
    files = []
    for dirname, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


# gets all the files as image arrays
test = []
for file in get_files('dataset_model2/model2_test'):
    img = cv2.imread(file)
    # sometimes cv2 does not read jpg files correctly, so when that happens, use pyplot and change to BGR
    # convert 4 color channel image to RGB
    if (img is None):
        # print(file)
        img = plt.imread(file)
        img = img[..., ::-1]
        if len(img.shape) > 2 and img.shape[2] == 4:
            # convert the image from RGBA2RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
    img_array = np.asarray(resized)
    test.append(img_array)

test = np.array(test, dtype=object)
test = test.astype('float32') / 255.


# vgg16 model
image_shape = (256,256,3)
batch_size = 128

# data augmentation
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=25,
    width_shift_range=0.1,
    rescale=1/255,
    shear_range=0.1,
    height_shift_range=0.2,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest')

# auto set label using keras flow_from directory
train_gen = datagen.flow_from_directory('dataset_model2/model2_train', target_size=image_shape[:2],
                                        color_mode='rgb', batch_size=batch_size, class_mode='categorical')
test_gen = datagen.flow_from_directory('dataset_model2/model2_test', target_size=image_shape[:2],
                                         color_mode='rgb', batch_size=batch_size, class_mode='categorical')


base_model = VGG16(weights='imagenet', include_top=False, input_shape=image_shape)
base_model.trainable = False
x = base_model.output
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
output = Dense(5, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics='accuracy')
es = EarlyStopping(monitor='val_accuracy', mode='max', patience=10)
model.fit(train_gen, validation_data=test_gen, epochs=20, )
model.evaluate(test)

tf.saved_model.save(model, "Location_classification")
