import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from gen_ai.gen_ai import question_pipeline_func
import requests
from PIL import Image
from predicting_nails.prediction.predict import predict
from streamlit_cropper import st_cropper



# Assume 'predict_disease' is a function from your CNN model module
#from model import predict_disease

# Page configuration
if 'stage' not in st.session_state:
    st.session_state.stage = 0

col1,  col2, temp1, temp2, col3 = st.columns([1,5,1,1,5])
# Add a picture under the header in column 1
col4, col5, col6 = st.columns([1,5,1])

if st.session_state.stage == 0:
    col2.markdown("# Nail Analysis")
    for i in range (0,7):
        col6.text("")
    # Image upload section
    image_path = "imagemsite.jpg"
    im1,  im2, im3 = st.columns([1,5,1])
    im2.image(image_path, caption='', use_column_width=True)
    col5.text("")
    col5.markdown("##### Upload an image to check if your nails are healthy")
# uploaded_image = col2.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="upload_image_button")


#if uploaded_image is not None:
    # Display the uploaded image
   # image = Image.open(uploaded_image)
    #image.convert('RGB').save('image.jpg')


def set_state(i):
    st.session_state.stage = i
botton1, botton2, botton3 = st.columns([5,2,5])
if st.session_state.stage == 0:
    botton2.button('start', on_click=set_state, args=[1])

if st.session_state.stage == 1: #cropping an image

    img_file = st.sidebar.file_uploader(label='Upload an image', type=['png', 'jpg','jpeg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    #box_color = st.sidebar.color_picker(label="Box Color", value='#AF0409')
    if img_file:
        st.markdown("##### Let's start by selecting the nail in your image")
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        image = st_cropper(img, realtime_update=realtime_update, box_color='#AF0409', return_type='image'
                                )
        tn1, tn2, tn3 = st.columns([5,2,5])
        # Manipulate cropped image at will
        st.write("Preview")
        tumbnail_ = image.thumbnail((150,150))
        tn1.image(image)


        image.save('image.jpg')


        tn3.text("")

        #col1.image(image, caption='Uploaded Image', use_column_width=True)
        tn3.button('save image and start prediction', on_click=set_state, args=[2])


if st.session_state.stage == 2: # prediction and Q&A
    botton1.markdown("# Nail Analysis")
    for i in range (0,1):
            botton1.text("")
    st.session_state.stage = 0
    with open('image.jpg', 'rb') as f:
        response = requests.post("https://nailpred-llcndp3loa-od.a.run.app/predict",files={'file':f}).json()

    prediction = response['pred']
    prob = response['prob']

    #prediction = 'Healthy nails'
    prob_rounded = np.round(prob, 3)*100
    # Display the prediction
    b1, b2 = st.columns([8,2])
    pred1, pred2, pred3 = st.columns([3,1,8])

    b2.button('new prediction', on_click=set_state, args=[1])
    for i in range (0,2):
            b2.text("")
    pred3.markdown("### Model Prediction")
    if prediction:

        pred1.image('image.jpg')
        pred3.success(f"{prediction}, probability {prob_rounded}%")

        for i in range (0,13):
            pred2.text("")
        # AI question and answer section
        st.markdown(f"#### Ask a Question about {prediction}")
        user_question = st.text_area("Enter your question here:")



        # Question and answers
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
    else:
        st.write("The model couldn't make a prediction for this image.")
        st.warning("You cannot ask a question until the model makes a prediction.")

        # Exit early if no prediction is available
        st.stop()
