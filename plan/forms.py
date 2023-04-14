from django.forms import ModelForm
from booking.models import Plans

class PlanForm(ModelForm):
    class Meta:
        model = Plans
        fields = '__all__'