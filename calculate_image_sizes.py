#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import csv
from PIL import Image
import sys

tort = sys.argv[1]

image_dir = f"./data_raw/{tort}"
csv_output_file_path = f"./data_proc/img_dims_{tort}.csv"


def create_image_csv(img_dir, csv_filename):
    # Ensure the directory ends with a separator
    if not img_dir.endswith(os.sep):
        img_dir += os.sep
    
    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'width', 'height']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header to the CSV file
        writer.writeheader()

        # Get all png files and sort them
        filenames = sorted([f for f in os.listdir(img_dir) if f.endswith('.png')],
                          key=lambda x: int(x.split('.')[0]))  # Sorting by converting filename to integer

        # Iterate through all PNG files in the directory
        for filename in filenames:
            filepath = os.path.join(img_dir, filename)
                
            # Open the image and get its dimensions
            with Image.open(filepath) as img:
                width, height = img.size
                
            # Write the name and dimensions to the CSV file
            writer.writerow({'name': filename, 'width': width, 'height': height})

# Example usage
create_image_csv(image_dir, csv_output_file_path)

