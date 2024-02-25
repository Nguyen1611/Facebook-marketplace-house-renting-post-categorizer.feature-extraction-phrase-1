"""
FIll prediction into the data-updated.csv which then be uploaded to SQL server
SQL sever part is incomplete
"""

import numpy as np
import pandas as pd
import help_function

# Read the original CSV file
df = pd.read_csv('data-updated.csv')

# add new column
new_column_name = ['Style','Gym','Laundry_room']
for name in new_column_name:
    if name not in df.columns:
        df[name] = np.nan
        df.to_csv('test_data.csv', index=False)

# Extract the second column (index 1)
second_column = df.iloc[:, 1]
second_column = second_column.astype(str)  # convert to string

# Create a new DataFrame with only the second column
new_df = pd.DataFrame({'Second Column': second_column})

for index, value in new_df['Second Column'].items():
    # store images of each row in a list
    img_list = value.split(',')
    result = []
    sec_list = []

    # all picture per post
    for img in img_list:
        if img.lower() == 'nan':
            continue  # Skip processing if the URL is 'nan'
        location = help_function.Categorical_Classification(img)
        result.append(location)

    for i, loco in enumerate(result):
        if loco == 'Gym':
            df.loc[index, 'Gym'] = 'Yes'
        elif loco == 'Laundry_room':
            df.loc[index, 'Laundry_room'] = 'Yes'
        elif loco == 'livingSpace': # extract all living space image
            sec_list.append(i)  # Append the index of i to sec_list

    if sec_list:
        # counter
        modern = 0
        vintage = 0
        # loop through sec list which contain index of image in livingSpace
        for ind in sec_list:
            style = help_function.Binary_Classification(img_list[ind])
            if style == 'Error':
                continue
            elif style == 0:
                vintage += 1
            else:
                modern += 1

        if vintage > modern:
            df.loc[index, 'Style'] = 'Vintage'
        else:
            df.loc[index, 'Style'] = 'Modern'

df.to_csv('data-updated.csv', index=False)
