
import os
import shutil
from sklearn.model_selection import train_test_split

# list folder/directories in to the train path
os.listdir('dataset_model2')
os.listdir('dataset_model2/model2_train')


root_directory = 'dataset_model2/model2_train'

# Get the names of the subdirectories (categories)
categories = os.listdir(root_directory)

# Define the split ratios (e.g., 80% training, 10% validation, 10% test)
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# Create destination directories for train, validation, and test sets
train_directory = 'dataset_model2/model2_train/train_set'
val_directory = 'dataset_model2/model2_train/val_set'
test_directory = 'dataset_model2/model2_train/test_set'

# Create destination directories if they don't exist
os.makedirs(train_directory, exist_ok=True)
os.makedirs(val_directory, exist_ok=True)
os.makedirs(test_directory, exist_ok=True)

# Iterate through each category
for category in categories:
    category_directory = os.path.join(root_directory, category)

    # Get the list of images in the category
    images = os.listdir(category_directory)

    # Split the images into train, validation, and test sets
    train_images, test_images = train_test_split(images, test_size=val_ratio + test_ratio, random_state=42)

    # Move images to their respective directories
    for img in train_images:
        src = os.path.join(category_directory, img)
        dest = os.path.join(train_directory, category, img)
        shutil.copy(src, dest)

    for img in test_images:
        src = os.path.join(category_directory, img)
        dest = os.path.join(test_directory, category, img)
        shutil.copy(src, dest)
