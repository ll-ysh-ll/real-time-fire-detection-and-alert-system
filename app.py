import streamlit as st
import cv2
from PIL import Image,ImageEnhance
import numpy as np
import pandas as pd
import glob
import random
import os
import time
import pandas as pd
import pydub
import asyncio
import logging
import queue
import threading
import urllib.request
from pathlib import Path
from typing import List, NamedTuple
from image_detection import *
from video_detection import *
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import pydub
import streamlit as st
from aiortc.contrib.media import MediaPlayer
import av


@st.cache(persist=True)
def load_image(img):
    im = Image.open(img)
    return im


# Threshold Values
#Conf_threshold = 0.4
#NMS_threshold = 0.4

# Colours
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),(255, 255, 0), (255, 0, 255), (0, 255, 255),(255, 255, 255)]

@st.cache(persist=True)
def txt2str(text):
    txt=""
    for i in text:
        txt+=i+"\t"
    return txt


def main():
    """
    Fire Detection
    """
    st.title('Fire Detection 🤖')
    #st.text('Yolov4 and OpenCV')

    menu = ['Image','Video']
    choice = st.sidebar.selectbox('Menu',menu)

    if choice == 'Image':
        st.subheader('Image Detection')
        with st.spinner('Wait for the Weights and Configuration files to load'):
            time.sleep(1)
        st.success("Done!")
        image_file = st.file_uploader("Upload Image",type=['jpg', 'png', 'jpeg'])

        if image_file is not None:
            input_image = Image.open(image_file)
            st.text('Original Image')
            # st.write(type(input_image))
            st.image(input_image)

        # Fire Detection
        if st.button("Process"):
            result_img,text = yolo_objectdetection(input_image)
            st.image(result_img)
            # txt=txt2str(text)
            if text:
                st.error("Fire Detected")
            elif not text:
                st.success('No Fire')

    if choice == 'Video':
        video_detection()



if __name__ == '__main__':
    main()