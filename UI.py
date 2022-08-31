import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
import getpass
import smtplib
import glob
from datetime import datetime
import matplotlib.image as mpimg
now = datetime.now().time()

class YOLO:

    def __init__(self, config, model, labels, size=416, confidence=0.5, threshold=0.3):
        self.confidence = confidence
        self.threshold = threshold
        self.size = size
        self.labels = labels
        self.net = cv2.dnn.readNetFromDarknet(config, model)

    def inference(self, image):
        ih, iw = image.shape[:2]

        ln = self.net.getLayerNames()
        # ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        ln = [ln[i-1] for i in self.net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.size, self.size), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(ln)
        end = time.time()
        inference_time = end - start

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > self.confidence:
                    box = detection[0:4] * np.array([iw, ih, iw, ih])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

        results = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                x, y = (boxes[i][0], boxes[i][1])
                w, h = (boxes[i][2], boxes[i][3])
                id = classIDs[i]
                confidence = confidences[i]

                results.append((id, self.labels[id], confidence, x, y, w, h))

        return iw, ih, inference_time, results
class Foo(object):
    counter = 0
    def __call__(self):
        Foo.counter += 1
        return(Foo.counter)
    
def email_alert():
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    
    server.starttls()
    username = 'saishkamat7@gmail.com'
    receiver = username
    # passwd = getpass.getpass()
    passwd = 'saish@1234'
    server.login(username,passwd)


    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from datetime import datetime
    
    msg= MIMEMultipart()
    msg['from'] = 'FireDetectron'
    msg['to'] = 'outofbox97@gmail.com'
    msg['subject'] = "Images"
    passwd = 'tgkdneiakaacpzci'
    text = "Found Fire, have a look at sample images"
    msg.attach(MIMEText(text))
    F = glob.glob("detected-images/*")
    
    count = 0
    for i in F:
        with open(i,'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('content-Disposition','attachment',filename='{}.jpg'.format(count+1))
                msg.attach(part)
    server.sendmail(username,receiver,msg.as_string())

    

def detect_objects(our_image):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    our_image = np.array(our_image)

    flag = 0
    col1, col2 = st.columns(2)
    
    yolo = YOLO("YOLOv4/yolov4-custom.cfg", "YOLOv4/backup/yolov4-custom_best.weights", ["Fire"]) 
    st.success("Model Loaded!!")
            
    col1.subheader("Original Image")
    st.text("")
    plt.figure(figsize = (15,15))
    plt.imshow(cv2.cvtColor(our_image, cv2.COLOR_BGR2RGB))
    plt.imshow(our_image)
    # color_img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    col1.pyplot(use_column_width=True)

    width, height, inference_time, results = yolo.inference(our_image)
    if(results==[]):
        cv2.putText(our_image, 'No Fire', (0, 160), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2)
        st.write("Yolo Model is struggling to find FIRE in this image.")
    else:
        flag=1
        for detection in results:
            id, name, confidence, x, y, w, h = detection
            color = (0, 255, 255)
            cv2.rectangle(our_image, (x, y), (x + w, y + h), color, 2)
            pil_img = Image.fromarray(our_image)
            pil_img.save('detected-images/prediction.jpg')
            # cv2.imwrite('detected-images/prediction.jpg'.format(now),our_image)

    st.text("")
    col2.subheader("Object-Detected Image")
    st.text("")
    plt.figure(figsize = (15,15))
    plt.imshow(our_image)
    col2.pyplot(use_column_width=True)

    if(flag==1):
        # with st.spinner('Enter Password in terminal to alert Admin...'):
        try:
            email_alert()
            st.success('Alerting Email Sent!')
            # st.balloons()
        except:
            st.warning('Something went wrong in emailing.\
                       Allow Less Secure Apps [here](https://myaccount.google.com/lesssecureapps/)')


def object_main():
    
    st.title("Object Detection")
    
    choice = st.radio("", ("Show Demo", "Browse an Image"))
    st.write()

    if choice == "Browse an Image":
        st.set_option('deprecation.showfileUploaderEncoding', False)
        image_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])

        if image_file is not None:
            # our_image = Image.open(image_file)
            our_image = mpimg.imread(image_file)
            # our_image = cv2.imread(image_file)
            detect_objects(our_image)

    elif choice == "Show Demo":
##        our_image = Image.open("images/fire7.jpg")
        our_image = cv2.imread("images/fire_index.jpg")
        detect_objects(our_image)

    st.subheader("Author")
    st.markdown(
        '''
            I am Rahul Arepaka, II year CompSci student at Ecole School of Engineering, Mahindra University
            '''
        '''
            Linkedin Profile : https://www.linkedin.com/in/rahul-arepaka/
            '''
        '''
            Github account : https://github.com/rahularepaka
            '''
    )

    st.info("Feel free to edit with the source code and enjoy coding")
if __name__ == '__main__':
    object_main()