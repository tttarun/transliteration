from django import forms

from .models import myuploadfile,review

class MyuploadfileForm(forms.ModelForm):
    class Meta:
        model=myuploadfile
        fields = "__all__"






