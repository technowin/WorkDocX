from django.db import models

# Create your models here.

class client_module (models.Model):
    client = models.TextField(null=True, blank=True)
    department = models.TextField(null=True, blank=True)
    module = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)             
    created_by = models.TextField(null=True, blank=True) 
    updated_at = models.DateTimeField(null=True, blank=True)               
    updated_by = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'client_module'

    def __str__(self):
        return f"{self.client} - {self.department} - {self.module}"