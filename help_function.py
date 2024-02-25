"""
Help function to perform prediction which then being used in main
"""
import requests
import numpy as np
import tensorflow as tf
import cv2
from matplotlib import pyplot as plt

# this function take 1 link and return the result of binary classification 0 and 1 (modern or vintage)
# outdoor)
def Binary_Classification(url):
    try:
        # gets all the files as image arrays
        test = []

        # Download image from URL
        response = requests.get(url)
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Ensure correct color channels (convert from RGB to BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
        img_array = np.asarray(resized)
        test.append(img_array)

        test = np.array(test, dtype=object)
        test = test.astype('float32') / 255.

        loaded_model = tf.saved_model.load('Home_style_binary_classification')
        predictions = loaded_model(test)
        rounded_predictions = tf.round(predictions).numpy().astype(int).flatten()

        return rounded_predictions[0]
    except Exception as e:
        print(f"Error processing image at URL {url}: {str(e)}")
        return 'Error'


import requests
import numpy as np
import tensorflow as tf
import cv2
from matplotlib import pyplot as plt
from sklearn import preprocessing

# this function return 5 of categories (Gym, outdoor, livingSpace, toilet, Laundry_room)
def Categorical_Classification(url):
    try:
        test = []

        # Download image from URL
        response = requests.get(url)
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Ensure correct color channels (convert from RGB to BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
        img_array = np.asarray(resized)
        test.append(img_array)

        test = np.array(test, dtype=object)
        test = test.astype('float32') / 255.

        loaded_model = tf.saved_model.load('Location_classification')
        predictions = loaded_model(test)
        predicted_class = np.argmax(predictions, axis=-1)

        # Encode prediction
        classes = ['Gym', 'Laundry_room', 'livingSpace', 'outdoor', 'toilet']
        le = preprocessing.LabelEncoder()
        le.fit(classes)
        predicted_labels = le.inverse_transform(predicted_class)

        return predicted_labels[0]
    except Exception as e:
        print(f"Error processing image at URL {url}: {str(e)}")
        return 'Error'
