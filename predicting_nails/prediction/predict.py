import os
import numpy as np
from predicting_nails.params import *
from PIL import Image
import glob
from colorama import Fore, Style
from tensorflow import keras

from google.cloud import storage
# from preprocessing import preprocesssing_user_image
categories = ['normal', 'beau_s line', 'black line', 'clubbing', 'mees_ line', 'onycholysis', 'terry_s nail', 'white spot']
friendly_names = {
    'normal': 'Healthy nail',
    'beau_s line': 'Beaus line',
    'black line': 'Black line',
    'clubbing': 'Clubbing',
    'mees_ line': 'Mees line',
    'onycholysis': 'Onycholysis',
    'terry_s nail': 'Terry\'s nail',
    'white spot': 'White spot'
}
def load_model() -> keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'
    Return None (but do not Raise) if no model is found
    """

    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Get the latest model version name by the timestamp on disk
        local_model_directory = os.path.join(LOCAL_REGISTRY_PATH)
        local_model_paths = glob.glob(f"{local_model_directory}/*")

        if not local_model_paths:
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

        latest_model = keras.models.load_model(most_recent_model_path_on_disk)


        print("✅ Model loaded from local disk")

        return latest_model

    elif MODEL_TARGET == "gcs":
        print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

        client = storage.Client()
        blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))

        try:
            latest_blob = max(blobs, key=lambda x: x.updated)
            latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, latest_blob.name)
            latest_blob.download_to_filename(latest_model_path_to_save)

            latest_model = keras.models.load_model(latest_model_path_to_save)

            print("✅ Latest model downloaded from cloud storage")

            return latest_model
        except:
            print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")

            return None


def predict(img):
    """
    Preprocess the image.
    Make a binary prediction of healthy and diseases nails.
    """
    #X_processed = preprocesssing_user_image(X_pred)
    #img = Image.open(image)
    foo = img.resize((256,256))
    img_array = keras.utils.img_to_array(foo)
    X_reshaped = img_array.reshape((-1, 256, 256, 3))
    X_processed = X_reshaped/255.0 - 0.5

    model = load_model()


    try:
        result = model.predict(X_processed)[0]
        max_prob = np.max(result)
        prediction = ""
        prob = 0

        if result[0] == max_prob:
            prediction = 'normal'
            prob = result[0]
        elif result[1] == max_prob:
            prediction = 'beau_s line'
            prob = result[1]
        elif result[2] == max_prob:
            prediction = 'black line'
            prob = result[2]
        elif result[3] == max_prob:
            prediction = 'clubbing'
            prob = result[3]
        elif result[4] == max_prob:
            prediction = 'mees_ line'
            prob = result[4]
        elif result[5] == max_prob:
            prediction = 'onycholysis'
            prob = result[5]
        elif result[6] == max_prob:
            prediction = 'terry_s nail'
            prob = result[6]
        elif result[7] == max_prob:
            prediction = 'white spot'
            prob = result[7]

        friendly_name = friendly_names[prediction]
        prob = np.round(prob, 3)

        if prediction != 'normal':
            disease_status = 'Disease'
            print(f"The prediction is '{disease_status}: {friendly_name}' with {prob*100}% probability.")
            return disease_status, friendly_name, prob
        else:
            print(f"The prediction is '{friendly_name}' with {prob*100}% probability.")
            return friendly_name, prob
    except Exception as e:
        print(f"\n❌ Prediction failed. Check your models. Error: {e}")
        return None, None



    #     friendly_name = friendly_names[prediction]
    #     prob = np.round(prob, 3)
    #     print(f"The prediction is '{friendly_name}' with {prob*100}% probability.")
    #     return friendly_name, prob
    # except Exception as e:
    #     print(f"\n❌ Prediction failed. Check your models. Error: {e}")
    #     return None, None

    # try:
    #     result = model.predict(X_processed)[0]
    #     prediction_idx = np.argmax(result)
    #     prediction = categories[prediction_idx]
    #     prob = np.round(result[prediction_idx], 3)
    #     print(f"The prediction is '{prediction}' with {prob*100}% probability.")
    #     return prediction, prob
    # except Exception as e:
    #     print(f"\n❌ Prediction failed. Check your models. Error: {e}")
    #     return None, None

    # try:
    #     result = model.predict(X_processed)[0][0]
    #     print(result)
    #     if(result < 0.5):
    #       prediction = "Healthy nails"
    #       prob = np.round(1-result,3)
    #     if(result >= 0.5):
    #       prediction = "diseased nail"
    #       prob = np.round(result,3)
    #     #return LABLES_SIMPLE[y_pred]
    #     print("The prediction is a", prediction,"with", prob*100, "% probability.")
    #     return prediction, prob
    # except:
    #     print("\n❌ Prediction failed. Check your models")
