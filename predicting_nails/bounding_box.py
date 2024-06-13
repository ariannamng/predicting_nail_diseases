from PIL import Image
from inference_sdk import InferenceHTTPClient
import base64
from io import BytesIO

def detect_nail_bounding_box(image_file: Image.Image) -> dict:
    # define the image url to use for inference by encoding image to base64
    buffered = BytesIO()
    image_file.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str =  base64.b64encode(img_byte).decode()

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="Uxxz9pxisnamCFMwzir8"
    )

    result = CLIENT.infer(img_str,model_id="nail-detection-rldlg/2")

    # define the coordinates of the box of the first prediction
    xl = result['predictions'][0]['x'] - (result['predictions'][0]['width']/2)
    yt = result['predictions'][0]['y'] - (result['predictions'][0]['height']/2)
    xr = result['predictions'][0]['x'] + (result['predictions'][0]['width']/2)
    yb = result['predictions'][0]['y'] + (result['predictions'][0]['height']/2)

    return (xl, xr, yt, yb)
