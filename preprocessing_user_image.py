# Importing Required Modules
from rembg import remove
from PIL import Image

def preprocessing_user_image(img):
    # img = Image.open(path)
    X_resized = img.resize((256,256))
    X = np.array(X_resized)

    X_normalized = X/255.0

    return X_normalized

def user_image_remove_background(img):

    # Store path of the image in the variable input_path
    input_path =  'raw_data/dataset_for_model_1/healthy_13.JPG'

    # Store path of the output image in the variable output_path
    output_path = 'raw_data/dataset_for_model_1/healthy_13_new.JPG'

    # Processing the image
    input = Image.open(input_path)

    # Removing the background from the given Image
    output = remove(input)

    output = output.convert("RGB")

    #Saving the image in the given path
    output.save(output_path)
