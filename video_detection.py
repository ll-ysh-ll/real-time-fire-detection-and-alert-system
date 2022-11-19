import asyncio
import logging
import queue
import threading
import urllib.request
from pathlib import Path
from typing import List, NamedTuple
from PIL import Image
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import os
import av
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pydub
import streamlit as st
from aiortc.contrib.media import MediaPlayer
import glob
import time
import pandas as pd
import smtplib
# global start_time
start_time = int(time.time())

from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)




HERE = Path(__file__).parent

logger = logging.getLogger(__name__)


st.set_page_config(page_title="Fire Detection", page_icon="🔥")


WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={
        "video": True,
        "audio": True,
    },
)


def video_detection():

    
    st.subheader("Video Detection")

    with st.spinner('Wait for the Weights and Configuration files to load'):
        time.sleep(3)
    st.success('Done!')

    st.info("Please wait for 30-40 seconds for the webcam to load with the dependencies")

    app_object_detection()

    st.error('Please allow access to camera in order for this to work')
    #st.warning(
    #    'The object detection model might varies due to the server speed and internet speed')
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
    logger.debug("=== Alive threads ===")
    for thread in threading.enumerate():
        if thread.is_alive():
            logger.debug(f"  {thread.name} ({thread.ident})")


# Threshold Values
Conf_threshold = 0.4
NMS_threshold = 0.4

# Colours
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),(255, 255, 0), (255, 0, 255), (0, 255, 255),(255, 255, 255)]

# empty list
class_name = []

#Class names
NAMES = "./YOLOv4/obj.names"




# for reading all the datasets from the obj.names file into the array
with open(NAMES, 'rt') as f:
    class_name = f.read().rstrip('\n').split('\n')

# configration and weights file location - Server

model_config_file = './YOLOv4/yolov4-custom.cfg'
model_weight = './YOLOv4/backup/yolov4-custom_best.weights'


# darknet files
net = cv2.dnn.readNet(model_weight, model_config_file)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load Model
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

def email_alert():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    
    server.starttls()
    username = 'outofbox97@gmail.com'
    receiver = username
    # passwd = getpass.getpass()
    passwd = 'tgkdneiakaacpzci'
    server.login(username,passwd)


    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from datetime import datetime
    
    msg= MIMEMultipart()
    msg['from'] = 'FireDetectron'
    msg['to'] = 'outofbox97@gmail.com'
    msg['subject'] = "Fire Detected"
    text = "Fire Detected, have a look at image"
    msg.attach(MIMEText(text))
    F = glob.glob("mailing_images/*")
    
    count = 0
    for i in F:
        with open(i,'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('content-Disposition','attachment',filename='{}.jpg'.format(count+1))
                msg.attach(part)
    server.sendmail(username,receiver,msg.as_string())


def app_object_detection():
    class Video(VideoProcessorBase):
        def __init__(self):
            self.start_time = int(time.time())

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            image = frame.to_ndarray(format="bgr24")
            classes, scores, boxes = model.detect(
                image, Conf_threshold, NMS_threshold)
            label=None
            for (classid, score, box) in zip(classes, scores, boxes):

                color = COLORS[int(classid) % len(COLORS)]

                label = "%s : %f" % (class_name[classid[0]], score)

                cv2.rectangle(image, box, color, 1)
                cv2.putText(image, label, (box[0], box[1]-10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            if label:
                if label[:4]=="Fire" and (self.start_time+5)<int(time.time()):
                    im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    Image.fromarray(im_rgb).save('mailing_images/prediction.jpg')
                    self.start_time=int(time.time())+5
                    # email_alert()
                    print("Email Send")



            return av.VideoFrame.from_ndarray(image, format="bgr24")

    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_processor_factory=Video,
        async_processing=True,
    )

    

DEBUG = os.environ.get("DEBUG", "false").lower() not in [
    "false", "no", "0"]

logging.basicConfig(
    format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
    "%(message)s",
    force=True,
)

logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

st_webrtc_logger = logging.getLogger("streamlit_webrtc")
st_webrtc_logger.setLevel(logging.DEBUG)

fsevents_logger = logging.getLogger("fsevents")
fsevents_logger.setLevel(logging.WARNING)

