from django import forms
from django.forms.widgets import NumberInput,TimeInput


class BookingForm(forms.Form):
    fname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'inputbx label_name', 'id': 'name', 'placeholder': 'First name *'}))
    mname = forms.CharField(max_length=100, required=False ,widget= forms.TextInput(attrs={'class':'inputbx label_name','id':'label_name','placeholder':'Middle name'}))
    lname = forms.CharField(max_length=100, required=True, widget= forms.TextInput(attrs={'class':'inputbx label_name','id':'label_name','placeholder':'Last name *'}))
    cnum = forms.IntegerField(widget = NumberInput(attrs={'type':'tel','name':'cnum','id':"inputbx label-name mobileNumberInput",'placeholder': 'Enter your Mobile Number','class':'inputbx'}))
    arrivedate = forms.DateField(widget = NumberInput(attrs={'type':'date','ṇame':'date', 'id':"date",'class': 'inputbx label-name','placeholder':'Date'}))
    time = forms.TimeField(widget=TimeInput(attrs={'type':'time','ṇame':'time','class':'inputbx label-name','placeholder':'Time'}))
    adults = forms.IntegerField(widget = NumberInput(attrs={'name':'adults','id':"adults",'min':'0','placeholder':'No. of adults','class':'inputbx label-name'}))
    child = forms.IntegerField(widget = NumberInput(attrs={'name':'children','id':"",'min':'0','placeholder':'No. of children','class':'inputbx label-name'}))
    email = forms.CharField(max_length=100,widget= forms.EmailInput(attrs={'class':'inputbx label_name','id':'label_name','placeholder':'Email'}))
    
