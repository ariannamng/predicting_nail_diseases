import os
from tensorflow import keras

LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), "code", "ariannamng",
                               "predicting_nail_diseases", 'raw_data')

LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), "code", "ariannamng",

                               "predicting_nail_diseases", "models")



# Model
MODEL_TARGET = "local"
BUCKET_NAME = "predicting-nail-diseases"
