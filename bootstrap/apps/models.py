from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "className": self.category,
            "start": self.start_date.isoformat(),
            "end": self.end_date.isoformat() if self.end_date else None,
            "allDay": self.all_day,
        }
    
from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=255)
    className = forms.CharField(max_length=100)
    start = forms.DateTimeField()
    end = forms.DateTimeField(required=False)
    allDay = forms.BooleanField(required=False)
