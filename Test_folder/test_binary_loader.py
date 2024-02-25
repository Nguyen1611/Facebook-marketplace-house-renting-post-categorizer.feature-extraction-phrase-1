import numpy as np
import tensorflow as tf
import os
import cv2
from matplotlib import pyplot as plt
import csv


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
for file in get_files('dataset_model1/predict'):
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

loaded_model = tf.saved_model.load('../Home_style_binary_classification')
predictions = loaded_model(test)

# Round predictions to 0 or 1
rounded_predictions = tf.round(predictions).numpy().astype(int).flatten()

# Get the list of picture names from the 'dataset/predict' directory
picture_names = [os.path.basename(file) for file in get_files('dataset_model1/predict')]

# Create a list of tuples (picture_name, binary_prediction)
result_data = list(zip(picture_names, rounded_predictions))

# Save the result to a CSV file
output_csv = 'BinaryClassification_testAll.csv'
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['Picture', 'Prediction']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for picture, prediction in result_data:
        if prediction == 1:
            writer.writerow({'Picture': picture, 'Prediction': 'modern'})
        elif prediction == 0:
            writer.writerow({'Picture': picture, 'Prediction': 'vintage'})
        else: # if null value
            writer.writerow({'Picture': picture, 'Prediction': prediction})
print(f"Predictions saved to {output_csv}")