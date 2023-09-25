import os
import requests
import tarfile

def download_file(url, local_filename):
    """Download a file from a URL to a local filename."""
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def extract_tar_gz(tar_gz_path, extract_path='.'):
    """Extract a .tar.gz file to a specified path."""
    with tarfile.open(tar_gz_path, 'r:gz') as file:
        file.extractall(path=extract_path)

def download_and_extract(url, tar_gz_path, extract_path='.'):
    """Download a .tar.gz file from a URL and extract it."""
    print(f"Downloading {url}")
    download_file(url, tar_gz_path)
    print(f"Extracting zip file at {tar_gz_path}")
    extract_tar_gz(tar_gz_path, extract_path)
    os.remove(tar_gz_path)  # Remove the downloaded tar.gz file

try:
    print("Creating directory 'data_raw'.")
    os.mkdir('data_raw')
except FileExistsError:
    print("Directory 'data_raw' already exists.")

try:
    print("Creating directory 'data_proc'.")
    os.mkdir('data_proc')
except FileExistsError:
    print("Directory 'data_proc' already exists.")

# Example usage

urls = ["http://ufldl.stanford.edu/housenumbers/train.tar.gz",
        "http://ufldl.stanford.edu/housenumbers/test.tar.gz"]
tar_gz_paths = ['data_raw/train.tar.gz', 'data_raw/test.tar.gz']
extract_paths = ['data_raw', 'data_raw']

for i in range(len(urls)):
    print(f"{urls[i]}")
    download_and_extract(urls[i], tar_gz_paths[i], extract_paths[i])
