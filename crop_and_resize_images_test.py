#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
from PIL import Image
import os


# In[42]:


df = pd.read_csv('labels/meta_data_test.csv',index_col=0)


# In[43]:


meta_data = df


# In[44]:


# Path to the images directory
images_path = './data_raw/test'
save_path = './data_proc/test'


# In[ ]:


# Function to resize the image to 32x32
def resize_image(img_cropped):
    desired_size = (32, 32)
    img_resized = img_cropped.resize(desired_size, Image.ANTIALIAS)
    return img_resized

# Function to process and resize images
def process_and_resize_images(meta_data, images_path, save_path):
    for i, row in meta_data.iterrows():
        image_path = os.path.join(images_path, row['name'])
        with Image.open(image_path) as img:
            left, top, width, height = row['crop_left'], row['crop_top'], row['crop_width'], row['crop_height']
            img_cropped = img.crop((left, top, left + width, top + height))
            img_final = resize_image(img_cropped)
            img_save_path = os.path.join(save_path, f"cropped_{row['name']}")
            img_final.save(img_save_path)

# Calling the function to process and resize the images
process_and_resize_images(meta_data, images_path, save_path)

