# SVHN format 1 data downloader and accessories
I assume you have `numpy` and `pandas`. Otherwise you need to install those.

To run everything
```
source unpack.sh
```

## To run things step by step
install `mat73` for loading the label meta data
```pip install mat73```

to download the data, run
```python download_data.py```

generate the label meta data by
```
mkdir labels
python process_labels_train.py
python process_labels_test.py
```

crop and resize images so that they are 32-by-32
```
mkdir data_proc/train
mkdir data_proc/test
python crop_and_resize_images_train.py
python crop_and_resize_images_test.py
```