from dataclasses import field, fields
from tkinter import Widget
from xml.etree.ElementInclude import include
from django import forms
from . models import *

class Notesform(forms.ModelForm):
    class Meta:
        model= Notes
        fields=['title','description']

class DateInput(forms.DateInput):
    input_type='date'

class Homeworkform(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finish']


class dashboardform(forms.Form): ##this is custom form which is not a model form but it is designed for general requirements
    text=forms.CharField(max_length=1000,label='Search here ')


class Todoform(forms.ModelForm):
    class Meta:
        model= Todo
        fields=['title','status']