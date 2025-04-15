from django.db import models
from django.contrib.auth.models import User

class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_time = models.DateTimeField()
    wake_time = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    @property
    def duration(self):
        if self.sleep_time and self.wake_time:
            delta = self.wake_time - self.sleep_time
            total_seconds = delta.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "N/A"