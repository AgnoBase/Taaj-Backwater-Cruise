from django import forms
from django.forms.widgets import NumberInput,TimeInput

class BookingForm(forms.Form):
    fname = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'class':'inputbx','id':'label_name','placeholder':'First name'}))
    mname = forms.CharField(max_length=100,required=False ,widget= forms.TextInput(attrs={'class':'inputbx','id':'label_name','placeholder':'Middle name'}))
    lname = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'class':'inputbx','id':'label_name','placeholder':'Last name'}))
    cnum = forms.IntegerField(widget = NumberInput(attrs={'name':'cnum','id':"label-name",'placeholder':'Enter your Mobile Number','class':'inputbx'}))
    arrivedate = forms.DateField(widget = NumberInput(attrs={'type':'date','ṇame':'date', 'id':"label-name",'class':'inputbx','placeholder':'Date'}))
    time = forms.TimeField(widget=TimeInput(attrs={'type':'time','ṇame':'time','id':"label-name",'class':'inputbx','placeholder':'Time'}))
    adults = forms.IntegerField(widget = NumberInput(attrs={'name':'adults','id':"label-name",'placeholder':'No. of adults','class':'inputbx'}))
    child = forms.IntegerField(widget = NumberInput(attrs={'name':'children','id':"label-name",'placeholder':'No. of children','class':'inputbx'}))
    
class Emailform(forms.Form):
    email= forms.CharField(max_length=100,widget= forms.EmailInput(attrs={'class':'inputbx','id':'label_name','placeholder':'Email'}))