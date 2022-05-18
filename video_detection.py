import asyncio
import logging
import queue
import threading
import urllib.request
from pathlib import Path
from typing import List, NamedTuple

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

import time
import pandas as pd


from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)


st.set_page_config(page_title="Shazam for Food", page_icon="🍗")


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

#Coco - Server
COCO = "./obj.names"

#Coco - Local
#COCO = "models\\coco.names"


# for reading all the datasets from the coco.names file into the array
with open(COCO, 'rt') as f:
    class_name = f.read().rstrip('\n').split('\n')

# configration and weights file location - Server
model_config_file = "./yolov4-custom.cfg"
model_weight = "./backup/yolov4-custom_best.weights"

# configration and weights file location - Local
#model_config_file = "models\\yolov4-tiny.cfg"
#model_weight = "models\\yolov4-tiny.weights"


# darknet files
net = cv2.dnn.readNet(model_weight, model_config_file)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load Model
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)


def app_object_detection():

    class Video(VideoProcessorBase):

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            image = frame.to_ndarray(format="bgr24")

            classes, scores, boxes = model.detect(
                image, Conf_threshold, NMS_threshold)
            for (classid, score, box) in zip(classes, scores, boxes):

                color = COLORS[int(classid) % len(COLORS)]

                label = "%s : %f" % (class_name[classid[0]], score)

                cv2.rectangle(image, box, color, 1)
                cv2.putText(image, label, (box[0], box[1]-10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)

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

