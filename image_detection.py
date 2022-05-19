import cv2
import numpy as np
def yolo_objectdetection(image):
	img = np.array(image)
	with open('./YOLOv4/obj.names', 'r') as f:
	    classes = f.read().splitlines()
	net = cv2.dnn.readNetFromDarknet('./YOLOv4/yolov4-custom.cfg', './YOLOv4/backup/yolov4-custom_best.weights')
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
	model = cv2.dnn_DetectionModel(net)
	model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
	classIds, scores, boxes = model.detect(img, confThreshold=0.1, nmsThreshold=0.3)
	txt=[]
	for (classId, score, box) in zip(classIds, scores, boxes):
	    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
	                  color=(0, 255, 0), thickness=2)
	 
	    text = '%s: %.2f' % (classes[classId[0]], score)
	    txt.append(text)
	    cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
	                color=(0, 255, 0), thickness=2)
	color_img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	cv2.imwrite("mailing_images/prediction.jpg", color_img)
	return img,txt