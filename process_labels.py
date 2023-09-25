#!/usr/bin/env python
# coding: utf-8

# The SVHN label are stored in a matlab matrix.
# This requires a special dataloader: `mat73`

# In[128]:


# get_ipython().system('pip install mat73')


# In[129]:


import pandas as pd
import numpy as np
import mat73
import sys
# tort = "train"
tort = sys.argv[1]
digitStruct_file_path = f"./data_raw/{tort}/digitStruct.mat"
img_dims = pd.read_csv(f"data_proc/img_dims_{tort}.csv")
mat_data = mat73.loadmat(digitStruct_file_path)


# In[130]:


digitStruct = mat_data['digitStruct']
digitStruct.keys()


# `digitStruct` contains two keys
# - one stores the bounding boxes (`bbox`),
# - the other stores the names (`name`)

# In[131]:


bboxes = digitStruct['bbox']
names = digitStruct['name']
bbox_keys = bboxes[0].keys()
print(names[0])
print(bbox_keys)
print(bboxes[0])


# In[132]:


isinstance(names,list)


# Some images just have a singleton label, which is not stored as a list:

# In[133]:


i_bad = None
for i in range(len(bboxes)):
    bbox = bboxes[i]
    if not isinstance(bbox['height'], list):
        print(i)
        i_bad = i
        break
bbox = bboxes[i_bad]
print(type(bbox['height']))
assert(isinstance(bbox['height'],np.ndarray))
bbox


# Let us fix this

# In[134]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    if not isinstance(bbox['height'], list):
        for key in bbox_keys:
            assert(isinstance(bbox[key], np.ndarray))
            bboxes[i][key] = [bbox[key]]


# Make sure we converted everything properly

# In[135]:


for key in bbox_keys:
    types = set([type(bbox[key]) for bbox in bboxes])
    assert(len(types)==1) # types = {<class 'list'>}
    assert(list(types)[0] == list)


# In[136]:


bbox = bboxes[i_bad]
print(type(bbox['height']))
[int(val.item()) for val in bbox['height']]


# Let's simplify the bboxes and remove those arrays

# In[137]:


for i in range(len(bboxes)):
    for key in bbox_keys:
        bbox = bboxes[i]
        bboxes[i][key] = [int(val.item()) for val in bbox[key]]


# Check for the bad example

# In[138]:


bbox = bboxes[i_bad]
bbox


# Also check for a good example

# In[139]:


bbox = bboxes[0]
bbox


# Let's simplify the data organization structure

# In[140]:


for i in range(len(bboxes)):
    bboxes[i]['name'] = names[i]
bboxes[0]


# There's another issue: zeros are encoded by "10"

# In[141]:


i_zero = 24
bboxes[i_zero]


# In[142]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    if 10 in bbox['label']:
        bboxes[i]['label'] = [0 if x == 10 else x for x in bbox['label']]


# In[143]:


i_zero = 24
bboxes[i_zero]


# In[ ]:





# In[150]:


def calculate_smallest_containing_square(bbox_data, img_width, img_height):
    """
    Get the smallest square or rectangle that contains all bounding boxes.
    
    :param bbox_data: Dictionary containing 'left', 'top', 'width', 'height' of bounding boxes.
    :param img_width: Width of the image.
    :param img_height: Height of the image.
    :return: Coordinates (left, top, width, height) of the square or rectangle.
    """
    left = bbox_data['left']
    top = bbox_data['top']
    width = bbox_data['width']
    height = bbox_data['height']
    
    # Getting the minimum and maximum x and y coordinates among all bounding boxes
    min_x = min(left)
    min_y = min(top)
    max_x = max([l + w for l, w in zip(left, width)])
    max_y = max([t + h for t, h in zip(top, height)])
    
    # Calculating the width and height of the rectangle formed by these points
    rect_width = max_x - min_x
    rect_height = max_y - min_y
    
    # Taking the maximum of the width and height to determine the side length of the square
    side_length = max(rect_width, rect_height)
    
    # Centering the square
    square_left = min_x - (side_length - rect_width) / 2
    square_top = min_y - (side_length - rect_height) / 2
    
    # Intersecting the square with the image dimensions
    square_left = max(square_left, 0)
    square_top = max(square_top, 0)
    square_width = min(side_length, img_width - square_left)
    square_height = min(side_length, img_height - square_top)
    
    return square_left, square_top, square_width, square_height

for i in range(len(bboxes)):
    bbox = bboxes[i]
    assert(img_dims.loc[i]['name'] == names[i])
    img_width = img_dims.loc[i]['width']
    img_height = img_dims.loc[i]['height']
    crop_left, crop_top, crop_width, crop_height= calculate_smallest_containing_square(bbox,img_width,img_height)
    bboxes[i]["crop_left"] = crop_left
    bboxes[i]["crop_top"] = crop_top
    bboxes[i]["crop_width"] = crop_width
    bboxes[i]["crop_height"] = crop_height


# Finally, let us make a set of "unique sorted labels"

# In[151]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    bboxes[i]['unique_label'] = sorted(list(set(bbox['label'])))


# In[152]:


df = pd.DataFrame(bboxes)
cols = ['name'] + [col for col in df if col != 'name']
df = df[cols]

df.to_csv(f"./labels/meta_data_{tort}.csv")


# In[153]:


df[['name', 'unique_label']].to_csv(f"./labels/labels_{tort}.csv",index=False)

