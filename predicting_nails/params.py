import os

LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), "code", "ariannamng",
                               "predicting_nail_diseases", 'raw_data')

LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), "code", "ariannamng",
                               "predicting_nail_diseases")


# Model
MODEL_TARGET = "local"
BUCKET_NAME = "predicting-nail-diseases"

LABLES_SIMPLE = {0: "Healthy nails",
                1: "Diseased nails",
    }
