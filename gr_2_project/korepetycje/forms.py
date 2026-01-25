from django import forms
from .models import Nauczyciel

class NauczycielForm(forms.ModelForm):
    class Meta:
        model = Nauczyciel
        fields = '__all__'