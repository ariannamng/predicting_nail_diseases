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
from predicting_nails.bounding_box import detect_nail_bounding_box


# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

def set_state(i):
    st.session_state.stage = i

# Page configuration
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'start' not in st.session_state:
    st.session_state.start = 0


if st.session_state.get("start")==1:
    img_file = st.sidebar.file_uploader(label='Upload an image', type=['png', 'jpg','jpeg'],key=st.session_state.get("key"), accept_multiple_files = False)
    if img_file and st.session_state.stage == 0:
        set_state(1)

# starting page
if st.session_state.stage == 0:
    st.markdown("# NAIL ANALYSIS")
    st.markdown("#### Early Nail Diseases Detection")
    for i in range (0,2):
        st.text("")

    st.markdown("""Welcome to nAil, your trusted partner in nail health!
                Our innovative AI software allows you to effortlessly monitor
                the health of your nails. Simply upload an image and use our easy
                cropping tool to ensure that primarily your nail is visible.
                Our advanced technology will then analyze the image to determine
                whether your nail is healthy or shows signs of disease. After
                receiving your result, you can chat with nAIl to further investigate
                the state of your nail and get personalized advice. Stay proactive
                about your nail health with quick, accurate assessments and interactive support from nAil.""", unsafe_allow_html=True)

    col4, col5, col6 = st.columns([1,5,1])
    for i in range (0,3):
        col6.text("")
    # Image upload section
    image_path = "imagemsite.png"
    st.image(image_path, caption='', use_column_width=True)
    col5.text("")
    col5.markdown("##### Upload an image to check if your nails are healthy")

    botton1, botton2, botton3 = st.columns([5.6,2,5])
    if st.session_state.get("start")==0:
        if botton2.button('start'):
            st.session_state.start=1
            st.rerun()

# cropping page
if st.session_state.stage == 1: #cropping an image
        if img_file:
            st.markdown("##### Select your nail in your image:")
            #st.markdown("!temp only one nail at the time can be analysed")
            st.text("")

            t1, t2 = st.columns([6,4])
            tn1, tn2, tn3 = st.columns([6,2,2])

            with tn1:
                img = Image.open(img_file)

                # try to use computer vision to detect the nail in the picture
                try:
                    default_coords = detect_nail_bounding_box(img)
                except:
                    default_coords = None

                # Show a image cropper tool that the user can interact with
                image = st_cropper(img, realtime_update = True, box_color='#FF8505',
                                aspect_ratio = None, default_coords=default_coords,
                                return_type='image',
                                should_resize_image = True
                                    )

            t2.text("")

            # show a reallife preview of the cropped image selection
            t2.write("Preview")
            tn2.image(image.resize((image.width*150//image.height,150)))

            st.session_state.image = image

            # "Scan" botton acceptes the user selection of the cropped image and starts prediction
            if tn3.button('scan'):
                set_state(2)
                st.rerun()

# prediction and Q&A page
if st.session_state.stage == 2:

    st.session_state.image.convert('RGB').save('image.jpg')
    with open('image.jpg', 'rb') as f:
        with st.spinner():
            response = requests.post("https://nailpred-llcndp3loa-od.a.run.app/predict",files={'file':f}).json()

    st.markdown("# NAIL ANALYSIS")
    st.markdown("####  Early Nail Diseases Detection")

    st.text("")

    prediction = response['pred']
    prob = response['prob']

    #prediction = 'Healthy nails'
    prob_rounded = np.round(prob, 3)*100
    # Display the prediction

    pred1, pred2, pred3 = st.columns([3,1,8])
    for i in range (0,2):
            st.text("")
    pred3.markdown("### Model's Prediction")
    if prediction:

        image = st.session_state.image
        pred1.text("")
        pred1.image(image.resize((image.width*150//image.height,150)))
        pred3.warning(f"{prediction}, probability {prob_rounded}%")
        if pred3.button('new prediction'):
            set_state(0)
            if st.session_state.get("key")==1:
                st.session_state.key=0
            else:
                st.session_state.key=1
            st.rerun()
        for i in range (0,13):
            pred2.text("")
        # AI question and answer section
        st.markdown(f"#### Ask a Question about {prediction}")
        user_question = st.text_area("Enter your question here:", placeholder= "e.g. how to take care of nails?")

        # Question and answers
        if st.button("Get Answer"):
            if user_question:
                    # Simulate a response from the AI (this should be replaced with actual AI inference code)
                    try:
                        response = requests.get("https://nailpred-llcndp3loa-od.a.run.app/answer_question", params={'prediction' : prediction , 'question' : user_question})#change this to the prediction
                        st.markdown("#### AI Response:")
                        st.warning(response.json()['answer'])
                    except:
                        st.error("Please enter a question before clicking the button.")
    else:
        st.write("The model couldn't make a prediction for this image.")
        st.warning("You cannot ask a question until the model makes a prediction.")

        # Exit early if no prediction is available
        st.stop()

# Add space before the bottom text
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("This application is designed for educational purposes only, not as medical advice. The neural network predicts diseases from images, while the AI transformer answers questions about those diseases.🤘", unsafe_allow_html=True)
