import streamlit as st
import webbrowser
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
from weight_downloader import *
download_weight()
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

FILE_LIST = os.listdir("./yolov4/backup")
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
            # if not "yolov4-custom_best.weights" in file_list:
            #     os.system('wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O- | sed -rn "s/.*confirm=([0-9A-Za-z_]+).*/\1\n/p")&id=1K0kaVCRTNRDaYdnRaX9MUGu4OZf3G1cv" -O yolov4-custom_best.weights && rm -rf /tmp/cookies.txt')
            #     os.system('mv ./yolov4-custom_best.weights ./YOLOv4/backup/')
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
        st.subheader("Author")
        st.markdown(
            '''
            
            I'm yash, ML-AI Enthusiast & Freelancer.
        
            🎓 Graduated With Major in Computer Science & Engineering from DYPCET.

            📫 How to reach me:

            - [![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/users/289725455395848194) 

            - [![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:yashkolekar008@gmail.com) 

            - [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yash-kolekar-559492116/) 
            '''
        )
        st.info("Feel free to edit with the source code and enjoy coding")
    if choice == 'Video':
        video_detection()



if __name__ == '__main__':
    main()