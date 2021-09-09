import imutils
import cv2,os
import numpy as np
from django.conf import settings
from tensorflow.keras.models import load_model

oimgPath = os.path.join(settings.BASE_DIR,"imgs/original.jpg")
pimgPath = os.path.join(settings.BASE_DIR,"imgs/processed.jpg")
fPath = os.path.join(settings.BASE_DIR,"imgs/frame.jpg")
sPath = os.path.join(settings.BASE_DIR,"imgs/mvisia.jpg")

prototxtPathFACE = os.path.join(settings.BASE_DIR, "face_detector/deploy.prototxt")
weightsPathFACE = os.path.join(settings.BASE_DIR,"face_detector/res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNet(prototxtPathFACE, weightsPathFACE)

prototxtPathAGE = os.path.join(settings.BASE_DIR, "face_detector/age_deploy.prototxt")
weightsPathAGE = os.path.join(settings.BASE_DIR,"face_detector/age_net.caffemodel")
ageNet = cv2.dnn.readNetFromCaffe(prototxtPathAGE, weightsPathAGE)


class Camera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()


	def stream(self):
		success, image = self.video.read()
		ret, jpeg = cv2.imencode('.jpg', image)
		cv2.imwrite(fPath,image)
		return jpeg.tobytes()
		
class Operacoes(object):

	def get_frame(self):
		img = cv2.imread(fPath)
		if img is None:
			img = cv2.imread(sPath)
		cv2.imwrite(oimgPath,img)
		cv2.imwrite(pimgPath,img)
		return img

	def update_process(self):
		img = cv2.imread(pimgPath)
		if img is None:
			img = cv2.imread(sPath)
		return img

	def binarize(self, b, g, r, k):
		img = cv2.imread(pimgPath)
		rows,cols,channels = img.shape
		mask = np.zeros((rows,cols, 1),np.uint8)
		for i in range(rows):
			for j in range(cols):
				if ((img[i,j,0]*int(b) + img[i,j,1]*int(g) + img[i,j,2]*int(r)) > int(k)):
					mask[i,j] = 255
				else:
					mask[i,j] = 0
		cv2.imwrite(pimgPath,mask)
		return mask

	def crop(self,x,dx,y,dy):
		pimg = cv2.imread(pimgPath)
		crop_img = pimg[int(y):int(dy), int(x):int(dx)]
		cv2.imwrite(pimgPath,crop_img)
		return crop_img
	
	def background_subtract(self):
		oimg = cv2.imread(oimgPath)
		cap = cv2.VideoCapture(0)
		ret, img = cap.read()
		sub = (img-oimg)
		cv2.imwrite(pimgPath,sub)
		return sub
	
	def detect_and_predict_age(self,frame, faceNet, ageNet):
		AGE_BUCKETS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)","(38-43)", "(48-53)", "(60-100)"]
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
		faceNet.setInput(blob)
		detections = faceNet.forward()
		
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > 0.5:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				face = frame[startY:endY, startX:endX]
				faceBlob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),(78.4263377603, 87.7689143744, 114.895847746),swapRB=False)
				ageNet.setInput(faceBlob)
				preds = ageNet.forward()
				i = preds[0].argmax()
				age = AGE_BUCKETS[i]
				ageConfidence = preds[0][i]
				text = format(age)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		return frame

	def detect_faces_and_lambda(self):
		frame = cv2.imread(pimgPath)
		frame = imutils.resize(frame, width=650)
		frame = self.detect_and_predict_age(frame, faceNet, ageNet)
		return frame