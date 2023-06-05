from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from booking.models import Plans


class AdminProfile(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(AdminProfile, self).__init__(*args, **kwargs)
        
        for fieldname in ['email']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = ('email',)
        

class PlanForm(ModelForm):
    class Meta:
        model = Plans
        fields = '__all__'