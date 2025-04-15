from django.db import models
from django.contrib.auth.models import User

class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_time = models.DateTimeField()
    wake_time = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    @property
    def duration(self):
        return self.wake_time - self.sleep_time