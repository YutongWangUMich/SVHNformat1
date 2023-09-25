# SVHN format 1 data downloader and accessories

install `mat73` for loading the label meta data
`pip install mat73`

to download the data, run
`python download_data.py`

generate the label meta data by
```
mkdir labels
python process_labels_train.py
python process_labels_test.py
```