from django import forms
from .models import SleepRecord

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['sleep_time', 'wake_time', 'notes']
        widgets = {
            'sleep_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }