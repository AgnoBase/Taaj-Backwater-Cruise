from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class AdminProfile(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(AdminProfile, self).__init__(*args, **kwargs)
        
        for fieldname in ['email']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = ('email',)
        
class AdminPassword(PasswordResetForm):
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"class":"input-field","placeholder":"Email"}),
    )
    

    