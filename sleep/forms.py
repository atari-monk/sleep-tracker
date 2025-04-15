from django import forms
from .models import SleepRecord
from django.core.exceptions import ValidationError

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['sleep_time', 'wake_time', 'notes']
        widgets = {
            'sleep_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        sleep_time = cleaned_data.get('sleep_time')
        wake_time = cleaned_data.get('wake_time')

        if sleep_time and wake_time:
            if wake_time <= sleep_time:
                raise ValidationError("Wake time must be after sleep time")

            duration = wake_time - sleep_time
            if duration.total_seconds() > 24 * 3600:
                raise ValidationError("Sleep duration cannot be more than 24 hours")
            if duration.total_seconds() < 1 * 300:
                raise ValidationError("Sleep duration should be at least 5 minutes")

        return cleaned_data