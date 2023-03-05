from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class AdminProfile(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(AdminProfile, self).__init__(*args, **kwargs)
        
        for fieldname in ['email']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = ('email',)