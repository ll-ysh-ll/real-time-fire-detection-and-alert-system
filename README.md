# Weapon Detection

Fire detection only using visiual inspection

#### YOLO v4 :
YOLO is a state-of-the-art, real-time object detection algorithm. In this notebook, we will apply the YOLO algorithm to detect objects in images. darknet prints out the objects it detected, its confidence, and how long it took to find them. We didn't compile Darknet with OpenCV so it can't display the detections directly. Instead, it saves them in predictions.png. You can open it to see the detected objects.

checkout [![@AlexeyAB](https://img.shields.io/badge/AlexeyAB-%20-black)](https://github.com/AlexeyAB/darknet) for more information on YOLO

#### Classes used for training :
- Fire

#### Dataset gathering and image annotation:

labeling tool: [![@labelImg](https://img.shields.io/badge/LabelImg-%20-blue)](https://github.com/tzutalin/labelImg)
#### Loss and mAP chart 
![App Screenshot](https://github.com/ll-ysh-ll/weapon-detection/blob/master/Screenshots/chart_yolov4-custom%20(4).png?raw=true)



## Screenshots

#### Fire Detection on Images
![App Screenshot](https://github.com/ll-ysh-ll/real-time-fire-detection-and-alert-system/blob/master/Screenshot/1.png?raw=true)
![App Screenshot](https://github.com/ll-ysh-ll/real-time-fire-detection-and-alert-system/blob/master/Screenshot/2.png?raw=true)
![App Screenshot](https://github.com/ll-ysh-ll/real-time-fire-detection-and-alert-system/blob/master/Screenshot/3.png?raw=true)
![App Screenshot](https://github.com/ll-ysh-ll/real-time-fire-detection-and-alert-system/blob/master/Screenshot/4.png?raw=true)

### To-do

- [x]  Dataset Gathering
- [x]  Image Annotation
- [x]  Model Training
- [ ]  E-mail Alert
- [ ]  Deployment Using Webapp


## Contact me

In any case if you need help feel free to contact me anytime

 yashkolekar008@gmail.com

 linkedin.com/in/yash-kolekar-559492116
