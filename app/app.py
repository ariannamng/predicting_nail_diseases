import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from gen_ai.gen_ai import ask_questions


col1, col2 = st.columns([4,4])
# Assume 'predict_disease' is a function from your CNN model module
#from model import predict_disease

# Page configuration
col1.markdown("# Nail Analysis :)")

# Add a picture under the header in column 1
image_path = "imagemsite.jpg"
col1.image(image_path, caption='steps to capture a clear nail image', use_column_width=True)

# Image upload section
col2.markdown("### Upload an image to check if your nails are healthy")
uploaded_image = col2.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="upload_image_button")


if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Predict disease using the CNN model
    #TODO prediction = predict_disease(image) ---->> comment this out when  MODEL IS READY
    prediction = 'Healthy nails'

    # Display the prediction
    st.markdown("### Model Prediction")
    if prediction:
        st.write(f"The model predicts: **{prediction}**")
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
        response = ask_questions("Healthy nails")#change this to the prediction
        st.markdown("#### AI Response:")
        st.write(response)
    else:
        st.warning("Please enter a question before clicking the button.")
# bottom text
st.markdown("This application is designed for educational purposes only, not as medical advice. The neural network predicts diseases from images, while the AI transformer answers questions about those diseases. Users should use it with awareness of its limitations and academic context.", unsafe_allow_html=True)
