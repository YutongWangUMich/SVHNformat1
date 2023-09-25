pip install mat73
python download_data.py
mkdir labels
python process_labels_train.py
python process_labels_test.py
mkdir data_proc/train
mkdir data_proc/test
python crop_and_resize_images_train.py
python crop_and_resize_images_test.py
