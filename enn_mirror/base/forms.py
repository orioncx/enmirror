__author__ = 'root'
from django import forms
from models import MirrorObject

class MirrorAdminForm(forms.ModelForm):
    class Meta:
        model = MirrorObject
        fields='__all__'