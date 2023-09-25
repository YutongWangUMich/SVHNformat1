#!/usr/bin/env python
# coding: utf-8

# The SVHN label are stored in a matlab matrix.
# This requires a special dataloader: `mat73`

# In[3]:


# get_ipython().system('pip install mat73')


# In[4]:


import pandas as pd
import numpy as np
import mat73
digitStruct_file_path = "./data_raw/test/digitStruct.mat"
mat_data = mat73.loadmat(digitStruct_file_path)


# In[13]:


digitStruct = mat_data['digitStruct']
digitStruct.keys()


# `digitStruct` contains two keys
# - one stores the bounding boxes (`bbox`),
# - the other stores the names (`name`)

# In[21]:


bboxes = digitStruct['bbox']
names = digitStruct['name']
bbox_keys = bboxes[0].keys()
print(names[0])
print(bbox_keys)
print(bboxes[0])


# In[22]:


isinstance(names,list)


# Some images just have a singleton label, which is not stored as a list:

# In[30]:


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

# In[36]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    if not isinstance(bbox['height'], list):
        for key in bbox_keys:
            assert(isinstance(bbox[key], np.ndarray))
            bboxes[i][key] = [bbox[key]]


# Make sure we converted everything properly

# In[45]:


for key in bbox_keys:
    types = set([type(bbox[key]) for bbox in bboxes])
    assert(len(types)==1) # types = {<class 'list'>}
    assert(list(types)[0] == list)


# In[55]:


bbox = bboxes[i_bad]
print(type(bbox['height']))
[int(val.item()) for val in bbox['height']]


# Let's simplify the bboxes and remove those arrays

# In[56]:


for i in range(len(bboxes)):
    for key in bbox_keys:
        bbox = bboxes[i]
        bboxes[i][key] = [int(val.item()) for val in bbox[key]]


# Check for the bad example

# In[61]:


bbox = bboxes[i_bad]
bbox


# Also check for a good example

# In[63]:


bbox = bboxes[0]
bbox


# Let's simplify the data organization structure

# In[66]:


for i in range(len(bboxes)):
    bboxes[i]['name'] = names[i]
bboxes[0]


# There's another issue: zeros are encoded by "10"

# In[74]:


i_zero = 24
bboxes[i_zero]


# In[77]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    if 10 in bbox['label']:
        bboxes[i]['label'] = [0 if x == 10 else x for x in bbox['label']]


# In[78]:


i_zero = 24
bboxes[i_zero]


# In[86]:


# Function to calculate the smallest containing bounding box
def calculate_smallest_containing_box(info):
    # Extracting bounding box information from the dictionary
    lefts = info['left']
    tops = info['top']
    widths = info['width']
    heights = info['height']
    
    # Calculate the minimum and maximum coordinates
    min_left = min(lefts)
    min_top = min(tops)
    max_right = max(left + width for left, width in zip(lefts, widths))
    max_bottom = max(top + height for top, height in zip(tops, heights))
    
    # Calculate width and height of the containing box
    width = max_right - min_left
    height = max_bottom - min_top
    
    return min_left, min_top, width, height

crop_left, crop_top, crop_width, crop_height= calculate_smallest_containing_box(bboxes[i_zero])
for i in range(len(bboxes)):
    bbox = bboxes[i]
    crop_left, crop_top, crop_width, crop_height= calculate_smallest_containing_box(bbox)
    bboxes[i]["crop_left"] = crop_left
    bboxes[i]["crop_top"] = crop_top
    bboxes[i]["crop_width"] = crop_width
    bboxes[i]["crop_height"] = crop_height


# Finally, let us make a set of "unique sorted labels"

# In[92]:


for i in range(len(bboxes)):
    bbox = bboxes[i]
    bboxes[i]['unique_label'] = sorted(list(set(bbox['label'])))


# In[93]:


df = pd.DataFrame(bboxes)
cols = ['name'] + [col for col in df if col != 'name']
df = df[cols]

df.to_csv("labels/meta_data_test.csv")

