from django.urls import path, include
from pipeline import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('camera_feed', views.camera_feed, name='camera_feed'),
    path('frame_feed', views.frame_feed, name='frame_feed'),
    path('bkg_subtract_feed', views.bkg_subtract_feed, name='bkg_subtract_feed'),
    path('faces_feed', views.faces_feed, name='faces_feed'),
    path('', views.form_modelform, name="form_modelform"),
    ]