pip install mat73
python download_data.py
mkdir labels
mkdir data_proc/train
mkdir data_proc/test

python calculate_image_sizes.py train
python calculate_image_sizes.py test

python process_labels.py train
python process_labels.py test

python crop_and_resize_images.py train
python crop_and_resize_images.py test
