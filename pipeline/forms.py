from django import forms

from pipeline.models import Crop_Parameters, Binarize_Parameters

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop_Parameters
        fields = "__all__"

class BinForm(forms.ModelForm):
    class Meta:
        model = Binarize_Parameters
        fields = "__all__"