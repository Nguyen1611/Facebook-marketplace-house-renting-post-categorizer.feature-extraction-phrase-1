import numpy as np
import tensorflow as tf
import os
import cv2
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing

# Function to get all the paths to each file in the folder
def get_files(directory):
    files = []
    for dirname, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files

# Load the model
loaded_model = tf.saved_model.load('../Location_classification')

# Get the test data and IDs
test = []
test_ids = []

for file in get_files('dataset_model2/model2_test_all'):
    img = cv2.imread(file)
    if img is None:
        img = plt.imread(file)
        img = img[..., ::-1]
        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)
    img_array = np.asarray(resized)
    test.append(img_array)
    test_ids.append(os.path.basename(file))  # Keep the original filename

test = np.array(test, dtype=object)
test = test.astype('float32') / 255.

# Get predictions
predictions = loaded_model(test)
predicted_class = np.argmax(predictions, axis=-1)

# Encode prediction
classes = ['Gym', 'Laundry_room', 'livingSpace', 'outdoor', 'toilet']
le = preprocessing.LabelEncoder()
le.fit(classes)
predicted_labels = le.inverse_transform(predicted_class)

# Create a DataFrame
df = pd.DataFrame({
    "ID": test_ids,
    "Predicted_Location": predicted_labels
})

# Save to CSV
df.to_csv('Location_classification_testAll.csv', index=False)
