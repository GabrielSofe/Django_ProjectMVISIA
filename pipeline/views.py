from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from pipeline.camera import Camera, Operacoes
from pipeline.forms import CropForm, BinForm
import cv2
import os
from django.conf import settings

txtPath = os.path.join(settings.BASE_DIR,"imgs/saida.txt")

def index(request):
	return render(request, 'pipeline/home.html')

def gen(camera):
	while True:
		frame = camera.stream()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def show_processed_img(operacoes):
	frame = operacoes.update_process()
	ret, jpeg = cv2.imencode('.jpg', frame)
	yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def cam_frame(operacoes):
	frame = operacoes.get_frame()
	ret, jpeg = cv2.imencode('.jpg', frame)
	yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def crop_img(operacoes,x,dx,y,dy):
	operacoes.crop(x,dx,y,dy)

def binarize_img(operacoes,b,g,r,k):
	operacoes.binarize(b,g,r,k)

def background_subtract(operacoes):
	frame = operacoes.background_subtract()
	ret, jpeg = cv2.imencode('.jpg', frame)
	yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
def detect_faces(operacoes):
	frame = operacoes.detect_faces_and_lambda()
	ret, jpeg = cv2.imencode('.jpg', frame)
	yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(Camera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def frame_feed(request):
	return StreamingHttpResponse(cam_frame(Operacoes()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def bkg_subtract_feed(request):
	return StreamingHttpResponse(background_subtract(Operacoes()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def camera_feed(request):
	return StreamingHttpResponse(show_processed_img(Operacoes()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def faces_feed(request):
	return StreamingHttpResponse(detect_faces(Operacoes()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def form_modelform(request):
	cform = CropForm()
	bform = BinForm()
	
	if request.method == "GET":		return render(request, "pipeline/home.html",context={'cform':cform, 'bform':bform})

	else:
		if 'cform' in request.POST:
			cform = CropForm(request.POST)
			if cform.is_valid():
				x = request.POST.get("x")
				dx = request.POST.get("dx")
				y = request.POST.get("y")
				dy = request.POST.get("dy")
				crop_img(Operacoes(),x,dx,y,dy)
				cform = CropForm()
		elif 'bform' in request.POST:
			bform = BinForm(request.POST)
			if bform.is_valid():
				b = request.POST.get("b")
				g = request.POST.get("g")
				r = request.POST.get("r")
				k = request.POST.get("k")
				binarize_img(Operacoes(),b,g,r,k)
				bform = BinForm()
	return render(request, "pipeline/home.html",context={'cform':cform, 'bform':bform})
