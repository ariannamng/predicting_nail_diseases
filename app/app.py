import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from gen_ai.gen_ai import question_pipeline_func
import requests
from PIL import Image
from predicting_nails.prediction.predict import predict


col1, col2 = st.columns([4,4])
# Assume 'predict_disease' is a function from your CNN model module
#from model import predict_disease

# Page configuration
col1.markdown("# Nail Analysis :)")

# Add a picture under the header in column 1
image_path = "imagemsite.jpg"
col1.image(image_path, caption='steps to capture a clear nail image - Generated by AI', use_column_width=True)

# Image upload section
col2.markdown("### Upload an image to check if your nails are healthy")
uploaded_image = col2.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="upload_image_button")


if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    image.save('image.jpg')

    col1.image(image, caption='Uploaded Image', use_column_width=True)

    # Predict disease using the CNN model
    # prediction, prob = predict(image)

    with open('image.jpg', 'rb') as f:
        response = requests.post("http://127.0.0.1:8000/predict",files={'file':f}).json()

    prediction = response['pred']
    prob = response['prob']

    #prediction = 'Healthy nails'
    prob_rounded = np.round(prob, 3)*100
    # Display the prediction

    col2.markdown("### Model Prediction")
    if prediction:
        col2.write(f"**{prediction}, probability {prob_rounded}%**")
    else:
        st.write("The model couldn't make a prediction for this image.")
        st.warning("You cannot ask a question until the model makes a prediction.")

        # Exit early if no prediction is available
        st.stop()



# AI question and answer section
st.markdown("#### Ask a Question")
user_question = st.text_area("Enter your question here:")

if st.button("Get Answer"):
    if user_question:
        # Simulate a response from the AI (this should be replaced with actual AI inference code)
        response = requests.get("http://127.0.0.1:8000/answer_question", params={'prediction' : prediction , 'question' : user_question})#change this to the prediction
        st.markdown("#### AI Response:")

        st.write(response.json()['answer'])
         # Add space before the bottom text
        st.markdown("<br><br><br>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question before clicking the button.")
# bottom text
st.markdown("This application is designed for educational purposes only, not as medical advice. The neural network predicts diseases from images, while the AI transformer answers questions about those diseases.🤘", unsafe_allow_html=True)
