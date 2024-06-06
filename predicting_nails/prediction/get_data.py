import os
import numpy as np
from predicting_nails.params import *
from PIL import Image

def download_bucket_objects(bucket_name, blob_path, local_path):
    # blob path is bucket folder name
    command = "gsutil cp -r gs://{bucketname}/{blobpath} {localpath}".format(bucketname = bucket_name, blobpath = blob_path, localpath = local_path)
    os.system(command)
    return command

# Define the bucket name and the blob_path and load the data from GBP to a local directory
def get_data():
    local_dir = os.path.join(LOCAL_DATA_PATH, "dataset_for_model_1")
    if os.path.exists(local_dir) == False:
        bucket_name = 'predicting-nail-diseases' # do not use gs://
        for i in range(0,50):
            try:
                blob_path_h = f'dataset_for_model_1/healthy_data/healthy_{i}.JPG' # blob path in bucket where healthy data is stored
                local_dir = os.path.join(LOCAL_DATA_PATH, "dataset_for_model_1", f"healthy_{i}.JPG") # path to the RAW data foldr from .env
                download_bucket_objects(bucket_name, blob_path_h, local_dir)
                blob_path_d = f'dataset_for_model_1/diseased_data/diseased_{i}.JPG' # blob path in bucket where diseased data is stored
                local_dir = os.path.join(LOCAL_DATA_PATH, "dataset_for_model_1", f"diseased_{i}.JPG") # path to the RAW data foldr from .env
                download_bucket_objects(bucket_name, blob_path_d, local_dir)
            except:
                pass
get_data()

def load_simple_data(path, nb_healthy = 50, nb_disease = 50):

    X, y = [], []

    for i in range(nb_healthy):
        h_path = os.path.join(path, 'dataset_for_model_1', f'healthy_{i}.JPG')
        img = Image.open(h_path)
        foo = img.resize((224,224))
        X.append(np.array(foo))
        y.append(0)

    for i in range(nb_disease):
        d_path = os.path.join(path, 'dataset_for_model_1', f'diseased_{i}.JPG')
        img = Image.open(h_path)
        foo = img.resize((224,224))
        X.append(np.array(foo))
        y.append(1)

    c = list(zip(X, y))
    np.random.shuffle(c)
    X, y = zip(*c)

    return np.array(X), np.array(y)
